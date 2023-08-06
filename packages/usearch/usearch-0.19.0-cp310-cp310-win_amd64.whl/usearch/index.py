from __future__ import annotations

# The purpose of this file is to provide Pythonic wrapper on top
# the native precompiled CPython module. It improves compatibility
# Python tooling, linters, and static analyzers. It also embeds JIT
# into the primary `Index` class, connecting USearch with Numba.
import os
from typing import Optional, Union, NamedTuple, List, Iterable

import numpy as np

from usearch.compiled import Index as _CompiledIndex, IndexMetadata
from usearch.compiled import SparseIndex as _CompiledSetsIndex

from usearch.compiled import MetricKind, ScalarKind, MetricSignature
from usearch.compiled import (
    DEFAULT_CONNECTIVITY,
    DEFAULT_EXPANSION_ADD,
    DEFAULT_EXPANSION_SEARCH,
    USES_OPENMP,
    USES_SIMSIMD,
    USES_NATIVE_F16,
)

MetricKindBitwise = (
    MetricKind.Hamming,
    MetricKind.Tanimoto,
    MetricKind.Sorensen,
)

SparseIndex = _CompiledSetsIndex

Label = np.uint32


def _normalize_dtype(dtype) -> ScalarKind:
    if dtype is None:
        return ScalarKind.F32
    if isinstance(dtype, ScalarKind):
        return dtype

    if isinstance(dtype, str):
        _normalize = {
            "f64": ScalarKind.F64,
            "f32": ScalarKind.F32,
            "f16": ScalarKind.F16,
            "f8": ScalarKind.F8,
            "b1": ScalarKind.B1,
        }
        return _normalize[dtype.lower()]

    if not isinstance(dtype, ScalarKind):
        _normalize = {
            np.float64: ScalarKind.F64,
            np.float32: ScalarKind.F32,
            np.float16: ScalarKind.F16,
            np.int8: ScalarKind.F8,
        }
        return _normalize[dtype]

    return dtype


class Matches(NamedTuple):
    labels: np.ndarray
    distances: np.ndarray
    counts: Union[np.ndarray, int]

    @property
    def is_batch(self) -> bool:
        return isinstance(self.counts, np.ndarray)

    @property
    def batch_size(self) -> int:
        return len(self.counts) if isinstance(self.counts, np.ndarray) else 1

    @property
    def total_matches(self) -> int:
        return np.sum(self.counts)

    def to_list(self, row: Optional[int] = None) -> Union[List[dict], List[List[dict]]]:
        if not self.is_batch:
            assert row is None, "Exporting a single sequence is only for batch requests"
            labels = self.labels
            distances = self.distances

        elif row is None:
            return [self.to_list(i) for i in range(self.batch_size)]

        else:
            count = self.counts[row]
            labels = self.labels[row, :count]
            distances = self.distances[row, :count]

        return [
            {"label": int(label), "distance": float(distance)}
            for label, distance in zip(labels, distances)
        ]

    def recall_first(self, expected: np.ndarray) -> float:
        best_matches = self.labels if not self.is_batch else self.labels[:, 0]
        return np.sum(best_matches == expected) / len(expected)

    def __repr__(self) -> str:
        return (
            f"usearch.Matches({self.total_matches})"
            if self.is_batch
            else f"usearch.Matches({self.total_matches} across {self.batch_size} queries)"
        )


class CompiledMetric(NamedTuple):
    pointer: int
    kind: MetricKind
    signature: MetricSignature


class Index:
    """Fast JIT-compiled vector-search index for dense equi-dimensional embeddings.

    Vector labels must be integers.
    Vectors must have the same number of dimensions within the index.
    Supports Inner Product, Cosine Distance, Ln measures
    like the Euclidean metric, as well as automatic downcasting
    and quantization.
    """

    def __init__(
        self,
        ndim: int,
        metric: Union[str, MetricKind, CompiledMetric] = MetricKind.IP,
        dtype: Optional[str] = None,
        jit: bool = False,
        connectivity: int = DEFAULT_CONNECTIVITY,
        expansion_add: int = DEFAULT_EXPANSION_ADD,
        expansion_search: int = DEFAULT_EXPANSION_SEARCH,
        tune: bool = False,
        path: Optional[os.PathLike] = None,
        view: bool = False,
    ) -> None:
        """Construct the index and compiles the functions, if requested (expensive).

        :param ndim: Number of vector dimensions
        :type ndim: int

        :param metric: Distance function, defaults to MetricKind.IP
        :type metric: Union[MetricKind, Callable, str], optional
            Kind of the distance function, or the Numba `cfunc` JIT-compiled object.
            Possible `MetricKind` values: IP, Cos, L2sq, Haversine, Pearson,
            Hamming, Tanimoto, Sorensen.
            Not every kind is JIT-able. For Jaccard distance, use `SparseIndex`.

        :param dtype: Scalar type for internal vector storage, defaults to None
        :type dtype: str, optional
            For continuous metrics can be: f16, f32, f64, or f8.
            For bitwise metrics it's implementation-defined, and can't change.
            Example: you can use the `f16` index with `f32` vectors in Euclidean space,
            which will be automatically downcasted.

        :param jit: Enable Numba to JIT compile the metric, defaults to False
        :type jit: bool, optional
            This can result in up-to 3x performance difference on very large vectors
            and very recent hardware, as the Python module is compiled with high
            compatibility in mind and avoids very fancy assembly instructions.

        :param connectivity: Connections per node in HNSW, defaults to None
        :type connectivity: Optional[int], optional
            Hyper-parameter for the number of Graph connections
            per layer of HNSW. The original paper calls it "M".
            Optional, but can't be changed after construction.

        :param expansion_add: Traversal depth on insertions, defaults to None
        :type expansion_add: Optional[int], optional
            Hyper-parameter for the search depth when inserting new
            vectors. The original paper calls it "efConstruction".
            Can be changed afterwards, as the `.expansion_add`.

        :param expansion_search: Traversal depth on queries, defaults to None
        :type expansion_search: Optional[int], optional
            Hyper-parameter for the search depth when querying
            nearest neighbors. The original paper calls it "ef".
            Can be changed afterwards, as the `.expansion_search`.

        :param tune: Automatically adjusts hyper-parameters, defaults to False
        :type tune: bool, optional

        :param path: Where to store the index, defaults to None
        :type path: Optional[os.PathLike], optional
        :param view: Are we simply viewing an immutable index, defaults to False
        :type view: bool, optional
        """

        if metric in MetricKindBitwise:
            assert dtype is None or dtype == ScalarKind.B1
            dtype = ScalarKind.B1
        else:
            dtype = _normalize_dtype(dtype)

        if metric is None:
            metric = MetricKind.IP

        if isinstance(metric, str):
            _normalize = {
                "cos": MetricKind.Cos,
                "ip": MetricKind.IP,
                "l2_sq": MetricKind.L2sq,
                "haversine": MetricKind.Haversine,
                "perason": MetricKind.Pearson,
                "hamming": MetricKind.Hamming,
                "tanimoto": MetricKind.Tanimoto,
                "sorensen": MetricKind.Sorensen,
            }
            metric = _normalize[metric.lower()]

        if isinstance(metric, MetricKind) and jit:
            try:
                from usearch.numba import jit
            except ImportError:
                raise ModuleNotFoundError(
                    "To use JIT install Numba with `pip install numba`."
                    "Alternatively, reinstall with `pip install usearch[jit]`"
                )

            metric = jit(
                ndim=ndim,
                metric=metric,
                dtype=dtype,
            )

        if isinstance(metric, MetricKind):
            self._metric_kind = metric
            self._metric_jit = None
            self._metric_pointer = 0
            self._metric_signature = MetricSignature.ArrayArraySize
        elif isinstance(metric, CompiledMetric):
            self._metric_jit = metric
            self._metric_kind = metric.kind
            self._metric_pointer = metric.pointer
            self._metric_signature = metric.signature
        else:
            raise ValueError(
                "The `metric` must be a `CompiledMetric` or a `MetricKind`"
            )

        self._compiled = _CompiledIndex(
            ndim=ndim,
            dtype=dtype,
            metric=self._metric_kind,
            metric_pointer=self._metric_pointer,
            metric_signature=self._metric_signature,
            connectivity=connectivity,
            expansion_add=expansion_add,
            expansion_search=expansion_search,
            tune=tune,
        )

        self.path = path
        if path and os.path.exists(path):
            if view:
                self._compiled.view(path)
            else:
                self._compiled.load(path)

    @staticmethod
    def metadata(path: os.PathLike) -> IndexMetadata:
        return IndexMetadata(path)

    @staticmethod
    def restore(path: os.PathLike, view: bool = False) -> Index:
        meta = Index.metadata(path)
        bits_per_scalar = {
            ScalarKind.F8: 8,
            ScalarKind.F16: 16,
            ScalarKind.F32: 32,
            ScalarKind.F64: 64,
            ScalarKind.B1: 1,
        }[meta.scalar_kind]
        ndim = meta.bytes_for_vectors * 8 // meta.size // bits_per_scalar
        return Index(
            ndim=ndim,
            connectivity=meta.connectivity,
            metric=meta.metric,
            path=path,
            view=view,
        )

    def add(
        self, labels, vectors, *, copy: bool = True, threads: int = 0
    ) -> Union[int, np.ndarray]:
        """Inserts one or move vectors into the index.

        For maximal performance the `labels` and `vectors`
        should conform to the Python's "buffer protocol" spec.

        To index a single entry:
            labels: int, vectors: np.ndarray.
        To index many entries:
            labels: np.ndarray, vectors: np.ndarray.

        When working with extremely large indexes, you may want to
        pass `copy=False`, if you can guarantee the lifetime of the
        primary vectors store during the process of construction.

        :param labels: Unique identifier for passed vectors, optional
        :type labels: Buffer
        :param vectors: Collection of vectors.
        :type vectors: Buffer
        :param copy: Should the index store a copy of vectors, defaults to True
        :type copy: bool, optional
        :param threads: Optimal number of cores to use, defaults to 0
        :type threads: int, optional

        :return: Inserted label or labels
        :type: Union[int, np.ndarray]
        """
        assert isinstance(vectors, np.ndarray), "Expects a NumPy array"
        assert vectors.ndim == 1 or vectors.ndim == 2, "Expects a matrix or vector"
        is_batch = vectors.ndim == 2
        generate_labels = labels is None

        # If no `labels` were provided, generate some
        if generate_labels:
            start_id = len(self._compiled)
            if is_batch:
                labels = np.arange(start_id, start_id + vectors.shape[0])
            else:
                labels = start_id
        if isinstance(labels, np.ndarray):
            labels = labels.astype(Label)
        elif isinstance(labels, Iterable):
            labels = np.array(labels, dtype=Label)

        self._compiled.add(labels, vectors, copy=copy, threads=threads)

        return labels

    def search(
        self, vectors, k: int = 10, *, threads: int = 0, exact: bool = False
    ) -> Matches:
        """Performs approximate nearest neighbors search for one or more queries.

        :param vectors: Query vector or vectors.
        :type vectors: Buffer
        :param k: Upper limit on the number of matches to find, defaults to 10
        :type k: int, optional

        :param threads: Optimal number of cores to use, defaults to 0
        :type threads: int, optional
        :param exact: Perform exhaustive linear-time exact search, defaults to False
        :type exact: bool, optional
        :return: Approximate matches for one or more queries
        :rtype: Matches
        """
        tuple_ = self._compiled.search(
            vectors,
            k,
            exact=exact,
            threads=threads,
        )
        return Matches(*tuple_)

    @property
    def specs(self) -> dict:
        return {
            "Class": "usearch.Index",
            "Connectivity": self.connectivity,
            "Size": self.size,
            "Dimensions": self.ndim,
            "Expansion@Add": self.expansion_add,
            "Expansion@Search": self.expansion_search,
            "OpenMP": USES_OPENMP,
            "SimSIMD": USES_SIMSIMD,
            "NativeF16": USES_NATIVE_F16,
            "JIT": self.jit,
            "DType": self.dtype,
            "Path": self.path,
        }

    def __len__(self) -> int:
        return self._compiled.__len__()

    @property
    def jit(self) -> bool:
        return self._metric_jit is not None

    @property
    def size(self) -> int:
        return self._compiled.size

    @property
    def ndim(self) -> int:
        return self._compiled.ndim

    @property
    def metric(self) -> MetricKind:
        return self._metric_kind

    @property
    def dtype(self) -> ScalarKind:
        return self._compiled.dtype

    @property
    def connectivity(self) -> int:
        return self._compiled.connectivity

    @property
    def capacity(self) -> int:
        return self._compiled.capacity

    @property
    def memory_usage(self) -> int:
        return self._compiled.memory_usage

    @property
    def expansion_add(self) -> int:
        return self._compiled.expansion_add

    @property
    def expansion_search(self) -> int:
        return self._compiled.expansion_search

    @expansion_add.setter
    def expansion_add(self, v: int):
        self._compiled.expansion_add = v

    @expansion_search.setter
    def expansion_search(self, v: int):
        self._compiled.expansion_search = v

    def save(self, path: os.PathLike):
        self._compiled.save(path)

    def load(self, path: os.PathLike):
        self._compiled.load(path)

    def view(self, path: os.PathLike):
        self._compiled.view(path)

    def clear(self):
        self._compiled.clear()

    @property
    def labels(self) -> np.ndarray:
        return self._compiled.labels

    def get_vectors(
        self, labels: np.ndarray, dtype: ScalarKind = ScalarKind.F32
    ) -> np.ndarray:
        dtype = _normalize_dtype(dtype)
        return np.vstack([self._compiled.__getitem__(l, dtype) for l in labels])

    @property
    def vectors(self) -> np.ndarray:
        return self.get_vectors(self.labels)

    def __delitem__(self, label: int):
        raise NotImplementedError()

    def __contains__(self, label: int) -> bool:
        return self._compiled.__contains__(label)

    def __getitem__(self, label: int) -> np.ndarray:
        return self._compiled.__getitem__(label)

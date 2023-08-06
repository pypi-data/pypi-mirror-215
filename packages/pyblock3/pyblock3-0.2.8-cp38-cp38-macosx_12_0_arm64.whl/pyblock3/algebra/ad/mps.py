
#  pyblock3: An Efficient python MPS/DMRG Library
#  Copyright (C) 2020 The pyblock3 developers. All Rights Reserved.
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program. If not, see <https://www.gnu.org/licenses/>.
#
#

"""
1D tensor network for MPS/MPO.
"""

import numpy as np
from numpy.lib.mixins import NDArrayOperatorsMixin
import numbers
from collections import Counter
from functools import reduce

from ..symmetry import BondInfo, BondFusingInfo
from ..core import SparseTensor, SubTensor, SliceableTensor, FermionTensor
from .flat import FlatFermionTensor, FlatSparseTensor
from ..mps import MPSInfo
from ...symbolic.symbolic import SymbolicSparseTensor

from . import ENABLE_JAX

if ENABLE_JAX:
    import jax.numpy as jnp
else:
    jnp = np

def implements(np_func):
    global _numpy_func_impls
    return lambda f: (_numpy_func_impls.update({np_func: f})
                      if np_func not in _numpy_func_impls else None,
                      _numpy_func_impls[np_func])[1]


def jax_pytree_node(cls):
    if ENABLE_JAX:
        from jax import tree_util
        tree_util.register_pytree_node(
            cls, cls.pytree_flatten, cls.pytree_unflatten)
    return cls



_mps_numpy_func_impls = {}
_numpy_func_impls = _mps_numpy_func_impls

@jax_pytree_node
class MPS(NDArrayOperatorsMixin):
    """
    Matrix Product State / Matrix Product Operator.

    Attributes:
        tensors : list(SparseTensor/FermionTensor)
            A list of block-sparse tensors.
        n_sites : int
            Number of sites.
        const : float
            Constant term.
        opts : dict or None
            Options indicating how bond dimension truncation
            should be done after MPO @ MPS, etc.
            Possible options are: max_bond_dim, cutoff, max_dw, norm_cutoff
        dq : SZ
            Delta quantum of MPO operator
    """

    def __init__(self, tensors, const=0.0, opts=None, dq=None):
        self.tensors = tensors
        self.opts = opts if opts is not None else {}
        self.const = const
        self.dq = dq

    def pytree_flatten(self):
        traced = (*self.tensors, self.const, )
        others = (self.opts, self.dq, )
        return traced, others
    
    @classmethod
    def pytree_unflatten(cls, others, traced):
        opts, dq = others
        tensors, const = list(traced[:-1]), traced[-1]
        return cls(tensors=tensors, const=const, opts=opts, dq=dq)

    @property
    def n_sites(self):
        """Number of sites"""
        return len(self.tensors)

    @property
    def dtype(self):
        return self.tensors[0].dtype if self.n_sites != 0 else float

    def __len__(self):
        return len(self.tensors)

    @property
    def T(self):
        tensors = [None] * self.n_sites
        for i in range(self.n_sites):
            assert self.tensors[i].ndim % 2 == 0
            d = self.tensors[i].ndim // 2 - 1
            tr = (0, *tuple(range(d + 1, d + d + 1)),
                  *tuple(range(1, d + 1)), d + d + 1)
            tensors[i] = self.tensors[i].transpose(tr)
        return MPS(tensors=tensors, const=self.const, opts=self.opts, dq=self.dq)

    @staticmethod
    def ones(info, dtype=float, opts=None):
        """Construct unfused MPS from MPSInfo, with identity matrix elements."""
        tensors = [None] * info.n_sites
        for i in range(info.n_sites):
            if isinstance(info.basis[i], BondInfo):
                tensors[i] = SparseTensor.ones(
                    (info.left_dims[i], info.basis[i], info.left_dims[i + 1]), dtype=dtype)
            else:
                tensors[i] = FlatSparseTensor.ones(
                    (info.left_dims[i], info.basis[i], info.left_dims[i + 1]), dtype=dtype)
        return MPS(tensors=tensors, opts=opts)

    @staticmethod
    def zeros(info, dtype=float, opts=None):
        """Construct unfused MPS from MPSInfo, with zero matrix elements."""
        tensors = [None] * info.n_sites
        for i in range(info.n_sites):
            if isinstance(info.basis[i], BondInfo):
                tensors[i] = SparseTensor.zeros(
                    (info.left_dims[i], info.basis[i], info.left_dims[i + 1]), dtype=dtype)
            else:
                tensors[i] = FlatSparseTensor.zeros(
                    (info.left_dims[i], info.basis[i], info.left_dims[i + 1]), dtype=dtype)
        return MPS(tensors=tensors, opts=opts)

    @staticmethod
    def random(info, low=0, high=1, dtype=float, opts=None):
        """Construct unfused MPS from MPSInfo, with random matrix elements."""
        tensors = [None] * info.n_sites
        for i in range(info.n_sites):
            if isinstance(info.basis[i], BondInfo):
                tensors[i] = SparseTensor.random(
                    (info.left_dims[i], info.basis[i], info.left_dims[i + 1]),
                    dtype=dtype) * (high - low) + low
            else:
                tensors[i] = FlatSparseTensor.random(
                    (info.left_dims[i], info.basis[i], info.left_dims[i + 1]),
                    dtype=dtype) * (high - low) + low
        return MPS(tensors=tensors, opts=opts)
    
    def fix_pattern(self, pattern=None):
        dq = None
        for i in range(self.n_sites):
            self.tensors[i], dq = self.tensors[i].fix_pattern(pattern=pattern, dq=dq)
        return dq

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        if ufunc in _mps_numpy_func_impls:
            types = tuple(
                x.__class__ for x in inputs if not isinstance(x, numbers.Number))
            return self.__array_function__(ufunc, types, inputs, kwargs)
        out = kwargs.pop("out", None)
        if out is not None and not all(isinstance(x, MPS) for x in out):
            return NotImplemented
        if method == "__call__":
            if ufunc.__name__ in ["add", "subtract"]:
                a, b = inputs
                if ufunc.__name__ == "subtract":
                    b = -b
                if isinstance(a, numbers.Number):
                    const = a + b.const
                    tensors = b.tensors
                elif isinstance(b, numbers.Number):
                    const = a.const + b
                    tensors = a.tensors
                else:
                    const = a.const + b.const
                    tensors = MPS._add(a, b).tensors
                    if len(a.opts) != 0:
                        tensors = MPS.compress(
                            MPS(tensors=tensors), **a.opts)[0].tensors
            elif ufunc.__name__ in ["multiply", "divide", "true_divide"]:
                a, b = inputs
                if isinstance(a, numbers.Number):
                    const = getattr(ufunc, method)(a, b.const)
                    tensors = [getattr(ufunc, method)(
                        a, b.tensors[0])] + b.tensors[1:]
                elif isinstance(b, numbers.Number):
                    const = getattr(ufunc, method)(a.const, b)
                    tensors = [getattr(ufunc, method)(
                        a.tensors[0], b)] + a.tensors[1:]
                else:
                    return NotImplemented
            elif len(inputs) == 1:
                const = getattr(ufunc, method)(inputs[0].const)
                if ufunc.__name__ in ["conjugate"]:
                    tensors = [getattr(ufunc, method)(ts)
                               for ts in inputs[0].tensors]
                else:
                    tensors = [getattr(ufunc, method)(
                        inputs[0].tensors[0])] + inputs[0].tensors[1:]
            else:
                return NotImplemented
        else:
            return NotImplemented
        if out is not None:
            if isinstance(out, tuple):
                out[0].tensors = tensors
                out[0].const = const
                out[0].opts = self.opts
            else:
                out.tensors = tensors
                out.const = const
                out.opts = self.opts
        return MPS(tensors=tensors, const=const, opts=self.opts, dq=self.dq)

    def __array_function__(self, func, types, args, kwargs):
        if func not in _mps_numpy_func_impls:
            return NotImplemented
        if not all(issubclass(t, self.__class__) for t in types):
            return NotImplemented
        return _mps_numpy_func_impls[func](*args, **kwargs)

    def canonicalize(self, center):
        """
        MPS canonicalization.

        Args:
            center : int
                Site index of canonicalization center.
        """
        tensors = [ts for ts in self.tensors]
        if center < 0:
            center = self.n_sites + center
        assert 0 <= center < self.n_sites
        for i in range(0, center):
            q, r = tensors[i].left_canonicalize()
            tensors[i] = q
            tensors[i + 1] = np.tensordot(r, tensors[i + 1], axes=1)
        for i in range(self.n_sites - 1, center, -1):
            l, q = tensors[i].right_canonicalize()
            tensors[i] = q
            tensors[i - 1] = np.tensordot(tensors[i - 1], l, axes=1)
        return MPS(tensors=tensors, opts=self.opts, const=self.const, dq=self.dq)

    def compress(self, **opts):
        """
        MPS bond dimension compression.

        Args:
            max_bond_dim : int
                Maximal total bond dimension.
                If `k == -1`, no restriction in total bond dimension.
            cutoff : double
                Minimal kept singluar value.
            max_dw : double
                Maximal sum of square of discarded singluar values.
        """
        merror = 0.0
        tensors = [ts for ts in self.tensors]
        left = opts.pop("left", True)
        if left:
            for i in range(0, self.n_sites - 1):
                q, r = tensors[i].left_canonicalize()
                tensors[i] = q
                tensors[i + 1] = np.tensordot(r, tensors[i + 1], axes=1)
            for i in range(self.n_sites - 1, 0, -1):
                l, s, r = tensors[i].right_svd(full_matrices=False)
                l, s, r, err = r.__class__.truncate_svd(l, s, r, **opts)
                rs = np.tensordot(s.diag(), r, axes=1)
                tensors[i] = rs
                tensors[i - 1] = np.tensordot(tensors[i - 1], l, axes=1)
                merror = max(merror, err)
        else:
            for i in range(self.n_sites - 1, 0, -1):
                l, q = tensors[i].right_canonicalize()
                tensors[i] = q
                tensors[i - 1] = np.tensordot(tensors[i - 1], l, axes=1)
            for i in range(0, self.n_sites - 1, 1):
                l, s, r = tensors[i].left_svd(full_matrices=False)
                l, s, r, err = l.__class__.truncate_svd(l, s, r, **opts)
                ls = np.tensordot(l, s.diag(), axes=1)
                tensors[i] = ls
                tensors[i + 1] = np.tensordot(r, tensors[i + 1], axes=1)
                merror = max(merror, err)
        return MPS(tensors=tensors, const=self.const, opts=self.opts, dq=self.dq), merror

    @staticmethod
    def _add(a, b):
        """Add two MPS."""
        assert isinstance(a, MPS) and isinstance(b, MPS)
        assert a.n_sites == b.n_sites
        n_sites = a.n_sites

        if n_sites == 1:
            return MPS(tensors=[a[0] + b[0]], const=a.const + b.const, opts=a.opts, dq=a.dq)

        ainfos = [t.infos for t in a.tensors]
        binfos = [t.infos for t in b.tensors]
        sum_bonds = []
        sum_bonds.append(ainfos[0][0])
        for i in range(n_sites - 1):
            x = ainfos[i + 1][0] | ainfos[i][-1]
            y = binfos[i + 1][0] | binfos[i][-1]
            sum_bonds.append(x + y)
        sum_bonds.append(ainfos[-1][-1])

        tensors = []
        for i in range(n_sites):
            tensors.append(a.tensors[i].kron_add(
                b.tensors[i], infos=(sum_bonds[i], sum_bonds[i + 1])))
        return MPS(tensors=tensors, const=a.const + b.const, opts=a.opts, dq=a.dq)

    def __getitem__(self, i):
        return self.tensors[i]

    def __setitem__(self, i, ts):
        self.tensors[i] = ts

    def conj(self):
        return np.conj(self)

    @staticmethod
    @implements(np.copy)
    def _copy(x):
        return MPS(tensors=[t.copy() for t in x.tensors], const=x.const, opts=x.opts.copy(), dq=x.dq)

    def copy(self):
        return np.copy(self)

    @staticmethod
    @implements(np.dot)
    def _dot(a, b, out=None):
        if isinstance(a, numbers.Number) or isinstance(b, numbers.Number):
            return np.multiply(a, b, out=out)

        assert isinstance(a, MPS) and isinstance(b, MPS)
        assert a.n_sites == b.n_sites

        left = jnp.array(0.0)
        for i in range(a.n_sites):
            assert a.tensors[i].ndim == b.tensors[i].ndim
            if a.tensors[i].n_blocks == 0 or b.tensors[i].n_blocks == 0:
                return 0

            if i != a.n_sites - 1:
                cidx = list(range(0, a.tensors[i].ndim - 1))
            else:
                cidx = list(range(0, a.tensors[i].ndim))

            if i == 0:
                left = np.tensordot(
                    a.tensors[i], b.tensors[i], axes=(cidx, cidx))
            else:
                lbra = np.tensordot(left, a.tensors[i], axes=([0], [0]))
                left = np.tensordot(lbra, b.tensors[i], axes=(cidx, cidx))

        if ENABLE_JAX:
            r = left
        else:
            r = left if isinstance(left, float) else left.item()

        if out is not None:
            out[()] = r

        return r + a.const * b.const

    def dot(self, b, out=None):
        return np.dot(self, b, out=out)

    @staticmethod
    @implements(np.linalg.norm)
    def _norm(x):
        d = np.conj(x).dot(x)
        assert abs(d.imag) / abs(d.real) < 1E-10
        return np.sqrt(abs(d.real) if abs(d.real) < 1E-10 else d.real)

    def norm(self):
        return np.linalg.norm(self)

    @staticmethod
    @implements(np.matmul)
    def _matmul(a, b, out=None):
        if isinstance(a, numbers.Number) or isinstance(b, numbers.Number):
            return np.multiply(a, b, out=out)

        assert isinstance(a, MPS) and isinstance(b, MPS)

        opts = {**a.opts, **b.opts}

        if b.n_sites == 1:
            r = a.tensors[0].__class__.pdot(a.tensors, b.tensors[0])
            ir = r.infos
            rl = r.ones(bond_infos=(ir[1], ir[0], ir[1]), pattern="-++")
            rr = r.ones(bond_infos=(ir[-2], ir[-1], ir[-1]), pattern="++-")
            r = np.tensordot(rl, r, axes=2)
            r = np.tensordot(r, rr, axes=2)
            tensors = [r]
        elif a.n_sites == 1:
            raise NotImplementedError("not implemented yet")
        else:

            assert a.n_sites == b.n_sites

            n_sites = a.n_sites
            tensors = [None] * n_sites

            if all(ta.ndim == tb.ndim and ta.ndim % 2 == 1 for ta, tb in zip(a.tensors, b.tensors)):
                return np.dot(a, b, out=out)

            for i in range(n_sites):
                tensors[i] = a.tensors[i].pdot(b.tensors[i])

            # merge virtual dims
            prod_bonds = []
            infos = [t.infos for t in tensors]
            prod_bonds.append(infos[0][0] ^ infos[0][1])
            for tl, tr in zip(infos[1:], infos[:-1]):
                prod_bonds.append((tl[0] | tr[-2]) ^ (tl[1] | tr[-1]))
            prod_bonds.append(infos[-1][-2] ^ infos[-1][-1])

            for i in range(n_sites):
                old_pattern = getattr(tensors[i], "pattern", None)
                tensors[i] = tensors[i].fuse(-2, -1, info=prod_bonds[i + 1]
                                             ).fuse(0, 1, info=prod_bonds[i])
                if old_pattern is not None:
                    tensors[i].pattern = tensors[i].pattern[:-1] + old_pattern[-1]
                

        r = MPS(tensors=tensors)

        # const terms
        if a.const != 0 and b.const == 0:
            r += a.const * b
        elif a.const == 0 and b.const != 0:
            r += a * b.const
        elif a.const != 0 and b.const != 0:
            r += a * b.const + a.const * b
            r.const -= a.const * b.const

        # compression
        if len(opts) != 0:
            if r.n_sites > 1:
                r, _ = MPS.compress(r, **opts)
            r.opts = opts

        if out is not None:
            out.tensors = r.tensors
            out.const = r.const
            out.opts = r.opts

        return r

    def matmul(self, b, out=None):
        return np.matmul(self, b, out=out)

    @property
    def bond_dim(self):
        bonds = []
        infos = [t.infos for t in self.tensors]
        infos = [i if len(i) != 0 else (BondInfo(), ) for i in infos]
        d = infos[0][0].n_bonds
        bonds.append(infos[0][0])
        for i in range(self.n_sites - 1):
            d = max(d, (infos[i + 1][0] | infos[i][-1]).n_bonds)
        d = max(d, infos[-1][-1].n_bonds)
        return d

    def show_bond_dims(self):
        bonds = []
        infos = [t.infos for t in self.tensors]
        infos = [i if len(i) != 0 else (BondInfo(), ) for i in infos]
        bonds.append(infos[0][0])
        for i in range(self.n_sites - 1):
            bonds.append(infos[i + 1][0] | infos[i][-1])
        bonds.append(infos[-1][-1])
        r = '|'.join([str(x.n_bonds) for x in bonds])
        return r if self.const == 0 else r + " (%+12.5f)" % self.const

    @staticmethod
    def _to_sliceable(a, info=None):
        return a.to_sliceable(info=info)

    def to_sliceable(self, info=None):
        """
        Get a shallow copy of MPS with SliceableTensor.

        Args:
            info : MPSInfo, optional
                MPSInfo containing the complete basis BondInfo.
                If not specified, the BondInfo will be generated from the MPS,
                which may be incomplete.
        """

        # virtual dims
        infos = [t.infos for t in self.tensors]
        bonds = []
        bonds.append(infos[0][0])
        for i in range(self.n_sites - 1):
            bonds.append(infos[i + 1][0] | infos[i][-1])
        bonds.append(infos[-1][-1])

        tensors = [None] * self.n_sites
        k = 0
        for i in range(self.n_sites):
            if info is None:
                minfos = infos[i][1:self[i].ndim - 1]
            else:
                minfos = info.basis[k:k + self[i].ndim - 2]
                k += self[i].ndim - 2
            sinfos = (bonds[i], *minfos, bonds[i + 1])
            tensors[i] = self[i].to_sliceable(infos=sinfos)

        return MPS(tensors=tensors, const=self.const, opts=self.opts, dq=self.dq)

    @staticmethod
    def _to_sparse(a):
        return a.to_sparse()

    def to_sparse(self):
        tensors = [None] * len(self.tensors)
        for it, ts in enumerate(self.tensors):
            if isinstance(ts, FlatSparseTensor) or isinstance(ts, FlatFermionTensor):
                tensors[it] = ts
            else:
                tensors[it] = ts.to_sparse(dq=None if it == 0 else self.dq)
        return MPS(tensors=tensors, const=self.const, opts=self.opts, dq=self.dq)

    @staticmethod
    def _to_symbolic(a):
        return a.to_sparse()

    def to_symbolic(self):
        tensors = [None] * len(self.tensors)
        for it, ts in enumerate(self.tensors):
            if isinstance(ts, FlatFermionTensor):
                tensors[it] = ts.to_fermion()
            else:
                tensors[it] = ts
        infos = [t.infos for t in tensors]
        bonds = []
        bonds.append(infos[0][0])
        for i in range(self.n_sites - 1):
            bonds.append(infos[i + 1][0] | infos[i][-1])
        bonds.append(infos[-1][-1])
        for it, ts in enumerate(tensors):
            pos = -1 if it == self.n_sites - 1 else int(it != 0)
            if isinstance(ts, SymbolicSparseTensor):
                tensors[it] = ts
            if isinstance(ts, FlatSparseTensor):
                assert False
            elif isinstance(ts, FlatFermionTensor):
                tensors[it] = SymbolicSparseTensor.from_sparse(ts.to_fermion(),
                    pos=pos, infos=bonds[it:it + 2], dq=None if it == 0 else self.dq)
            else:
                tensors[it] = SymbolicSparseTensor.from_sparse(ts,
                    pos=pos, infos=bonds[it:it + 2], dq=None if it == 0 else self.dq)
        return MPS(tensors=tensors, const=self.const, opts=self.opts, dq=self.dq)

    @staticmethod
    def _to_non_flat(a):
        return a.to_non_flat()

    def to_non_flat(self):
        tensors = [None] * len(self.tensors)
        for it, ts in enumerate(self.tensors):
            if isinstance(ts, FlatSparseTensor):
                tensors[it] = ts.to_sparse()
            elif isinstance(ts, FlatFermionTensor):
                tensors[it] = ts.to_fermion()
            elif isinstance(ts, SparseTensor) or isinstance(ts, FermionTensor):
                tensors[it] = ts
            else:
                tensors[it] = ts.to_sparse()
        return MPS(tensors=tensors, const=self.const, opts=self.opts, dq=self.dq)

    @staticmethod
    def _to_flat(a):
        return a.to_flat()

    def to_flat(self):
        tensors = [None] * len(self.tensors)
        for it, ts in enumerate(self.tensors):
            if isinstance(ts, FlatSparseTensor) or isinstance(ts, FlatFermionTensor):
                tensors[it] = ts
            elif isinstance(ts, SparseTensor):
                tensors[it] = FlatSparseTensor.from_sparse(ts)
            elif isinstance(ts, FermionTensor):
                tensors[it] = FlatFermionTensor.from_fermion(ts)
            else:
                tensors[it] = ts.to_flat()
        return MPS(tensors=tensors, const=self.const, opts=self.opts, dq=self.dq)

    @staticmethod
    def _from_flat(a):
        return a.from_flat()

    def from_flat(self):
        from ..flat import FlatFermionTensor as FF, FlatSparseTensor as FS
        m = self.to_flat()
        tensors = [None] * len(m.tensors)
        for it, ts in enumerate(m.tensors):
            if isinstance(ts, FS):
                tensors[it] = FlatSparseTensor.from_flat(ts)
            else:
                tensors[it] = FlatFermionTensor.from_flat(ts)
        return MPS(tensors=tensors, const=self.const, opts=self.opts, dq=self.dq)
    
    @staticmethod
    def _from_core(a):
        return a.from_core()

    def from_core(self):
        return MPS(tensors=self.tensors, const=self.const, opts=self.opts, dq=self.dq)

    @staticmethod
    def _simplify(a):
        """Reduce virtual bond dimensions for symbolic sparse tensors.
        Only works when tensor is SparseSymbolicTensor."""
        return a.simplify()

    def simplify(self):
        """Reduce virtual bond dimensions for symbolic sparse tensors.
        Only works when tensor is SparseSymbolicTensor."""

        tensors = self.tensors[:]

        for i in range(self.n_sites - 1):
            r = tensors[i].get_remap(left=False)
            tensors[i] = tensors[i].simplify(r, left=False)
            tensors[i + 1] = tensors[i + 1].simplify(r, left=True)

        for i in range(self.n_sites - 1, 0, -1):
            r = tensors[i].get_remap(left=True)
            tensors[i] = tensors[i].simplify(r, left=True)
            tensors[i - 1] = tensors[i - 1].simplify(r, left=False)

        return MPS(tensors=tensors, const=self.const, opts=self.opts, dq=self.dq)

    @staticmethod
    def _amplitude(a, det):
        return a.amplitude(det=det)

    def amplitude(self, det):
        """
        Return overlap <MPS|det>.
        MPS tensors must be sliceable."""
        tensors = [None] * self.n_sites
        k = 0
        for i in range(self.n_sites):
            assert isinstance(self[i], SliceableTensor)
            tensors[i] = self[i][(
                slice(None), *det[k:k + self[i].ndim - 2], slice(None))]
            k += self[i].ndim - 2
        assert k == len(det)
        r = reduce(np.dot, tensors).to_sparse()
        return 0 if r.n_blocks == 0 else r.blocks[0].item(0)

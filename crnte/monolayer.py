"""Spin-resolved tight-binding model of the hexagonal (honeycomb) h-CrN monolayer.

PROVISIONAL minimal model (pipeline validation, not yet fit to DFT).
------------------------------------------------------------------
Cr and N sit on the two sublattices (A, B) of a planar honeycomb, graphene-like.
For this first pass we keep ONE effective orbital per site (Cr d_eff, N p_eff) and impose
the Cr local moment as a Stoner exchange field that spin-splits the Cr level by Delta_ex.

This deliberately reproduces the *qualitative* h-CrN target (see memory / Kuklin 2017 +
arXiv:2408.06754): a DIRAC HALF-METAL — one spin channel metallic (gapless Dirac point at the
Fermi level), the other gapped by ~4 eV — with the moment (3 mu_B/Cr) supplied by the exchange
field rather than derived. The full multi-orbital Cr-t2g + N-p Slater-Koster fit to the
published bands replaces this later; the geometry/Bloch machinery below carries over unchanged.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

# --- provisional parameters (eV, Angstrom); targets from Kuklin 2017 (c6nr07790k.pdf) ---
CrN_BOND = 1.884           # Cr-N bond length (Angstrom), Kuklin 2017
A_LATT = 3.258             # measured honeycomb lattice constant (Angstrom), Kuklin 2017
MINORITY_GAP = 3.9         # spin-down band gap (eV), Kuklin 2017 (PBE = HSE06)


@dataclass(frozen=True)
class MonolayerParams:
    a: float = A_LATT       # lattice constant (Angstrom)
    eps_N: float = -MINORITY_GAP / 2.0   # N p_eff on-site (eV); places majority node at E_F
    eps_Cr: float = 0.0     # Cr d_eff spin-averaged on-site (eV)
    t: float = 1.5          # Cr-N nearest-neighbour hopping (eV)
    delta_ex: float = MINORITY_GAP       # Cr exchange (Stoner) splitting -> 3.9 eV minority gap
    # With eps_Cr - delta_ex/2 == eps_N the MAJORITY channel is a gapless Dirac semimetal,
    # while the MINORITY Cr level sits ~delta_ex above N -> ~4 eV minority gap. E_F = eps_N.

    def onsite_Cr(self, spin: int) -> float:
        """spin = +1 (majority/up) or -1 (minority/down)."""
        return self.eps_Cr - spin * self.delta_ex / 2.0

    @property
    def E_fermi(self) -> float:
        """Charge-neutral Fermi level = majority Dirac-point energy (this minimal model)."""
        return self.eps_N


def lattice_geometry(a: float):
    """Return (a1, a2, deltas, b1, b2) for a graphene-like honeycomb, lattice constant a.

    a1, a2   : real-space primitive vectors (|a_i| = a).
    deltas   : the three A->B nearest-neighbour vectors (|delta| = a/sqrt(3)).
    b1, b2   : reciprocal primitive vectors, a_i . b_j = 2*pi*delta_ij.
    """
    d = a / np.sqrt(3.0)                      # bond length
    a1 = d * np.array([1.5,  np.sqrt(3.0) / 2.0])
    a2 = d * np.array([1.5, -np.sqrt(3.0) / 2.0])
    deltas = [
        d * np.array([1.0, 0.0]),
        d * np.array([-0.5,  np.sqrt(3.0) / 2.0]),
        d * np.array([-0.5, -np.sqrt(3.0) / 2.0]),
    ]
    amat = np.vstack([a1, a2])               # rows = a1, a2
    bmat = 2.0 * np.pi * np.linalg.inv(amat).T   # rows = b1, b2  (a_i . b_j = 2pi dij)
    b1, b2 = bmat[0], bmat[1]
    return a1, a2, deltas, b1, b2


def bloch_hamiltonian(k, p: MonolayerParams, spin: int) -> np.ndarray:
    """2x2 Bloch Hamiltonian H(k) for one spin. k is a 2-vector (1/Angstrom)."""
    _, _, deltas, _, _ = lattice_geometry(p.a)
    f = sum(np.exp(1j * np.dot(k, dvec)) for dvec in deltas)   # A->B structure factor
    return np.array([
        [p.onsite_Cr(spin), p.t * f],
        [p.t * np.conj(f),  p.eps_N],
    ], dtype=complex)


def bands_along_path(frac_points, labels, p: MonolayerParams, spin: int, n_per_seg: int = 200):
    """Diagonalize along a k-path given by high-symmetry points in fractional (b1,b2) coords.

    Returns (x, energies, tick_pos, labels): x is cumulative |k| distance, energies is
    (n_k, 2) sorted ascending.
    """
    _, _, _, b1, b2 = lattice_geometry(p.a)
    bmat = np.vstack([b1, b2])
    kpts = [np.array(fp, float) @ bmat for fp in frac_points]   # cartesian k

    xs, evs, ticks = [], [], [0.0]
    x0 = 0.0
    for i in range(len(kpts) - 1):
        seg = np.linspace(kpts[i], kpts[i + 1], n_per_seg)
        seg_len = np.linalg.norm(kpts[i + 1] - kpts[i])
        for j, k in enumerate(seg):
            w = np.linalg.eigvalsh(bloch_hamiltonian(k, p, spin))
            xs.append(x0 + seg_len * j / (n_per_seg - 1))
            evs.append(np.sort(w.real))
        x0 += seg_len
        ticks.append(x0)
    return np.array(xs), np.array(evs), ticks, labels

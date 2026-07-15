"""Reduced multi-orbital Slater-Koster TB model of the h-CrN monolayer (out-of-plane manifold).

Orbitals near E_F only (the in-plane sigma manifold sits at -5.5 eV, irrelevant to transport):
    Cr (sublattice A): d_z2, d_xz, d_yz        N (sublattice B): p_z
Planar honeycomb, so bond direction cosines are (l, m, 0). The Slater-Koster selection rule at
n = 0 gives a clean structure (verified numerically in tests):
    * N p_z couples ONLY to Cr d_xz, d_yz via pd_pi  (elements l*pdpi, m*pdpi)
    * Cr d_z2 is NON-BONDING w.r.t. N p_z; it disperses only through Cr-Cr 2nd-neighbour hopping
      t_zz on the triangular Cr sublattice -> the flat band that rises to touch E_F.
On-site energies are referenced to E_F = 0 using Kuklin's DFT orbital energies (majority spin);
the minority channel is the same shifted up by the exchange splitting delta_ex (fit to the
3.9 eV gap). See crnte/kuklin_targets.py for the fit targets and the no-DFT decision in memory.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .monolayer import lattice_geometry


@dataclass(frozen=True)
class SKParams:
    a: float = 3.258        # lattice constant (Angstrom), Kuklin
    # NOTE: eps_pi is the BARE Cr d_xz/d_yz on-site; hybridization with p_z pushes the *bonding*
    # combination down to Kuklin's -4.4 eV peak and the *antibonding* up to touch E_F.
    eps_dz2: float = -2.3   # majority Cr d_z2 on-site (eV, rel. E_F); non-bonding flat band
    eps_pi: float = -2.6    # majority Cr (d_xz, d_yz) bare on-site (eV, rel. E_F)
    eps_pz: float = -3.2    # N p_z on-site (eV, rel. E_F)
    pdpi: float = 1.45      # Cr(d_xz,d_yz)-N(p_z) pd_pi hopping (eV)
    t_zz: float = 0.08      # Cr-Cr 2nd-neighbour d_z2 hopping (eV); small -> d_z2 stays flat
    delta_ex: float = 3.6   # Cr-d exchange splitting (eV); minority = majority + delta_ex

    def cr_shift(self, spin: int) -> float:
        """Exchange shift on Cr d: 0 for majority (+1), +delta_ex for minority (-1)."""
        return 0.0 if spin == +1 else self.delta_ex


def _second_neighbour_vectors(a1, a2):
    """The 6 Cr-Cr (same-sublattice) 2nd-neighbour vectors on the triangular sublattice."""
    return [a1, -a1, a2, -a2, a1 - a2, a2 - a1]


def build_H(k, p: SKParams, spin: int) -> np.ndarray:
    """4x4 Bloch Hamiltonian. Orbital order: [d_z2, d_xz, d_yz] (Cr), [p_z] (N)."""
    a1, a2, deltas, _, _ = lattice_geometry(p.a)
    d = p.a / np.sqrt(3.0)
    shift = p.cr_shift(spin)

    H = np.zeros((4, 4), dtype=complex)
    # on-site (Cr d shifted by exchange; N p_z unshifted)
    H[0, 0] = p.eps_dz2 + shift
    H[1, 1] = p.eps_pi + shift
    H[2, 2] = p.eps_pi + shift
    H[3, 3] = p.eps_pz

    # Cr-Cr 2nd-neighbour hopping disperses the non-bonding d_z2 band (triangular lattice)
    s2 = sum(np.exp(1j * np.dot(k, tau)) for tau in _second_neighbour_vectors(a1, a2))
    H[0, 0] += p.t_zz * s2.real

    # Cr-N nearest-neighbour pd_pi: p_z couples only to d_xz (l) and d_yz (m)
    f_xz = sum((dv[0] / d) * np.exp(1j * np.dot(k, dv)) for dv in deltas)  # sum l_delta * phase
    f_yz = sum((dv[1] / d) * np.exp(1j * np.dot(k, dv)) for dv in deltas)  # sum m_delta * phase
    H[1, 3] = p.pdpi * f_xz
    H[2, 3] = p.pdpi * f_yz
    H[3, 1] = np.conj(H[1, 3])
    H[3, 2] = np.conj(H[2, 3])
    return H


def bands_along_path(frac_points, p: SKParams, spin: int, n_per_seg: int = 200):
    """Diagonalize along a k-path (fractional b1,b2 coords). Returns (x, energies, ticks)."""
    _, _, _, b1, b2 = lattice_geometry(p.a)
    bmat = np.vstack([b1, b2])
    kpts = [np.array(fp, float) @ bmat for fp in frac_points]

    xs, evs, ticks, x0 = [], [], [0.0], 0.0
    for i in range(len(kpts) - 1):
        seg = np.linspace(kpts[i], kpts[i + 1], n_per_seg)
        seg_len = np.linalg.norm(kpts[i + 1] - kpts[i])
        for j, kk in enumerate(seg):
            w = np.linalg.eigvalsh(build_H(kk, p, spin))
            xs.append(x0 + seg_len * j / (n_per_seg - 1))
            evs.append(np.sort(w.real))
        x0 += seg_len
        ticks.append(x0)
    return np.array(xs), np.array(evs), ticks

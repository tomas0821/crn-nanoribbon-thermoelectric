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
    # --- effective majority conduction orbital c (Cr triangular sublattice) -----------------
    # Kuklin Fig. 2d (spin-up) shows a conduction band with an electron pocket at K (CBM at
    # -0.2 eV) rising to ~+0.6 eV at M and ~+2.4 eV at Gamma. The out-of-plane pd-pi manifold
    # cannot supply this band, so we add ONE effective Cr-sublattice orbital fitted directly to
    # the digitized dispersion (least squares, 1st-3rd neighbour hoppings; see
    # crnte/kuklin_targets.py CB1_DIGITIZED). It is symmetry-decoupled from N p_z in a planar
    # sheet (s- or d-like on Cr; Kuklin Fig. 3a puts Cr d_xy/d_x2-y2 + s weight above E_F).
    eps_c: float = 0.9147   # effective conduction orbital on-site (eV, rel. E_F, majority)
    t_c1: float = 0.2852    # c-c 1st-neighbour hopping (dist a) on the Cr triangular lattice
    t_c2: float = -0.0278   # c-c 2nd-neighbour hopping (dist sqrt(3) a)
    t_c3: float = 0.0297    # c-c 3rd-neighbour hopping (dist 2a)
    delta_c: float = 3.6    # exchange shift of c for the minority spin (assumed d-dominated)

    def cr_shift(self, spin: int) -> float:
        """Exchange shift on Cr d: 0 for majority (+1), +delta_ex for minority (-1)."""
        return 0.0 if spin == +1 else self.delta_ex

    def c_shift(self, spin: int) -> float:
        """Exchange shift on the effective conduction orbital c."""
        return 0.0 if spin == +1 else self.delta_c


def _second_neighbour_vectors(a1, a2):
    """The 6 Cr-Cr (same-sublattice) 2nd-neighbour vectors on the triangular sublattice."""
    return [a1, -a1, a2, -a2, a1 - a2, a2 - a1]


def cr_shells(a1, a2):
    """Cr-Cr shells on the triangular sublattice: (dist a, dist sqrt(3) a, dist 2a) vectors."""
    sh1 = [a1, -a1, a2, -a2, a1 - a2, a2 - a1]
    sh2 = [a1 + a2, -(a1 + a2), 2 * a1 - a2, -(2 * a1 - a2), 2 * a2 - a1, -(2 * a2 - a1)]
    sh3 = [2 * a1, -2 * a1, 2 * a2, -2 * a2, 2 * (a1 - a2), -2 * (a1 - a2)]
    return sh1, sh2, sh3


def build_H(k, p: SKParams, spin: int) -> np.ndarray:
    """5x5 Bloch Hamiltonian. Orbital order: [d_z2, d_xz, d_yz, c] (Cr), [p_z] (N).

    c is the effective majority conduction orbital (Cr triangular sublattice, electron pocket
    at K); it is symmetry-decoupled from N p_z in the planar sheet and carries its own
    1st-3rd-neighbour hoppings t_c1..t_c3.
    """
    a1, a2, deltas, _, _ = lattice_geometry(p.a)
    d = p.a / np.sqrt(3.0)
    shift = p.cr_shift(spin)
    sh1, sh2, sh3 = cr_shells(a1, a2)
    S = lambda sh: np.real(sum(np.exp(1j * np.dot(k, tau)) for tau in sh))

    H = np.zeros((5, 5), dtype=complex)
    # on-site (Cr d shifted by exchange; c by its own shift; N p_z unshifted)
    H[0, 0] = p.eps_dz2 + shift
    H[1, 1] = p.eps_pi + shift
    H[2, 2] = p.eps_pi + shift
    H[3, 3] = p.eps_c + p.c_shift(spin)
    H[4, 4] = p.eps_pz

    # Cr-Cr same-sublattice hoppings: d_z2 (1st shell only) and c (three shells)
    H[0, 0] += p.t_zz * S(sh1)
    H[3, 3] += p.t_c1 * S(sh1) + p.t_c2 * S(sh2) + p.t_c3 * S(sh3)

    # Cr-N nearest-neighbour pd_pi: p_z couples only to d_xz (l) and d_yz (m)
    f_xz = sum((dv[0] / d) * np.exp(1j * np.dot(k, dv)) for dv in deltas)  # sum l_delta * phase
    f_yz = sum((dv[1] / d) * np.exp(1j * np.dot(k, dv)) for dv in deltas)  # sum m_delta * phase
    H[1, 4] = p.pdpi * f_xz
    H[2, 4] = p.pdpi * f_yz
    H[4, 1] = np.conj(H[1, 4])
    H[4, 2] = np.conj(H[2, 4])
    return H


def build_H_dp(k, p: SKParams, spin: int) -> np.ndarray:
    """4x4 Bloch Hamiltonian of the d+p_z manifold ONLY (no effective c orbital).

    This is the original reduced manifold used by the mean-field magnetism module (crnte.scf):
    the c pocket holds only ~0.03 e/Cr and is neglected there. Orbital order:
    [d_z2, d_xz, d_yz] (Cr), [p_z] (N).
    """
    H5 = build_H(k, p, spin)
    idx = [0, 1, 2, 4]          # drop the c orbital (index 3)
    return H5[np.ix_(idx, idx)]


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

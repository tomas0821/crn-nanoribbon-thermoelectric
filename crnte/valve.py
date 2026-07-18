"""Spinful (noncollinear) CrN ribbon spin valve: domain-wall leakage of the OFF state.

The collinear antiparallel valve (crnte.ribbon_sk.build_spin_valve) has T = 0 exactly in the
half-metallic window because each spin species has no propagating states in one lead. A REAL
junction between oppositely magnetized segments hosts a domain wall of finite width, and a
noncollinear texture mixes the spin channels: carriers can rotate ("track") their spin with the
local exchange field and leak through. This module quantifies that leakage.

Model: the full spinful Hamiltonian, Cr sites carry 4 orbitals x 2 spins, N sites 1 x 2. The
local exchange field of magnitude Delta_orb = (Delta_ex on d, Delta_c on c, 0 on p_z) points
along the unit vector n(x) of a Walker wall profile,

    theta(x) = 2 arctan exp[(x - x0)/delta],   n = (sin theta, 0, cos theta),

which rotates from +z (left lead) to -z (right lead) over a wall of width lambda = pi * delta.
On-site term (spin (x) orbital blocks):  H = I_2 (x) E_orb + [(I_2 - n.sigma)/2] (x) D_orb,
which for n = +z reproduces the collinear convention (majority unshifted, minority + Delta).
All hoppings are spin diagonal. Leads are collinear (+z left, -z right), so the two spin
channels decouple in the leads and the total transmission is well defined.

The relevant length scale is the spin-mistracking length ell_mt ~ hbar v_F / Delta_ex
[Cabrera-Falicov / Waintal-Viret physics]: for walls wider than ell_mt the spin follows the
texture adiabatically and the wall becomes transparent. In a half-metal Delta_ex is huge, so
ell_mt ~ 1 Angstrom: only an atomically abrupt wall (or a nonmagnetic spacer) preserves the
OFF state.
"""
from __future__ import annotations

import kwant
import numpy as np

from .monolayer_sk import SKParams
from .ribbon_sk import _transverse_bound

_SQRT3 = np.sqrt(3.0)
_S0 = np.eye(2, dtype=complex)
_SX = np.array([[0, 1], [1, 0]], dtype=complex)
_SZ = np.array([[1, 0], [0, -1]], dtype=complex)


def _lattice_spinful(a: float):
    d = a / _SQRT3
    prim = [(a, 0.0), (a * 0.5, a * _SQRT3 / 2.0)]
    lat = kwant.lattice.general(prim, [(0.0, 0.0), (0.0, d)], norbs=[8, 2], name="crn_s")
    cr, nn = lat.sublattices
    return lat, cr, nn, d


def build_wall_valve(edge: str, width: int, p: SKParams, wall_delta: float,
                     length: int | None = None) -> kwant.system.FiniteSystem:
    """Two-terminal spinful ribbon with a Walker domain wall of parameter delta (Angstrom).

    wall width lambda = pi * wall_delta. wall_delta = 0 gives the abrupt (collinear) limit.
    ``length`` counts lead periods; default is enough to contain the wall plus margins.
    """
    a = p.a
    lat, cr, nn, d = _lattice_spinful(a)
    E_cr = np.diag([p.eps_dz2, p.eps_pi, p.eps_pi, p.eps_c]).astype(complex)
    D_cr = np.diag([p.delta_ex, p.delta_ex, p.delta_ex, p.delta_c]).astype(complex)
    E_n = np.array([[p.eps_pz]], dtype=complex)

    def theta_of(x, x0):
        if wall_delta <= 1e-9:
            return 0.0 if x < x0 else np.pi
        return 2.0 * np.arctan(np.exp((x - x0) / wall_delta))

    def cr_onsite(theta):
        proj = 0.5 * (_S0 - np.sin(theta) * _SX - np.cos(theta) * _SZ)   # (I - n.sigma)/2
        return np.kron(_S0, E_cr) + np.kron(proj, D_cr)

    n_onsite = np.kron(_S0, E_n)

    # spin-diagonal hoppings
    def hop_crn(site1, site2):
        if site1.family == cr:
            bond = site2.pos - site1.pos
            l, m = bond[0] / d, bond[1] / d
            blk = p.pdpi * np.array([[0.0], [l], [m], [0.0]], dtype=complex)
        else:
            bond = site1.pos - site2.pos
            l, m = bond[0] / d, bond[1] / d
            blk = p.pdpi * np.array([[0.0, l, m, 0.0]], dtype=complex)
        return np.kron(_S0, blk)

    crcr = [np.kron(_S0, np.diag(v).astype(complex)) for v in
            ([p.t_zz, 0, 0, p.t_c1], [0, 0, 0, p.t_c2], [0, 0, 0, p.t_c3])]
    SHELLS = ((crcr[0], ((1, 0), (0, 1), (1, -1))),
              (crcr[1], ((1, 1), (2, -1), (-1, 2))),
              (crcr[2], ((2, 0), (0, 2), (2, -2))))

    lo, hi = _transverse_bound(edge, width, a)
    if edge == "zigzag":
        axis, lc, period = np.array([2.0 * a, 0.0]), 0, 2.0 * a

        def in_width(pos):
            return lo <= pos[1] <= hi
    elif edge == "armchair":
        axis, lc, period = np.array([0.0, a * _SQRT3]), 1, a * _SQRT3

        def in_width(pos):
            return lo <= pos[0] <= hi
    else:
        raise ValueError(edge)

    if length is None:
        # wall (extends ~ +/- 4 delta) plus two lead periods of margin on each side
        length = max(4, int(np.ceil((8.0 * wall_delta + 4.0 * period) / period)))
    L = length * period
    x0 = 0.5 * L

    def scat_shape(pos):
        return in_width(pos) and 0.0 <= pos[lc] < L

    def onsite(site):
        if site.family != cr:
            return n_onsite
        return cr_onsite(theta_of(site.pos[lc], x0))

    syst = kwant.Builder()
    syst[lat.shape(scat_shape, (0.0, 0.0))] = onsite
    syst[lat.neighbors(1)] = hop_crn
    for mat, kinds in SHELLS:
        for delta in kinds:
            syst[kwant.builder.HoppingKind(delta, cr, cr)] = mat

    def make_lead(theta):
        sym = kwant.TranslationalSymmetry(axis)
        if edge == "armchair":
            sym.add_site_family(cr, other_vectors=[(1, 0)])
            sym.add_site_family(nn, other_vectors=[(1, 0)])
        lead = kwant.Builder(sym)
        lead[lat.shape(in_width, (0.0, 0.0))] = (lambda site, t=theta:
                                                 cr_onsite(t) if site.family == cr else n_onsite)
        lead[lat.neighbors(1)] = hop_crn
        for mat, kinds in SHELLS:
            for delta in kinds:
                lead[kwant.builder.HoppingKind(delta, cr, cr)] = mat
        return lead

    # Kwant attaches a lead on the side its symmetry vector points toward: reverse the
    # theta=0 lead so it sits on the LEFT (where the wall profile starts at theta ~ 0).
    syst.attach_lead(make_lead(0.0).reversed())
    syst.attach_lead(make_lead(np.pi))
    return syst.finalized()


def wall_transmission(edge: str, width: int, p: SKParams, wall_delta: float, energies):
    """Total (spin-summed) transmission through the wall at the given energies."""
    syst = build_wall_valve(edge, width, p, wall_delta)
    out = np.empty(len(energies))
    for i, E in enumerate(energies):
        for nudge in (0.0, 1e-6, -1e-6, 1e-5):
            try:
                s = kwant.smatrix(syst, energy=float(E) + nudge)
                t = s.transmission(1, 0)
                n_open = len(s.lead_info[0].momenta) / 2
                if np.isfinite(t) and -1e-6 <= t <= n_open + 1e-6:
                    out[i] = t
                    break
            except RuntimeError:
                continue
        else:
            out[i] = np.nan
    return out

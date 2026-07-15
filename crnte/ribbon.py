"""Kwant construction of hexagonal CrN nanoribbons + Landauer transmission.

Uses the same provisional effective honeycomb model as crnte.monolayer (Cr and N on the two
sublattices, spin-split Cr on-site, single NN hopping t). Cr = sublattice 'a', N = 'b'.
Edge type ('zigzag' | 'armchair') and width N (number of Cr+N atom rows across) select the
ribbon. Leads are the same pristine ribbon, so T(E) counts propagating modes per spin.
"""
from __future__ import annotations

import kwant
import numpy as np

from .monolayer import MonolayerParams

# Kwant honeycomb: prim_vecs = a*[(1,0),(1/2,sqrt3/2)], sublattices a=(0,0), b=(0, a/sqrt3).
_SQRT3 = np.sqrt(3.0)


def _lattice(a: float):
    lat = kwant.lattice.honeycomb(a, norbs=1, name="crn")
    return lat, lat.sublattices  # (Cr=a, N=b)


def _onsite(sublat_is_Cr: bool, p: MonolayerParams, spin: int) -> float:
    """On-site energy, shifted so E_F = 0. spin = +1 majority / -1 minority."""
    e = p.onsite_Cr(spin) if sublat_is_Cr else p.eps_N
    return e - p.E_fermi


def build_ribbon(edge: str, width: int, p: MonolayerParams, spin: int,
                 length: int = 2) -> kwant.system.FiniteSystem:
    """Finalized two-lead pristine ribbon. width = # atom rows across, length = # cells long."""
    a = p.a
    lat, (cr, nn) = _lattice(a)
    d = a / _SQRT3  # bond length

    if edge == "zigzag":
        # ribbon axis along x; transverse = y. Symmetry vector = prim_vec (1,0)*a.
        axis = np.array([a, 0.0])
        W = width * (d * 1.5) / 2.0 + d * 0.3   # half-width bound in y
        def in_width(pos):
            return -W <= pos[1] <= W
    elif edge == "armchair":
        # ribbon axis along y; transverse = x.
        axis = np.array([0.0, a * _SQRT3])
        W = width * (d * _SQRT3 / 2.0) / 2.0 + d * 0.3
        def in_width(pos):
            return -W <= pos[0] <= W
    else:
        raise ValueError(f"edge must be 'zigzag' or 'armchair', got {edge!r}")

    def onsite(site):
        return _onsite(site.family == cr, p, spin)

    # --- scattering region: a finite chunk of the ribbon ---
    syst = kwant.Builder()

    def scat_shape(pos):
        if edge == "zigzag":
            return in_width(pos) and 0.0 <= pos[0] < length * a
        return in_width(pos) and 0.0 <= pos[1] < length * a * _SQRT3

    syst[lat.shape(scat_shape, (0.0, 0.0))] = onsite
    syst[lat.neighbors()] = p.t

    # --- leads: translationally invariant ribbon along the axis ---
    sym = kwant.TranslationalSymmetry(axis)
    if edge == "armchair":
        # axis (0, sqrt3*a) = -pv0 + 2*pv1 = (-1, 2) is non-primitive; give a linearly
        # independent auxiliary vector so Kwant can define the fundamental domain.
        sym.add_site_family(cr, other_vectors=[(1, 0)])
        sym.add_site_family(nn, other_vectors=[(1, 0)])
    lead = kwant.Builder(sym)

    def lead_shape(pos):
        return in_width(pos)

    lead[lat.shape(lead_shape, (0.0, 0.0))] = onsite
    lead[lat.neighbors()] = p.t

    syst.attach_lead(lead)
    syst.attach_lead(lead.reversed())
    return syst.finalized()


def transmission(syst, energies) -> np.ndarray:
    """T(E) from lead 0 to lead 1 over an array of energies (relative to E_F).

    Kwant's mode solver fails when an energy lands exactly on a flat band / band edge; on that
    RuntimeError we nudge the energy by a tiny offset and retry (physically negligible shift).
    """
    out = np.empty(len(energies))
    for i, e in enumerate(energies):
        for nudge in (0.0, 1e-6, -1e-6, 1e-5, -1e-5, 1e-4):
            try:
                s = kwant.smatrix(syst, energy=float(e) + nudge)
                out[i] = s.transmission(1, 0)
                break
            except RuntimeError:
                continue
        else:
            out[i] = np.nan
    return out

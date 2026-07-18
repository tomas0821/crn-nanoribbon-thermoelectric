"""Kwant construction of hexagonal CrN nanoribbons on the FITTED reduced SK model.

Multi-orbital: Cr sites carry 3 orbitals (d_z2, d_xz, d_yz), N sites carry 1 (p_z), so on-sites
and hoppings are matrices. The Cr-N nearest-neighbour hopping is the direction-dependent
Slater-Koster pd_pi matrix (p_z couples only to d_xz, d_yz); Cr-Cr 2nd-neighbour hopping carries
the d_z2 t_zz term. Consistency with crnte.monolayer_sk.build_H is checked in tests.
"""
from __future__ import annotations

import kwant
import numpy as np

from .monolayer_sk import SKParams
from .ribbon import transmission  # model-agnostic T(E) helper (energy-nudge on flat bands)

__all__ = ["build_ribbon_sk", "transmission"]

_SQRT3 = np.sqrt(3.0)


def _lattice(a: float):
    # kwant honeycomb convention so the ribbon symmetry axes are lattice vectors:
    #   prim vecs pv0=(a,0), pv1=(a/2, a*sqrt3/2); Cr=(0,0), N=(0, a/sqrt3).
    # SK hoppings use actual site.pos, so they are correct regardless of this choice.
    d = a / _SQRT3
    prim = [(a, 0.0), (a * 0.5, a * _SQRT3 / 2.0)]
    lat = kwant.lattice.general(prim, [(0.0, 0.0), (0.0, d)], norbs=[4, 1], name="crn")
    cr, nn = lat.sublattices  # Cr (4 orb: d_z2, d_xz, d_yz, c), N (1 orb: p_z)
    return lat, cr, nn, d


def _transverse_bound(edge: str, N: int, a: float):
    """Transverse (lo, hi) bound that contains EXACTLY N atomic rows (Cr and N) across the ribbon.

    N is the number of Cr+N atomic rows across the non-periodic direction -- the DMRG-paper
    width convention. Rows are the distinct transverse coordinates of the honeycomb sites; we
    keep the N closest to the ribbon centre (a connected strip) and bound just outside them.
    """
    d = a / _SQRT3
    pv0 = np.array([a, 0.0])
    pv1 = np.array([a / 2.0, a * _SQRT3 / 2.0])
    tc = 1 if edge == "zigzag" else 0            # transverse coordinate: y (zigzag), x (armchair)
    R = 2 * N + 6
    coords = set()
    for n in range(-R, R + 1):
        for m in range(-R, R + 1):
            base = n * pv0 + m * pv1
            coords.add(round(base[tc], 4))               # Cr row
            coords.add(round(base[tc] + (0.0 if tc == 0 else d), 4))  # N row (offset (0,d))
    rows = np.array(sorted(coords))
    sel = np.sort(rows[np.argsort(np.abs(rows))[:N]])    # N rows closest to centre
    eps = 0.2 * d
    return sel[0] - eps, sel[-1] + eps


def build_ribbon_sk(edge: str, width: int, p: SKParams, spin: int,
                    length: int = 2, vacancy: float = 0.0, seed: int = 0
                    ) -> kwant.system.FiniteSystem:
    """Finalized two-lead CrN ribbon on the SK model. spin = +1 majority / -1 minority.

    ``width`` is N, the number of Cr+N atomic rows across the ribbon (DMRG-paper convention).
    vacancy: fraction (0..~0.3) of edge Cr sites removed from the SCATTERING region (leads stay
    pristine) to model edge disorder / vacancies. seed fixes the random removal.
    """
    a = p.a
    lat, cr, nn, d = _lattice(a)
    shift = p.cr_shift(spin)
    cshift = p.c_shift(spin)

    cr_onsite = np.diag([p.eps_dz2 + shift, p.eps_pi + shift, p.eps_pi + shift,
                         p.eps_c + cshift]).astype(complex)
    n_onsite = np.array([[p.eps_pz]], dtype=complex)
    # Cr-Cr same-sublattice hoppings by shell: d_z2 (t_zz) on shell 1; c on shells 1-3
    crcr1 = np.diag([p.t_zz, 0.0, 0.0, p.t_c1]).astype(complex)   # dist a
    crcr2 = np.diag([0.0, 0.0, 0.0, p.t_c2]).astype(complex)      # dist sqrt(3) a
    crcr3 = np.diag([0.0, 0.0, 0.0, p.t_c3]).astype(complex)      # dist 2a

    def onsite(site):
        return cr_onsite if site.family == cr else n_onsite

    def hop_crn(site1, site2):
        """<site1|H|site2> Slater-Koster pd_pi; p_z couples only to d_xz (l), d_yz (m)."""
        if site1.family == cr:                       # 4x1: <Cr | H | N p_z>
            bond = site2.pos - site1.pos             # Cr -> N
            l, m = bond[0] / d, bond[1] / d
            return p.pdpi * np.array([[0.0], [l], [m], [0.0]], dtype=complex)
        bond = site1.pos - site2.pos                 # site1 = N; Cr -> N direction
        l, m = bond[0] / d, bond[1] / d
        return p.pdpi * np.array([[0.0, l, m, 0.0]], dtype=complex)   # 1x4

    # --- geometry: axis + transverse bound holding exactly N (=width) atomic rows ---
    lo, hi = _transverse_bound(edge, width, a)
    if edge == "zigzag":
        # period 2a (two primitive cells): the c orbital's 2nd/3rd-shell hoppings reach up to
        # 2a along the transport direction and must connect only ADJACENT lead cells in Kwant.
        axis = np.array([2.0 * a, 0.0])

        def in_width(pos):
            return lo <= pos[1] <= hi

        def scat_shape(pos):
            # length counts LEAD periods (2a for zigzag, see axis above)
            return in_width(pos) and 0.0 <= pos[0] < length * 2.0 * a
    elif edge == "armchair":
        axis = np.array([0.0, a * _SQRT3])

        def in_width(pos):
            return lo <= pos[0] <= hi

        def scat_shape(pos):
            return in_width(pos) and 0.0 <= pos[1] < length * a * _SQRT3
    else:
        raise ValueError(f"edge must be 'zigzag' or 'armchair', got {edge!r}")

    # Cr-Cr HoppingKinds per shell (in units of the primitive vectors pv0, pv1)
    SHELLS = ((crcr1, ((1, 0), (0, 1), (1, -1))),          # dist a
              (crcr2, ((1, 1), (2, -1), (-1, 2))),         # dist sqrt(3) a
              (crcr3, ((2, 0), (0, 2), (2, -2))))          # dist 2a

    # --- scattering region ---
    syst = kwant.Builder()
    syst[lat.shape(scat_shape, (0.0, 0.0))] = onsite
    syst[lat.neighbors(1)] = hop_crn
    for mat, kinds in SHELLS:
        for delta in kinds:
            syst[kwant.builder.HoppingKind(delta, cr, cr)] = mat

    # --- optional edge vacancies in the scattering region ---
    if vacancy > 0.0:
        import random
        rng = random.Random(seed)
        tc = 1 if edge == "zigzag" else 0          # transverse coordinate index
        cr_sites = [s for s in syst.sites() if s.family == cr]
        coords = np.array([s.pos[tc] for s in cr_sites])
        cmax, cmin = coords.max(), coords.min()
        edge_sites = [s for s, c in zip(cr_sites, coords)
                      if abs(c - cmax) < 0.3 or abs(c - cmin) < 0.3]
        n_rem = int(round(vacancy * len(edge_sites)))
        for s in rng.sample(edge_sites, min(n_rem, len(edge_sites))):
            del syst[s]

    # --- lead: translationally invariant ribbon along the axis ---
    sym = kwant.TranslationalSymmetry(axis)
    if edge == "armchair":
        sym.add_site_family(cr, other_vectors=[(1, 0)])
        sym.add_site_family(nn, other_vectors=[(1, 0)])
    lead = kwant.Builder(sym)
    lead[lat.shape(in_width, (0.0, 0.0))] = onsite
    lead[lat.neighbors(1)] = hop_crn
    for mat, kinds in SHELLS:
        for delta in kinds:
            lead[kwant.builder.HoppingKind(delta, cr, cr)] = mat

    syst.attach_lead(lead)
    syst.attach_lead(lead.reversed())
    return syst.finalized()

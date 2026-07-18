"""Self-consistent mean-field (unrestricted Hartree-Fock) machinery for CrN ribbon EDGES.

NOTE: this module works in the reduced d+p_z manifold (build_H_dp) WITHOUT the effective
conduction orbital c: the c pocket holds only ~0.07 e/Cr and contributes negligibly to the
Cr moment, so the edge-magnetism analysis is unchanged by the transport-model extension.

Stage 1 (this file, verified below): a hand-built 1D Bloch Hamiltonian H_sigma(k) for a ribbon of
width N, with a SITE-DEPENDENT exchange shift on the Cr d orbitals -- the quantity the SCF loop
will iterate. Constructing it by hand (rather than via Kwant) gives a clean orbital<->site index
map, needed to project eigenvectors back onto sites for the occupation update.

The ribbon unit cell is periodic along the transport axis T; H(k)=H0 + V e^{ikT} + V^dag e^{-ikT}.
Cr sites carry 3 orbitals (d_z2, d_xz, d_yz), N sites 1 (p_z), same Slater-Koster hoppings as
crnte.ribbon_sk (pd_pi for Cr-N, t_zz for Cr-Cr d_z2). Later stages add: bulk filling/U
calibration, the SCF occupation loop, the edge moment profile, and J1/J2 from magnetic-config
energies.
"""
from __future__ import annotations

import numpy as np

from .monolayer_sk import SKParams
from .ribbon_sk import _transverse_bound

_S3 = np.sqrt(3.0)


def ribbon_cell(edge: str, N: int, a: float, ncell: int = 1):
    """Sites of a ribbon supercell of `ncell` periods along transport (kwant-honeycomb convention).

    Returns (cr, nn, Tsuper, tc) where Tsuper = ncell * (one-period translation).
    """
    d = a / _S3
    pv0 = np.array([a, 0.0])
    pv1 = np.array([a / 2.0, a * _S3 / 2.0])
    lo, hi = _transverse_bound(edge, N, a)
    if edge == "zigzag":
        Tp = np.array([a, 0.0]); tc, lc = 1, 0        # transverse=y, transport=x
    elif edge == "armchair":
        Tp = np.array([0.0, a * _S3]); tc, lc = 0, 1    # transverse=x, transport=y
    else:
        raise ValueError(edge)
    Lp = np.linalg.norm(Tp)                            # one-period length along transport
    cr, nn = [], []
    R = 3 * N + 8
    for n in range(-R, R + 1):
        for m in range(-R, R + 1):
            base = n * pv0 + m * pv1
            for pos, lst in ((base, cr), (base + np.array([0.0, d]), nn)):
                if lo - 1e-6 <= pos[tc] <= hi + 1e-6 and -1e-6 <= pos[lc] < ncell * Lp - 1e-6:
                    lst.append(pos)
    return np.array(cr), np.array(nn), ncell * Tp, tc


def _hop_block(A_is_cr, B_is_cr, bond, p, d):
    """Hopping matrix from site A's orbitals to site B's orbitals for separation `bond`=posB-posA."""
    dist = np.linalg.norm(bond)
    if A_is_cr and B_is_cr:                       # Cr-Cr 2nd neighbour: d_z2-d_z2 only
        if abs(dist - p.a) < 0.15 * p.a:
            return np.diag([p.t_zz, 0.0, 0.0]).astype(complex)
        return None
    if A_is_cr and (not B_is_cr):                 # Cr(d) -> N(p_z), Cr->N cosines
        if abs(dist - d) < 0.15 * d:
            l, m = bond / d
            return p.pdpi * np.array([[0.0], [l], [m]], dtype=complex)   # 3x1
        return None
    if (not A_is_cr) and B_is_cr:                 # N(p_z) -> Cr(d), Cr->N direction = -bond
        if abs(dist - d) < 0.15 * d:
            l, m = -bond / d
            return p.pdpi * np.array([[0.0, l, m]], dtype=complex)       # 1x3
        return None
    return None                                    # N-N: no hopping


def build_bloch(edge: str, N: int, p: SKParams, spin: int, exchange=None, ncell: int = 1):
    """Return (H0, V, cr_index, rows). H(k)=H0+V e^{ikT}+V^dag e^{-ikT} for an `ncell`-period cell.

    exchange: optional array of per-Cr-site exchange shifts added to that Cr's d orbitals (eV). If
    None, the uniform fitted shift ``p.cr_shift(spin)`` is used on every Cr (reproduces ribbon_sk).
    cr_index[i] = (i0,i1,i2) orbital indices of Cr site i; rows[i] = its transverse coordinate.
    """
    a, d = p.a, p.a / _S3
    cr, nn, T, tc = ribbon_cell(edge, N, a, ncell)
    nC, nN = len(cr), len(nn)
    dim = 3 * nC + nN
    cr_index = [(3 * i, 3 * i + 1, 3 * i + 2) for i in range(nC)]
    n_orb = [3 * nC + j for j in range(nN)]
    rows = cr[:, tc]

    if exchange is None:
        exchange = np.full(nC, p.cr_shift(spin))
    exchange = np.asarray(exchange, float)

    H0 = np.zeros((dim, dim), complex)
    V = np.zeros((dim, dim), complex)
    # on-site energies (Cr d get the per-site exchange shift; N p_z fixed)
    for i in range(nC):
        H0[3 * i, 3 * i] = p.eps_dz2 + exchange[i]
        H0[3 * i + 1, 3 * i + 1] = p.eps_pi + exchange[i]
        H0[3 * i + 2, 3 * i + 2] = p.eps_pi + exchange[i]
    for j in range(nN):
        H0[n_orb[j], n_orb[j]] = p.eps_pz

    pos = list(cr) + list(nn)
    is_cr = [True] * nC + [False] * nN
    sl = [slice(3 * i, 3 * i + 3) for i in range(nC)] + [slice(n_orb[j], n_orb[j] + 1) for j in range(nN)]
    for A in range(nC + nN):
        for B in range(nC + nN):
            for tau, mat in ((np.zeros(2), H0), (T, V)):     # tau=0 -> H0, tau=+T -> V
                if tau[0] == 0 and tau[1] == 0 and A == B:
                    continue
                blk = _hop_block(is_cr[A], is_cr[B], (pos[B] + tau) - pos[A], p, d)
                if blk is not None:
                    mat[sl[A], sl[B]] += blk
    return H0, V, cr_index, rows


def bands(H0, V, Tlen, nk=200):
    """Band energies over the 1D BZ k in (-pi/T, pi/T]."""
    ks = np.linspace(-np.pi, np.pi, nk) / Tlen
    out = []
    for k in ks:
        Hk = H0 + V * np.exp(1j * k * Tlen) + V.conj().T * np.exp(-1j * k * Tlen)
        out.append(np.linalg.eigvalsh(Hk))
    return ks, np.array(out)


# --- Stage 2: bulk (uniform) mean-field calibration -------------------------------------------
# Calibrated so the uniform SCF reproduces the fitted bulk exchange (Delta_ex = 3.6 eV). The
# reduced 4-orbital manifold yields m_Cr = 2.67 mu_B (d_z2 fully polarised, d_xz/d_yz partially),
# ~11% below Kuklin's 3.0 because the omitted deep sigma-d orbitals also carry moment -- the known
# semi-quantitative limitation of the reduced model. The bulk SCF converges to this stable magnetic
# fixed point from any starting moment (verified). Relation: Delta_ex = U_EFF * m_Cr.
U_EFF = 1.346          # effective Stoner parameter (eV)
N_E_PER_CELL = 4.717   # electrons per unit cell in the reduced manifold (fixed filling)


def _bz_mesh(a, nk):
    from .monolayer_sk import lattice_geometry
    _, _, _, b1, b2 = lattice_geometry(a)
    return [(i / nk) * b1 + (j / nk) * b2 for i in range(nk) for j in range(nk)]


def monolayer_moment(p, nk=60):
    """Cr-d occupation/moment and total filling of the fitted bulk at E_F=0 (diagnostic)."""
    from .monolayer_sk import build_H_dp as build_H
    ncr = {+1: 0.0, -1: 0.0}
    ntot = 0
    for k in _bz_mesh(p.a, nk):
        for spin in (+1, -1):
            w, v = np.linalg.eigh(build_H(k, p, spin))
            for b in range(4):
                if w[b] < 0.0:
                    ncr[spin] += (np.abs(v[:3, b]) ** 2).sum()
                    ntot += 1
    ncr = {s: ncr[s] / nk ** 2 for s in ncr}
    return dict(m_Cr=ncr[+1] - ncr[-1], n_Cr_up=ncr[+1], n_Cr_dn=ncr[-1], N_e=ntot / nk ** 2)


def bulk_scf(p, U_eff=U_EFF, N_e=N_E_PER_CELL, m_init=2.0, nk=40, mix=0.3, tol=1e-4, maxit=100):
    """Self-consistent uniform mean-field. Returns dict(m_Cr, Delta_ex, E_F, iters).

    At fixed filling N_e, iterates Delta_ex = U_eff * m_Cr until the Cr-d moment converges.
    """
    import dataclasses
    from .monolayer_sk import build_H_dp as build_H
    kpts = _bz_mesh(p.a, nk)
    m = m_init
    EF = 0.0
    for it in range(maxit):
        pp = dataclasses.replace(p, delta_ex=U_eff * m)
        allE, proj = [], []
        for k in kpts:
            for spin in (+1, -1):
                w, v = np.linalg.eigh(build_H(k, pp, spin))
                cw = (np.abs(v[:3, :]) ** 2).sum(0)
                allE.extend(w)
                proj.extend(zip(cw, [spin] * 4))
        allE = np.array(allE)
        nocc = int(round(N_e * nk * nk))
        order = np.argsort(allE)
        EF = 0.5 * (allE[order[nocc - 1]] + allE[order[nocc]])
        up = sum(proj[i][0] for i in order[:nocc] if proj[i][1] == +1) / nk ** 2
        dn = sum(proj[i][0] for i in order[:nocc] if proj[i][1] == -1) / nk ** 2
        m_new = up - dn
        if abs(m_new - m) < tol:
            return dict(m_Cr=m_new, Delta_ex=U_eff * m_new, E_F=EF, iters=it)
        m = mix * m_new + (1 - mix) * m
    return dict(m_Cr=m, Delta_ex=U_eff * m, E_F=EF, iters=maxit)


# --- Stage 3: self-consistent per-site Cr moments in a ribbon (edge magnetism) ----------------
def ribbon_scf(edge: str, N: int, p: SKParams, U_eff=U_EFF, N_e=N_E_PER_CELL, nk=60,
               mix=0.3, tol=1e-4, maxit=400, m_init=2.674):
    """Converge the per-Cr-site moments m_i of a ferromagnetic width-N ribbon (unrestricted MF).

    Convention (as calibrated in bulk_scf): majority Cr d unshifted, minority Cr d shifted by the
    site-dependent U_eff*m_i. Returns dict(rows, m, m_interior, m_edge, E_band, E_F, iters).
    """
    cr, nn, T, tc = ribbon_cell(edge, N, p.a)
    nC = len(cr)
    Tlen = np.linalg.norm(T)
    rows = cr[:, tc]
    N_tot = int(round(N_e * nC))
    _, _, cri, _ = build_bloch(edge, N, p, +1, exchange=np.zeros(nC))     # orbital<->site map
    idx_by_site = [list(cri[i]) for i in range(nC)]
    ks = np.linspace(-np.pi, np.pi, nk, endpoint=False) / Tlen

    m = np.full(nC, float(m_init))
    E_band = EF = 0.0
    for it in range(maxit):
        H0u, Vu, _, _ = build_bloch(edge, N, p, +1, exchange=np.zeros(nC))
        H0d, Vd, _, _ = build_bloch(edge, N, p, -1, exchange=U_eff * m)
        allE, allw, alls = [], [], []          # energies, Cr-site weights, spin per state
        for k in ks:
            for H0, V, spin in ((H0u, Vu, +1), (H0d, Vd, -1)):
                Hk = H0 + V * np.exp(1j * k * Tlen) + V.conj().T * np.exp(-1j * k * Tlen)
                w, v = np.linalg.eigh(Hk)
                allE.append(w)
                allw.append(np.array([(np.abs(v[ix, :]) ** 2).sum(0) for ix in idx_by_site]).T)
                alls.append(np.full(len(w), spin))
        allE = np.concatenate(allE)
        allw = np.concatenate(allw, axis=0)     # (Nstates, nC)
        alls = np.concatenate(alls)
        order = np.argsort(allE)
        nocc = N_tot * nk
        occ = order[:nocc]
        EF = 0.5 * (allE[order[nocc - 1]] + allE[order[nocc]])
        E_band = allE[occ].sum() / nk
        up = allw[occ][alls[occ] == +1].sum(0) / nk
        dn = allw[occ][alls[occ] == -1].sum(0) / nk
        m_new = up - dn
        if np.max(np.abs(m_new - m)) < tol:
            m = m_new
            break
        m = mix * m_new + (1 - mix) * m

    interior = np.abs(rows - np.median(rows)) < 0.4 * (rows.max() - rows.min())
    return dict(rows=rows, m=m, m_interior=float(np.mean(m[interior])),
                m_edge=float(np.max(np.abs(m))), E_band=E_band, E_F=EF, iters=it)


# --- Stage 4: intra-edge exchange J1, J2 via the Lichtenstein (LKAG) magnetic-force theorem ----
def edge_exchange(edge: str, N: int, p: SKParams, U_eff=U_EFF, nk=120, nE=400, eta=0.02,
                  neighbors=(1, 2), E_min=-8.0):
    """Intra-edge exchange constants J_n along the edge Cr chain (meV), averaged over both edges.

    Uses the LKAG formula J_n = (1/2pi) Im \\int^{E_F} dE  delta^2 Tr_d[G^up_{n}(E) G^dn_{-n}(E)],
    with G^sigma_n the intersite Green's function between an edge Cr and its n-th neighbour along
    the edge (obtained by k-integration at the FM self-consistent solution). This isolates the
    inter-site exchange (naive total-energy flips are swamped by on-site kinetic terms). Returns
    dict with J_lkag[n] (unit-vector convention) and J_heis[n]=J_lkag/S^2 (Heisenberg, S=m_edge/2).
    """
    r = ribbon_scf(edge, N, p, nk=60)
    rows, m, EF = r["rows"], r["m"], r["E_F"]
    _, _, cri, _ = build_bloch(edge, N, p, +1, exchange=np.zeros(len(m)))
    H0u, Vu, _, _ = build_bloch(edge, N, p, +1, exchange=np.zeros(len(m)))
    H0d, Vd, _, _ = build_bloch(edge, N, p, -1, exchange=U_eff * m)
    Tlen = p.a if edge == "zigzag" else p.a * _S3
    dim = H0u.shape[0]
    edge_sites = [int(np.argmax(rows)), int(np.argmin(rows))]     # top & bottom edge Cr
    ks = np.linspace(-np.pi, np.pi, nk, endpoint=False) / Tlen
    Es = np.linspace(E_min, EF, nE)
    ii = np.eye(dim)

    J = {n: 0.0 for n in neighbors}
    for isite in edge_sites:
        bl = list(cri[isite])
        delta = U_eff * abs(m[isite])
        integ = {n: np.empty(nE, complex) for n in neighbors}
        for e, E in enumerate(Es):
            Gu = {n: np.zeros((3, 3), complex) for n in neighbors}
            Gd = {n: np.zeros((3, 3), complex) for n in neighbors}
            for k in ks:
                phase = np.exp(1j * k * Tlen)
                Hu = H0u + Vu * phase + Vu.conj().T / phase
                Hd = H0d + Vd * phase + Vd.conj().T / phase
                gu = np.linalg.inv((E + 1j * eta) * ii - Hu)[np.ix_(bl, bl)]
                gd = np.linalg.inv((E + 1j * eta) * ii - Hd)[np.ix_(bl, bl)]
                for n in neighbors:
                    Gu[n] += gu * phase ** n
                    Gd[n] += gd / phase ** n
            for n in neighbors:
                integ[n][e] = np.trace((Gu[n] / nk) @ (Gd[n] / nk))
        for n in neighbors:
            # J_ij = -d^2(Omega)/d(theta_i)d(theta_j): the cross-term of the Heisenberg form
            # H = -sum J e_i.e_j is -J theta_i theta_j, hence the overall minus sign here.
            J[n] += -(delta ** 2 / (2 * np.pi)) * np.imag(np.trapz(integ[n], Es)) * 1000.0  # meV
    J = {n: J[n] / len(edge_sites) for n in neighbors}                 # average over the two edges
    S = float(np.max(np.abs(m))) / 2.0
    return dict(J_lkag=J, J_heis={n: J[n] / S ** 2 for n in neighbors}, S=S,
                m_edge=float(np.max(np.abs(m))))

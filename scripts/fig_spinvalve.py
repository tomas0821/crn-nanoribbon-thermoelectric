#!/usr/bin/env python
"""Thermal spin valve: parallel vs antiparallel lead magnetizations (zigzag N=14).

(a) Total transmission T(E) for the parallel (P) and antiparallel (AP) configurations. In the
    AP case each spin species is majority in one lead and inside the minority gap in the other,
    so there are NO propagating states to transmit into: T_AP(E) = 0 identically across the
    whole half-metallic window [-3.2, +1.0] eV -- an exact lead-spectrum effect, independent of
    the domain-wall details. (Above the minority edge the model's effective conduction orbital
    is symmetry-decoupled from the pi* manifold, so the computed AP onset there is not
    quantitative; we therefore only claim the OFF window.)
(b) The resulting switch: G(mu) and thermocurrent on/off behaviour at 300 K.

Also estimates the inter-edge magnetic coupling (parallel vs antiparallel EDGE moments) with a
spin-symmetric mean-field convention, to assess whether both configurations are accessible.

Run:  ~/venvs/crn-te/bin/python scripts/fig_spinvalve.py
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from crnte import thermo as th  # noqa: E402
from crnte.monolayer_sk import SKParams  # noqa: E402
from crnte.ribbon_sk import build_spin_valve, transmission  # noqa: E402

FIGDIR, DATADIR = os.path.join(ROOT, "figures"), os.path.join(ROOT, "data")
E_GRID = np.linspace(-1.2, 1.0, 441)      # dE = 5 meV, within the exact OFF window
CACHE = os.path.join(DATADIR, "zigzag_N14_valve.npz")


def get_ap():
    if os.path.exists(CACHE):
        d = np.load(CACHE)
        return d["E"], d["T_up"], d["T_dn"]
    p = SKParams()
    Tu = transmission(build_spin_valve("zigzag", 14, p, +1), E_GRID)
    Td = transmission(build_spin_valve("zigzag", 14, p, -1), E_GRID)
    np.savez(CACHE, E=E_GRID, T_up=Tu, T_dn=Td)
    return E_GRID, Tu, Td


def interedge_energetics(edge="zigzag", N=8, nk=40, maxit=200, tol=1e-4, mix=0.3):
    """Mean-field energy difference (AP - P edge moments), spin-symmetric convention.

    Both configurations are converged with the SAME convention (shift_sigma(i) =
    (U/2)(m_ref - sigma m_i), which reduces to the calibrated FM convention for m_i = m_ref),
    and compared via E_tot = E_band - U sum_i n_up,i n_dn,i (mean-field double counting).
    Returns dict(dE_per_edge_Cr_meV, converged_AP, m_edge_AP).
    """
    from crnte import scf as S
    p = SKParams()
    cr, nn, T, tc = S.ribbon_cell(edge, N, p.a)
    nC = len(cr)
    Tlen = np.linalg.norm(T)
    rows = cr[:, tc]
    N_tot = int(round(S.N_E_PER_CELL * nC))
    _, _, cri, _ = S.build_bloch(edge, N, p, +1, exchange=np.zeros(nC))
    idx_by_site = [list(cri[i]) for i in range(nC)]
    ks = np.linspace(-np.pi, np.pi, nk, endpoint=False) / Tlen
    m_ref = 2.674

    def converge(m0):
        m = np.array(m0, float)
        for it in range(maxit):
            sh_u = 0.5 * S.U_EFF * (m_ref - m)
            sh_d = 0.5 * S.U_EFF * (m_ref + m)
            # build_bloch's ``exchange`` argument is the TOTAL per-site Cr shift for that spin
            H0u, Vu, _, _ = S.build_bloch(edge, N, p, +1, exchange=sh_u)
            H0d, Vd, _, _ = S.build_bloch(edge, N, p, -1, exchange=sh_d)
            allE, allw, alls = [], [], []
            for k in ks:
                for H0, V, sp in ((H0u, Vu, +1), (H0d, Vd, -1)):
                    Hk = H0 + V * np.exp(1j * k * Tlen) + V.conj().T * np.exp(-1j * k * Tlen)
                    w, v = np.linalg.eigh(Hk)
                    allE.append(w)
                    allw.append(np.array([(np.abs(v[ix, :]) ** 2).sum(0)
                                          for ix in idx_by_site]).T)
                    alls.append(np.full(len(w), sp))
            allE = np.concatenate(allE)
            allw = np.concatenate(allw, axis=0)
            alls = np.concatenate(alls)
            order = np.argsort(allE)
            occ = order[:N_tot * nk]
            E_band = allE[occ].sum() / nk
            up = allw[occ][alls[occ] == +1].sum(0) / nk
            dn = allw[occ][alls[occ] == -1].sum(0) / nk
            m_new = up - dn
            if np.max(np.abs(m_new - m)) < tol:
                m = m_new
                break
            m = mix * m_new + (1 - mix) * m
        E_tot = E_band - S.U_EFF * float(np.sum(up * dn))
        return m, E_tot, it

    mP, EP, itP = converge(np.full(nC, m_ref))
    ap0 = np.where(rows > np.median(rows), -m_ref, m_ref)
    mAP, EAP, itAP = converge(ap0)
    n_edge = 2  # edge Cr atoms per period cell (one per edge)
    stayed_ap = bool(np.min(mAP) < -1.0)
    return dict(dE_meV=1000.0 * (EAP - EP) / n_edge, converged_AP=stayed_ap,
                m_edge_AP=float(np.max(np.abs(mAP))), itP=itP, itAP=itAP)


def main():
    p = SKParams()
    d = np.load(os.path.join(DATADIR, "zigzag_N14_TE.npz"))
    E_ap, Tu_ap, Td_ap = get_ap()

    fig, axs = plt.subplots(1, 2, figsize=(9.6, 3.8))
    mask = (d["E"] >= -1.2) & (d["E"] <= 1.0)
    axs[0].plot(d["E"][mask], (d["T_up"] + d["T_dn"])[mask], color="C0", lw=1.8,
                label="parallel (P)")
    axs[0].plot(E_ap, Tu_ap + Td_ap, color="C3", lw=2.2, ls="--", label="antiparallel (AP)")
    axs[0].axvline(0, color="0.7", lw=0.6, ls=":")
    axs[0].set_xlabel(r"$E - E_F$ (eV)")
    axs[0].set_ylabel(r"total transmission $T_\uparrow + T_\downarrow$")
    axs[0].set_title("(a) P vs AP lead magnetizations (zigzag N=14)")
    axs[0].legend(frameon=False, fontsize=9)

    mu = np.linspace(-0.6, 0.9, 301)
    up = th.sweep_mu(d["E"], d["T_up"], mu, 300.0)
    dn = th.sweep_mu(d["E"], d["T_dn"], mu, 300.0)
    G_P = (up["G"] + dn["G"]) / 3.874e-5
    axs[1].plot(mu, G_P, color="C0", lw=1.8, label=r"$G_{\rm P}$")
    axs[1].plot(mu, np.zeros_like(mu), color="C3", lw=2.2, ls="--", label=r"$G_{\rm AP}=0$")
    axs[1].set_xlabel(r"$\mu - E_F$ (eV)")
    axs[1].set_ylabel(r"$G$ $(e^2/h)$, 300 K")
    axs[1].set_title("(b) conductance switch")
    axs[1].legend(frameon=False, fontsize=9)
    axs[1].axvline(0, color="0.7", lw=0.6, ls=":")

    fig.tight_layout()
    out = os.path.join(FIGDIR, "fig_spinvalve.png")
    fig.savefig(out, dpi=200)
    print(f"max |T_AP| on the grid: {max(np.max(np.abs(Tu_ap)), np.max(np.abs(Td_ap))):.2e}")
    print(f"G_P at E_F (300 K): {G_P[np.argmin(np.abs(mu))]:.2f} e^2/h")
    print(f"wrote {out}")

    r = interedge_energetics()
    print(f"inter-edge energetics (zigzag N=8): dE(AP-P) = {r['dE_meV']:+.2f} meV per edge Cr, "
          f"AP self-consistent: {r['converged_AP']} (m_edge_AP={r['m_edge_AP']:.2f}), "
          f"iters P/AP = {r['itP']}/{r['itAP']}")
    print("NOTE: this rigid-shift mean-field energy difference has no charge self-consistency")
    print("and is NOT quantitatively reliable; it is recorded here but NOT used in the paper.")
    with open(os.path.join(DATADIR, "spinvalve.txt"), "w") as fh:
        fh.write(f"max|T_AP| = {max(np.max(np.abs(Tu_ap)), np.max(np.abs(Td_ap))):.2e}\n")
        fh.write(f"interedge dE(AP-P) per edge Cr [meV] = {r['dE_meV']:+.3f} "
                 f"(AP stable: {r['converged_AP']}, m_edge_AP {r['m_edge_AP']:.3f})\n")
        fh.write("CAVEAT: rigid-shift MF total-energy difference without charge\n"
                 "self-consistency -- not reliable; not quoted in the manuscript.\n")


if __name__ == "__main__":
    main()

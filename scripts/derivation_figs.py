#!/usr/bin/env python
"""Figures for the derivations companion (derivations/figs/).

figD1_geometry.png   - real-space honeycomb with bond vectors and the three Cr-Cr shells
                       entering S_1, S_2, S_3; reciprocal lattice / BZ with the k-path.
figD2_fermiwindow.png- the Onsager weights (-df/dE)(E-mu)^n at 300 K.
figD3_phonon.png     - the six constructed phonon branches (anchors + ZA crossover) and the
                       ribbon mode count M(nu) for W = 18.6 A.
figD4_wall.png       - Walker wall profile theta(x), texture arrows, scattering region.

Run:  ~/venvs/crn-te/bin/python scripts/derivation_figs.py
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from crnte import phonon as ph  # noqa: E402

OUT = os.path.join(ROOT, "derivations", "figs")
os.makedirs(OUT, exist_ok=True)

A = 3.258
D = A / np.sqrt(3.0)
A1 = D * np.array([1.5, np.sqrt(3.0) / 2])
A2 = D * np.array([1.5, -np.sqrt(3.0) / 2])
DELTAS = [D * np.array([1.0, 0.0]),
          D * np.array([-0.5, np.sqrt(3.0) / 2]),
          D * np.array([-0.5, -np.sqrt(3.0) / 2])]


def fig_geometry():
    fig, axs = plt.subplots(1, 2, figsize=(10.2, 4.6))

    # (a) real space + shells
    ax = axs[0]
    cr, nn = [], []
    for n in range(-4, 5):
        for m in range(-4, 5):
            base = n * A1 + m * A2
            cr.append(base)
            nn.append(base + DELTAS[0])
    cr, nn = np.array(cr), np.array(nn)
    lim = 2.05 * A
    for p in cr:
        for dv in DELTAS:
            q = p + dv
            if np.linalg.norm(p) < lim + 2 and np.linalg.norm(q) < lim + 2:
                ax.plot([p[0], q[0]], [p[1], q[1]], color="0.75", lw=1.0, zorder=1)
    m_cr = np.linalg.norm(cr, axis=1) < lim
    m_nn = np.linalg.norm(nn, axis=1) < lim
    ax.scatter(cr[m_cr, 0], cr[m_cr, 1], s=90, color="#3b6fb0", ec="k", lw=0.6, zorder=3)
    ax.scatter(nn[m_nn, 0], nn[m_nn, 1], s=55, color="#c7ccd1", ec="k", lw=0.6, zorder=3)
    for dv, lab in zip(DELTAS, [r"$\delta_1$", r"$\delta_2$", r"$\delta_3$"]):
        ax.annotate("", xy=dv, xytext=(0, 0),
                    arrowprops=dict(arrowstyle="-|>", color="C3", lw=1.8), zorder=5)
        ax.text(*(dv * 1.28 + np.array([0.05, 0.0])), lab, color="C3", fontsize=12,
                ha="center", va="center")
    # Cr-Cr shells around the origin: radii a, sqrt3 a, 2a
    shells = [(A, "C2", r"shell 1: $|\tau|=a$ ($S_1$, $t_{zz},t_{c1}$)"),
              (np.sqrt(3) * A, "C1", r"shell 2: $|\tau|=\sqrt{3}a$ ($S_2$, $t_{c2}$)"),
              (2 * A, "C4", r"shell 3: $|\tau|=2a$ ($S_3$, $t_{c3}$)")]
    th = np.linspace(0, 2 * np.pi, 200)
    for r, c, lab in shells:
        ax.plot(r * np.cos(th), r * np.sin(th), ls="--", color=c, lw=1.4, label=lab)
    # mark the six shell-1 sites explicitly
    for tau in (A1, A2, A1 - A2, -A1, -A2, A2 - A1):
        ax.plot(*tau, marker="o", ms=13, mfc="none", mec="C2", mew=1.6, zorder=4)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    ax.set_title("(a) real space: bonds and Cr–Cr shells")
    ax.set_xlim(-2.3 * A, 2.3 * A); ax.set_ylim(-1.55 * A, 1.75 * A)
    ax.set_aspect("equal"); ax.axis("off")

    # (b) reciprocal space
    ax = axs[1]
    B1 = (2 * np.pi / (3 * D)) * np.array([1.0, np.sqrt(3.0)])
    B2 = (2 * np.pi / (3 * D)) * np.array([1.0, -np.sqrt(3.0)])
    K = (B1 - B2) / 3.0
    hexpts = [np.array([[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]]) @ K
              for t in np.linspace(0, 2 * np.pi, 7)[:-1]]
    hexpts.append(hexpts[0])
    hexpts = np.array(hexpts)
    ax.plot(hexpts[:, 0], hexpts[:, 1], color="k", lw=1.4)
    for v, lab in ((B1, r"$\mathbf{b}_1$"), (B2, r"$\mathbf{b}_2$")):
        ax.annotate("", xy=v, xytext=(0, 0),
                    arrowprops=dict(arrowstyle="-|>", color="C3", lw=1.6))
        ax.text(*(v * 1.09), lab, color="C3", fontsize=12, ha="center")
    M = (B1 + B2) / 2.0
    path = np.array([[0, 0], M, K, [0, 0]])
    ax.plot(path[:, 0], path[:, 1], color="C0", lw=2.0)
    for p, lab, off in (((0, 0), r"$\Gamma$", (-0.16, -0.12)), (M, "M", (0.08, 0.02)),
                        (K, "K", (0.06, 0.08))):
        ax.plot(*p, "ko", ms=5)
        ax.text(p[0] + off[0], p[1] + off[1], lab, fontsize=13)
    ax.set_title(r"(b) Brillouin zone and the $\Gamma$–M–K–$\Gamma$ path")
    ax.set_aspect("equal"); ax.axis("off")
    r = 1.35 * np.linalg.norm(B1)
    ax.set_xlim(-0.55 * r, 0.85 * r); ax.set_ylim(-0.75 * r, 0.75 * r)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "figD1_geometry.png"), dpi=200)
    print("wrote figD1_geometry.png")


def fig_fermiwindow():
    kT = 8.617e-5 * 300.0
    E = np.linspace(-0.30, 0.30, 1201)
    w = 1.0 / (4 * kT * np.cosh(E / (2 * kT)) ** 2)
    fig, ax = plt.subplots(figsize=(6.4, 3.9))
    ax.plot(E, w / w.max(), color="C0", lw=1.9,
            label=r"$(-\partial f/\partial E)$  ($\to \mathcal{L}_0$)")
    w1 = E * w
    ax.plot(E, w1 / np.abs(w1).max(), color="C3", lw=1.9,
            label=r"$(E-\mu)\,(-\partial f/\partial E)$  ($\to \mathcal{L}_1$, odd)")
    w2 = E * E * w
    ax.plot(E, w2 / w2.max(), color="C2", lw=1.9,
            label=r"$(E-\mu)^2(-\partial f/\partial E)$  ($\to \mathcal{L}_2$)")
    ax.axhline(0, color="k", lw=0.6)
    ax.axvline(0, color="0.8", lw=0.7, ls=":")
    for x in (-5 * kT, 5 * kT):
        ax.axvline(x, color="0.6", lw=0.8, ls="--")
    ax.text(5 * kT * 1.05, 0.82, r"$\pm 5k_BT$" + f"\n({5*kT*1e3:.0f} meV at 300 K)",
            fontsize=9, color="0.35")
    ax.set_xlabel(r"$E-\mu$ (eV)")
    ax.set_ylabel("weight (normalised)")
    ax.legend(frameon=False, fontsize=9, loc="upper left")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "figD2_fermiwindow.png"), dpi=200)
    print("wrote figD2_fermiwindow.png")


def fig_phonon():
    q = np.linspace(0, ph.Q_ZONE, 400)
    fig, axs = plt.subplots(1, 2, figsize=(10.6, 4.4))
    ax = axs[0]
    ax.plot(q, ph._nu_za(q), color="C0", lw=2.0, label=f"ZA (max {ph.ZA_MAX} THz)")
    quad = ph.ZA_ALPHA * q * q
    mq = quad < 7.0                       # clip the guide so it doesn't wreck the scale
    ax.plot(q[mq], quad[mq], color="C0", lw=1.0, ls=":",
            label=r"ZA quadratic $\alpha q^2$ ($\alpha=44$ THz $\mathrm{\AA}^2$)")
    ax.plot(q, ph._nu_sine(q, ph.TA_MAX), color="C2", lw=2.0, label=f"TA (max {ph.TA_MAX})")
    ax.plot(q, ph._nu_sine(q, ph.LA_MAX), color="C3", lw=2.0, label=f"LA (max {ph.LA_MAX})")
    for (nG, nZ), c in zip(ph.OPTICAL, ("C4", "C5", "C6")):
        ax.plot(q, nG - (nG - nZ) * np.sin(0.5 * np.pi * q / ph.Q_ZONE), color=c, lw=1.7,
                label=f"optical {nG}$\\to${nZ}")
        ax.plot([0, ph.Q_ZONE], [nG, nZ], "o", color=c, ms=4)
    for v_kms in (8.5, 4.3):
        # nu [THz] = v q / 2pi with v in km/s = 10 THz*Angstrom: slope = 10 v / 2pi THz A
        qq = q[q < 0.35]
        ax.plot(qq, (10.0 * v_kms / (2 * np.pi)) * qq, color="0.4", lw=0.9, ls="--")
    ax.text(0.36, 2.2, r"digitized slopes $v_{\rm LA},v_{\rm TA}$", fontsize=8, color="0.35")
    ax.set_xlabel(r"$q$ ($\mathrm{\AA}^{-1}$)  (isotropic; $q_{\rm ZB}=1.20$)")
    ax.set_ylabel(r"$\nu$ (THz)")
    ax.set_ylim(0, 18.2)
    ax.set_title("(a) constructed branches (anchors as dots)")
    ax.legend(frameon=False, fontsize=7.2, ncol=3, loc="upper center",
              bbox_to_anchor=(0.5, -0.18))

    ax = axs[1]
    nus = np.linspace(0.01, 17.5, 600)
    W = 18.6
    Ms = [ph.modes(nu, W) for nu in nus]
    ax.plot(nus, Ms, color="C0", lw=1.8)
    ax.axhline(4, color="0.6", lw=0.9, ls="--")
    ax.text(11.5, 4.4, "4-mode floor (gapless ribbon modes)", fontsize=8, color="0.35")
    ax.set_xlabel(r"$\nu$ (THz)")
    ax.set_ylabel(r"$M(\nu)$")
    ax.set_title(r"(b) ribbon mode count, $W=18.6\ \mathrm{\AA}$ (zigzag $N=14$)")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "figD3_phonon.png"), dpi=200)
    print("wrote figD3_phonon.png")


def fig_wall():
    fig, ax = plt.subplots(figsize=(7.6, 3.9))
    x = np.linspace(-60, 60, 1200)
    for delta, c in ((3.18, "C0"), (9.55, "C3")):
        th = 2 * np.arctan(np.exp(x / delta))
        lam = np.pi * delta
        ax.plot(x, th / np.pi, color=c, lw=2.0,
                label=rf"$\delta={delta}\ \mathrm{{\AA}}$  ($\lambda=\pi\delta={lam:.0f}\ \mathrm{{\AA}}$)")
    ax.axhline(0, color="k", lw=0.6); ax.axhline(1, color="k", lw=0.6)
    # texture arrows for the wider wall
    delta = 9.55
    for xa in np.linspace(-52, 52, 13):
        th = 2 * np.arctan(np.exp(xa / delta))
        ax.annotate("", xy=(xa + 4.5 * np.sin(th), 1.13 + 0.10 * np.cos(th)),
                    xytext=(xa - 4.5 * np.sin(th), 1.13 - 0.10 * np.cos(th)),
                    arrowprops=dict(arrowstyle="-|>", color="C3", lw=1.2),
                    annotation_clip=False)
    ax.text(-58, 1.24, r"$\hat n(x)$:", color="C3", fontsize=10)
    # scattering region for the wider wall: +-4 delta + 2 lead periods (2a each) margin
    core = 4 * delta
    margin = 2 * 2 * A
    ax.axvspan(-core - margin, core + margin, color="C1", alpha=0.10)
    ax.axvspan(-core, core, color="C1", alpha=0.14)
    ax.annotate(r"wall core $\pm4\delta$", xy=(0, 0.06), fontsize=9, ha="center", color="0.3")
    ax.annotate("+ 2 lead periods\nmargin each side", xy=(core + margin / 2, 0.42),
                fontsize=8, ha="center", color="0.3")
    ax.set_xlabel(r"$x-x_0$ ($\mathrm{\AA}$)")
    ax.set_ylabel(r"$\theta(x)/\pi$")
    ax.set_ylim(-0.05, 1.38)
    ax.legend(frameon=False, fontsize=9, loc="center right")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "figD4_wall.png"), dpi=200)
    print("wrote figD4_wall.png")


if __name__ == "__main__":
    fig_geometry()
    fig_fermiwindow()
    fig_phonon()
    fig_wall()

from scipy.stats import betabinom
from matplotlib import pyplot as plt
import numpy as np
from fig_1 import set_size
from tueplots import fontsizes
import sys

sys.path.insert(0, "../src/")
from test_hypotheses import make_hypothesis_data, run_hypothesis_test
import pandas as pd


def make_plot():
    # Options
    params = {
        "text.latex.preamble": r"\usepackage{lmodern}",
        "text.usetex": True,
        "font.size": 9,
        "font.family": "sans",
    }
    plt.rcParams.update(params)
    plt.rcParams.update(fontsizes.neurips2021())

    data = pd.read_csv("../dat/data_clean.csv", dtype={5: "object", 16: "object"})
    filtered = make_hypothesis_data(data)
    p_value, n_1, m_0, n_0 = run_hypothesis_test(1910, 2020, filtered)
    print(p_value)

    m_2020 = len(
        filtered[
            (filtered["startYear"] == 2020)
            & (filtered["Budget"] > filtered["Gross worldwide"])
        ]
    )

    lst = []
    years = []
    n = []
    for year in range(1960, 2022):
        if len(filtered[filtered["startYear"] == year]) == 0:
            continue
        years.append(year)
        lst.append(
            len(
                filtered[
                    (filtered["startYear"] == year)
                    & (filtered["Budget"] > filtered["Gross worldwide"])
                ]
            )
            / len(filtered[filtered["startYear"] == year])
        )
        n.append(len(filtered[(filtered["startYear"] == year)]))

    p = betabinom(n_1, m_0 + 1, n_0 - m_0 + 1)
    mm_1 = np.arange(n_1)

    size = set_size(397.48499, fraction=1, subplots=(1, 2))
    color1 = "#deb522"
    color2 = "#128bb5"
    linewidth = 1

    fig, ax = plt.subplots(1, 2, figsize=size)
    fig.tight_layout()
    ax02 = ax[1].twinx()
    ax02.plot(years, n, color=color2, linewidth=linewidth)
    ax[1].set_title("(b) Movies \& Flop-Rates")
    ax[1].plot(years, lst, color=color1, linewidth=linewidth)

    ax[1].set_ylim(0, 1.0)
    ax02.set_ylim(0)
    ax02.set_xlim(1960, 2022)

    ax02.set_ylabel("\#movies", color=color2)
    ax[1].set_ylabel("flop-rate", color=color1)
    ax[1].set_xlabel("year")

    ax[1].tick_params(axis="y", labelcolor=color1)
    ax02.tick_params(axis="y", labelcolor=color2)

    mm_1_nr = mm_1[mm_1 <= betabinom.ppf(0.95, n_1, m_0 + 1, n_0 - m_0 + 1)]
    ax[0].step(mm_1_nr, p.pmf(mm_1_nr), color="#deb522", linewidth=0.75)
    ax[0].fill_between(
        mm_1_nr, 0, p.pmf(mm_1_nr), step="pre", color="#deb522", alpha=0.5
    )

    mm_1_nr = mm_1[mm_1 >= betabinom.ppf(0.95, n_1, m_0 + 1, n_0 - m_0 + 1)]
    ax[0].step(mm_1_nr, p.pmf(mm_1_nr), color="black", alpha=0.5, linewidth=0.75)
    ax[0].fill_between(mm_1_nr, 0, p.pmf(mm_1_nr), step="pre", color="black", alpha=0.5)
    ax[0].axvline(min(mm_1_nr), color="black", linestyle="-", linewidth=0.75)

    ax[0].set_title("(a) Hypothesis-Test")
    ax[0].annotate(
        r"$\alpha$",
        xy=(148, 0.003),
        xycoords="data",
        xytext=(155, 0.01),
        textcoords="data",
        arrowprops=dict(arrowstyle="-", color="black", lw=0.75, ls="-"),
    )

    ax[0].axvline(m_2020, color="#128bb5", linestyle="-", linewidth=0.75)
    ax[0].text(
        m_2020 - 3,
        0.027,
        "$m_{2020}=$" + str(m_2020),
        fontsize=7,
        va="center",
        ha="center",
        rotation=-270,
        color=color2,
    )

    ax[0].set_ylabel("$p(m \mid H_0)$")
    ax[0].set_xlabel("$m$")
    ax[0].set_xlim(90, 140 + 50)
    ax[0].set_ylim(0, 0.055)

    plt.savefig(
        "../dat/fig2.pdf", bbox_inches="tight", pad_inches=0.0, transparent=True
    )
    plt.savefig(
        "../dat/fig2.png",
        bbox_inches="tight",
        pad_inches=0.0,
        facecolor="white",
        dpi=1000,
    )


if __name__ == "__main__":
    make_plot()

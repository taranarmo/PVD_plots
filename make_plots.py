import numpy as np
import pandas as pd
import matpotlib as plt


def plot_pvd(x, y, ax=None):
    if not ax:
        ax = plt.gca()
    x, y = (data.cumsum() for data in (x, y))
    for depth, color in zip(cols, plt.cm.bwr_r(np.linspace(0, 1, len(cols)))):
        ax.plot(x.loc[:, depth], y.loc[:, depth], label=f"{depth:.2f}", color=color)
    ax.legend()


aq1 = {}
for direction in ["East", "North", "Up"]:
    aq1[direction.lower()] = pd.read_csv(f"AQ1_EXP102.{direction}.csv", index_col=0, parse_dates=True)
    aq1[direction.lower()].columns = aq1[direction.lower()].columns.astype(float)

aq2 = {}
for direction in ["East", "North", "Up"]:
    aq2[direction.lower()] = pd.read_csv(f"AQ2_EXP1-202.{direction}.csv", index_col=0, parse_dates=True)
    aq2[direction.lower()].columns = aq1[direction.lower()].columns.astype(float)

fig, axes = plt.subplots(2, 2, figsize=(7, 5))
plot_pvd(aq1["east"], aq1["up"], axes[0])
plot_pvd(aq1["north"], aq1["up"], axes[1])
plot_pvd(aq1["east"], aq1["north"], axes[2])
plt.savefig("pvds.png")

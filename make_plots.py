import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def plot_pvd(x, y, ax=None):
    if ax is None:
        ax = plt.gca()
    x, y = (data.cumsum() for data in (x, y))
    for depth, color in zip(cols, plt.cm.bwr_r(np.linspace(0, 1, len(cols)))):
        ax.plot(x.loc[:, depth], y.loc[:, depth], label=f"{depth:.2f}", color=color)


aq1 = {}
for direction in ["East", "North", "Up"]:
    aq1[direction.lower()] = pd.read_csv(f"AQ1_EXP102.{direction}.csv", index_col=0, parse_dates=True)
    aq1[direction.lower()].columns = aq1[direction.lower()].columns.astype(float)

aq2 = {}
for direction in ["East", "North", "Up"]:
    aq2[direction.lower()] = pd.read_csv(f"AQ2_EXP1-202.{direction}.csv", index_col=0, parse_dates=True)
    aq2[direction.lower()].columns = aq1[direction.lower()].columns.astype(float)

cols = aq1['east'].columns.values[::10]
fig, axes = plt.subplots(2, 2, figsize=(7, 5))
axes = axes.flatten()
plot_pvd(aq1["east"], aq1["up"], axes[0])
plot_pvd(aq1["north"], aq1["up"], axes[1])
plot_pvd(aq1["east"], aq1["north"], axes[2])
cell = np.argmin(np.abs((1.6 - aq1['east'].columns.values)))
axes[3].plot(aq1["east"].iloc[:, cell].cumsum(), aq1["north"].iloc[:, cell].cumsum())
axes[3].plot(aq2["east"].iloc[:, cell].cumsum(), aq2["north"].iloc[:, cell].cumsum())

for ax, label in zip(axes, "abcd"):
    ax.text(s=label, x=0.05, y=0.5, transform=ax.transAxes)
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, bbox_to_anchor=(1, 0.5), loc='center right')
plt.subplots_adjust(right=0.85)
plt.savefig("pvds.png")
plt.show()

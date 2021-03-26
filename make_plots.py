import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

params = {
    "font.size": 8,
    "legend.fontsize": 8,
    "legend.handlelength": 1,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
}
plt.rcParams.update(params)


def plot_pvd(x, y, ax=None):
    if ax is None:
        ax = plt.gca()
    x, y = (data.cumsum()*60 for data in (x, y))
    for depth, color in zip(cols, plt.cm.bwr_r(np.linspace(0, 1, len(cols)))):
        ax.plot(x.loc[:, depth], y.loc[:, depth], label=f"{depth:.2f}", color=color)


index = slice("2020-03-30 10:30", "2020-04-05")
aq1 = {}
for direction in ["East", "North", "Up"]:
    aq1[direction.lower()] = pd.read_csv(f"AQ1_EXP102.{direction}.csv", index_col=0, parse_dates=True)
    aq1[direction.lower()].columns = aq1[direction.lower()].columns.astype(float)
    aq1[direction.lower()] = aq1[direction.lower()].loc[index]

aq2 = {}
for direction in ["East", "North", "Up"]:
    aq2[direction.lower()] = pd.read_csv(f"AQ2_EXP1-202.{direction}.csv", index_col=0, parse_dates=True)
    aq2[direction.lower()].columns = aq1[direction.lower()].columns.astype(float)
    aq2[direction.lower()] = aq2[direction.lower()].loc[index]

cols = aq1['east'].columns.values[::10]
fig, axes = plt.subplots(2, 2, figsize=(5, 7), dpi=500, sharey='row')
axes = axes.flatten()
plot_pvd(aq1["east"], aq1["up"], axes[0])
axes[0].set_xlabel("East, m");
axes[0].set_ylabel("Up, m");
plot_pvd(aq1["north"], aq1["up"], axes[1])
axes[1].set_xlabel("North, m");
plot_pvd(aq1["east"], aq1["north"], axes[2])
axes[2].set_xlabel("East, m");
axes[2].set_ylabel("North, m");
cell = np.argmin(np.abs((1.6 - aq1['east'].columns.values)))
axes[3].plot(aq1["east"].iloc[:, cell].cumsum()*60, aq1["north"].iloc[:, cell].cumsum()*60, label="ADCP I")
axes[3].plot(aq2["east"].iloc[:, cell].cumsum()*60, aq2["north"].iloc[:, cell].cumsum()*60, label="ADCP II")
axes[3].set_xlabel("East, m");
axes[3].legend()

for ax, label in zip(axes, "abcd"):
    ax.text(s=label, x=0.03, y=0.5, transform=ax.transAxes, fontstyle="italic")

plt.tight_layout()
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, bbox_to_anchor=(0.5, 1), loc='upper center', ncol=len(labels)//3+1)
plt.subplots_adjust(top=0.9)
plt.savefig("pvds.png")
axes[0].set_xlabel("Восток, м");
axes[0].set_ylabel("Вверх, м");
axes[1].set_xlabel("Север, м");
axes[2].set_xlabel("Восток, м");
axes[2].set_ylabel("Север, м");
axes[3].set_xlabel("Восток, м");
plt.savefig("pvds_ru.png")

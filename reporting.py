"""Render a fixed synthetic source-replay snapshot, not live telemetry."""
import csv
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def render(folder="reports"):
    folder = Path(folder)
    with (folder / "dashboard_data.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    sequence = [int(r["sequence"]) for r in rows]
    balances = [int(r["balance_cents"]) for r in rows]
    counts = [int(r["active_orders"]) for r in rows]
    fig = plt.figure(figsize=(16, 9), facecolor="#eef3f8")
    fig.text(.05, .93, "ZARYN DATA ENGINEERING", fontsize=23, weight="bold", color="#123047")
    fig.text(.05, .86, "Modernization Data-State Overview", fontsize=22, color="#123047")
    cards = [("Source events", str(len(rows))), ("Active orders", str(counts[-1])), ("Ending value / cents", str(balances[-1])), ("Source sequences", f"{sequence[0]} to {sequence[-1]}")]
    for i, (label, value) in enumerate(cards):
        fig.text(.05+i*.235, .75, label, fontsize=11, color="#526575")
        fig.text(.05+i*.235, .68, value, fontsize=29, weight="bold", color="#247f88")
    left, right = fig.add_axes([.07,.25,.40,.30]), fig.add_axes([.57,.25,.36,.30])
    left.plot(sequence, balances, color="#247f88", marker="o", linewidth=3)
    right.bar(sequence, counts, color="#269d9b")
    for ax, title in [(left, "Reconstructed source value by event / cents"), (right, "Active orders after each source event")]:
        ax.set_title(title, loc="left", pad=18, fontsize=11)
        ax.set_xticks(sequence)
        ax.set_xlabel("Source event sequence")
        ax.set_ylim(bottom=0)
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", alpha=.15)
        ax.set_axisbelow(True)
    fig.text(.05,.14,"Synthetic source replay; one assumed currency. Not live monitoring or proof of an SSIS migration.",fontsize=10,color="#526575")
    fig.text(.05,.07,"SYNTHETIC DATA | STATIC PYTHON REPORT | NOT A POWER BI SCREENSHOT",fontsize=11,color="#247f88")
    fig.savefig(folder / "dashboard.png", dpi=160, facecolor=fig.get_facecolor())
    plt.close(fig)


if __name__ == "__main__":
    render()

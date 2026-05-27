"""Generate the figures in figures/ from data/cleaned_air_quality_data.csv.

Usage:  python make_charts.py
Reqs:   pip install pandas matplotlib
"""
import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DATA = "data/cleaned_air_quality_data.csv"
OUT = "figures"
os.makedirs(OUT, exist_ok=True)

# Read (Korean headers) with a few encoding fallbacks
df = None
for enc in ("utf-8", "cp949", "euc-kr"):
    try:
        df = pd.read_csv(DATA, encoding=enc)
        break
    except Exception:
        pass

cols = list(df.columns)
date_c = cols[0]


def find(key):
    return next((c for c in cols if key.lower() in c.lower()), None)


ren = {find("pm10"): "PM10", find("pm2.5"): "PM2.5", find("o3"): "O3",
       find("no2"): "NO2", find("co "): "CO", find("so2"): "SO2"}
df = df.rename(columns={k: v for k, v in ren.items() if k})
poll = [v for v in ["PM10", "PM2.5", "O3", "NO2", "CO", "SO2"] if v in df.columns]
for p in poll:
    df[p] = pd.to_numeric(df[p], errors="coerce")
df[date_c] = pd.to_datetime(df[date_c], errors="coerce")

# 1) pollutant correlation heatmap
corr = df[poll].corr()
fig, ax = plt.subplots(figsize=(6, 5))
im = ax.imshow(corr, cmap="RdYlBu_r", vmin=-1, vmax=1)
ax.set_xticks(range(len(poll))); ax.set_xticklabels(poll, rotation=45, ha="right")
ax.set_yticks(range(len(poll))); ax.set_yticklabels(poll)
for i in range(len(poll)):
    for j in range(len(poll)):
        ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center", fontsize=8)
ax.set_title("Seoul air pollutants — correlation")
fig.colorbar(im, fraction=0.046, pad=0.04); fig.tight_layout()
fig.savefig(f"{OUT}/correlation.png", dpi=130); plt.close(fig)

# 2) daily mean PM2.5
daily = df.dropna(subset=[date_c]).groupby(df[date_c].dt.date)["PM2.5"].mean()
fig, ax = plt.subplots(figsize=(9, 3.5))
ax.plot(pd.to_datetime(daily.index), daily.values, color="#0ea5e9", lw=1)
ax.set_title("Daily mean PM2.5 across Seoul"); ax.set_ylabel("PM2.5 (ug/m3)")
ax.grid(alpha=0.3); fig.tight_layout()
fig.savefig(f"{OUT}/pm25-timeseries.png", dpi=130); plt.close(fig)

# 3) monthly mean PM2.5 vs PM10
m = df.dropna(subset=[date_c]).copy(); m["month"] = m[date_c].dt.month
mm = m.groupby("month")[["PM2.5", "PM10"]].mean()
fig, ax = plt.subplots(figsize=(8, 4)); w = 0.4
ax.bar(mm.index - w / 2, mm["PM2.5"], w, label="PM2.5", color="#ef4444")
ax.bar(mm.index + w / 2, mm["PM10"], w, label="PM10", color="#f59e0b")
ax.set_xticks(list(mm.index)); ax.set_xlabel("Month"); ax.set_ylabel("ug/m3")
ax.set_title("Monthly average PM2.5 vs PM10 (Seoul)"); ax.legend(); ax.grid(alpha=0.3, axis="y")
fig.tight_layout(); fig.savefig(f"{OUT}/monthly-pm.png", dpi=130); plt.close(fig)

print("wrote figures to", OUT)

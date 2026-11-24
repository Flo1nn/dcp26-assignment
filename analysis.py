import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Create charts folder
os.makedirs("charts", exist_ok=True)

# Connect to SQLite and load data
conn = sqlite3.connect("sprint_data.db")

df = pd.read_sql_query(
    "SELECT * FROM training_sessions",
    conn
)

conn.close()

print(df.head())

# -----------------------------
# Data Analysis
# -----------------------------

sleep_analysis = (
    df.groupby("sleep_hours")["intensity_rpe"]
    .mean()
)

weather_analysis = (
    df.groupby("weather")["intensity_rpe"]
    .mean()
)

print("\nAverage RPE by sleep hours:")
print(sleep_analysis)

print("\nAverage RPE by weather:")
print(weather_analysis)


# -----------------------------
# Chart 1: Sleep vs RPE
# -----------------------------

plt.figure()

bars = plt.bar(
    sleep_analysis.index.astype(str),
    sleep_analysis.values
)

for bar in bars:
    height = bar.get_height()

    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height + 0.1,
        f"{height:.2f}",
        ha="center"
    )

plt.xlabel("Sleep Hours")
plt.ylabel("Average RPE")
plt.title("Average Training Intensity by Sleep Duration")
plt.ylim(0, 10)

plt.savefig(
    "charts/sleep_vs_rpe.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()


# -----------------------------
# Chart 2: Weather vs RPE
# -----------------------------

plt.figure()

bars = plt.bar(
    weather_analysis.index,
    weather_analysis.values
)

for bar in bars:
    height = bar.get_height()

    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height + 0.1,
        f"{height:.2f}",
        ha="center"
    )

plt.xlabel("Weather Condition")
plt.ylabel("Average RPE")
plt.title("Average Training Intensity by Weather")
plt.ylim(0, 10)

plt.savefig(
    "charts/weather_vs_rpe.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()


# -----------------------------
# Chart 3: Felt Rating vs RPE
# -----------------------------

# Exclude sessions with missing values
felt_data = df.dropna(
    subset=["felt_rating", "intensity_rpe"]
)

plt.figure()

# Add slight horizontal jitter to overlapping points
rng = np.random.default_rng(42)

x_jitter = (
    felt_data["felt_rating"]
    + rng.uniform(-0.1, 0.1, len(felt_data))
)

plt.scatter(
    x_jitter,
    felt_data["intensity_rpe"],
    alpha=0.7,
    s=80
)

plt.xlabel("Pre-Training Felt Rating (1-5)")
plt.ylabel("Training Intensity (RPE)")
plt.title("Pre-Training Felt Rating vs Actual RPE")

plt.xticks([1, 2, 3, 4, 5])
plt.xlim(0.5, 5.5)
plt.ylim(0, 10)

plt.savefig(
    "charts/felt_vs_rpe.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()

print("\nAll three charts saved successfully!")

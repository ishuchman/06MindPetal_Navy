import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("ridership.csv")

fig, ax = plt.subplots(figsize=(12, 6))


bar_width = 0.4
index = range(len(df["station"]))


ax.bar(index, df["Entries"], bar_width, label="Entries", color="blue")
ax.bar([i + bar_width for i in index], df["exits"], bar_width, label="Exits", color="red")


ax.set_xlabel("Station")
ax.set_ylabel("Count")
ax.set_title("Entries and Exits per Station")
ax.set_xticks([i + bar_width / 2 for i in index])
ax.set_xticklabels(df["station"], rotation=45, ha="right")
ax.legend()

# Save or Show
plt.tight_layout()
plt.savefig("ridership_plot.png")  
plt.show() 
import streamlit as st
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import pandas as pd
import numpy as np
from matplotlib.lines import Line2D

# ==========================
# CONFIG
# ==========================
st.set_page_config(layout="centered")

st.title("Pass Map")

# ==========================
# Coordenadas
# ==========================
cords = [
    (25.76, 49.31), (29.75, 74.08),
    (13.45, 56.79), (18.11, 30.36),
    (59.50, 58.29), (75.13, 75.24),
    (44.21, 62.11), (45.87, 33.68),
    (51.19, 55.46), (97.57, 39.83),
    (34.90, 69.09), (39.72, 76.24),
    (33.07, 60.11), (32.41, 30.52),
    (48.70, 66.10), (63.82, 76.74),
    (37.89, 62.61), (46.70, 54.79),
    (41.55, 66.76), (104.88, 56.79),
    (38.39, 49.81), (40.72, 30.52),
    (46.20, 59.95), (91.92, 23.54),
    (15.62, 55.79), (16.11, 32.85),
    (24.92, 63.77), (41.55, 75.74),
    (52.35, 61.28), (94.58, 24.04),
    (32.90, 62.44), (46.54, 67.10),
    (51.52, 62.44), (69.97, 77.07),
    (40.05, 58.12), (38.56, 32.19),
    (45.04, 49.81), (44.04, 33.02),
    (64.99, 57.45), (86.26, 78.40),
    (46.20, 58.12), (53.85, 32.02),
    (4.48, 53.96), (5.81, 39.83),
    (60.33, 61.28), (108.87, 73.08),
    (14.12, 55.79), (21.27, 44.99),
    (52.19, 67.76), (111.37, 66.10),
    (14.78, 46.65), (39.05, 52.47),
    (11.63, 58.45), (29.08, 76.57),
    (38.06, 53.30), (38.56, 35.18),
    (45.21, 65.93), (57.84, 70.25),
    (17.28, 73.41), (4.48, 58.95),
    (47.53, 53.13), (51.52, 39.83),
    (48.70, 61.28), (48.20, 33.52),
    (56.18, 61.61), (105.22, 39.17),
    (42.05, 60.11), (94.41, 79.40),
    (23.26, 53.13), (29.75, 28.36),
    (38.89, 56.79), (43.71, 31.02),
    (37.39, 59.45), (56.18, 77.24),
    (36.56, 68.43), (75.13, 61.28),
    (26.09, 58.62), (40.05, 79.56),
    (59.50, 63.94), (71.80, 76.57),
    (24.43, 55.63), (55.51, 48.48),
    (18.94, 63.27), (23.59, 31.69),
    (38.56, 59.78), (52.35, 73.25),
    (26.42, 72.91), (28.91, 74.74),
    (41.88, 58.62), (46.04, 40.83),
    (46.87, 53.80), (72.97, 71.92),

    (40.72, 47.98), (43.38, 66.60),
    (20.10, 54.63), (43.04, 55.13),
    (15.95, 56.29), (16.45, 28.86),
    (53.02, 57.79), (49.69, 39.50),
    (76.12, 40.00), (46.20, 3.26),
    (25.42, 53.80), (25.26, 28.70),
    (29.25, 58.62), (24.92, 32.85),
    (27.75, 55.29), (13.29, 39.17),
    (18.28, 59.12), (49.36, 74.41),
    (45.37, 70.75), (38.56, 60.78),
    (14.29, 53.63), (23.93, 67.76),
    (15.45, 51.30), (41.05, 70.92),
    (49.69, 65.27), (30.41, 51.14),
    (54.68, 67.26), (82.11, 52.14),
    (38.72, 31.85), (14.45, 38.17),
    (69.81, 73.41), (106.88, 43.49),
    (55.01, 46.65), (58.17, 26.70),
    (17.11, 69.09), (57.51, 55.46),
    (17.44, 64.27), (37.89, 76.57),
    (49.69, 48.31), (59.83, 62.44),
    (64.99, 59.28), (81.11, 77.90),
    (60.00, 45.82), (67.15, 63.77),
    (72.14, 56.46), (89.26, 46.32)
]

passes_errados = [5, 10, 12, 25, 33, 34, 41, 43, 44, 62, 64, 69]

# ==========================
# DataFrame
# ==========================
passes = []
for i in range(0, len(cords), 2):
    start, end = cords[i], cords[i+1]
    numero = int(i/2) + 1
    passes.append({
        "numero": numero,
        "x_start": start[0], "y_start": start[1],
        "x_end": end[0], "y_end": end[1]
    })

df = pd.DataFrame(passes)

goal_x, goal_y = 120, 40

def dist_to_goal(x, y):
    return np.sqrt((goal_x - x)**2 + (goal_y - y)**2)

df["dist_start"] = dist_to_goal(df.x_start, df.y_start)
df["dist_end"] = dist_to_goal(df.x_end, df.y_end)

df["errado"] = df["numero"].isin(passes_errados)

df["progressivo"] = (
    (~df["errado"]) & 
    (df["x_start"] > 40) & 
    (df["dist_end"] <= df["dist_start"] * 0.75)
)

# ==========================
# Plot (MENOR)
# ==========================
pitch = Pitch(pitch_type='statsbomb', pitch_color='#ffffff', line_color='#c7d5dd')
fig, ax = pitch.draw(figsize=(8, 5))  # reduzido

for _, row in df.iterrows():
    if row["errado"]:
        color = '#e74c3c'
        alpha = 0.6
        width = 1.5
    elif row["progressivo"]:
        color = '#3498db'
        alpha = 0.9
        width = 2.5
    else:
        color = '#bdc3c7'
        alpha = 0.4
        width = 1.2

    pitch.arrows(row.x_start, row.y_start, row.x_end, row.y_end,
                 color=color, alpha=alpha, width=width,
                 headwidth=3, headlength=3, ax=ax)

legend_elements = [
    Line2D([0], [0], color=(0.1, 0.4, 0.9, 0.9), lw=2.5, label='Progressive Passes'),
    Line2D([0], [0], color=(0.6, 0.6, 0.6, 0.5), lw=2, label='Successful Passes'),
    Line2D([0], [0], color=(0.9, 0.1, 0.1, 0.7), lw=2, label='Unsuccessful Passes')
]

ax.legend(handles=legend_elements, loc='upper left', fontsize=9,
          frameon=True, facecolor='#ffffff', edgecolor='#cccccc',
          shadow=True, bbox_to_anchor=(0.01, 0.99))

pitch.arrows(50, 85, 70, 85, color='#4a4a4a', width=1.5,
             headwidth=4, headlength=5, ax=ax, clip_on=False)

ax.text(60, 88, 'ATTACK DIRECTION', color='#4a4a4a',
        va='center', ha='center', fontsize=8, fontweight='bold', alpha=0.8)

plt.title("Pass Map", fontsize=13, pad=15)

# largura ~850px
st.pyplot(fig, use_container_width=True)

# ==========================
# Estatísticas
# ==========================
st.markdown("---")

col1, col2, col3 = st.columns(3)

col1.metric("PASSES", "69", "57 (82.6%)")
col2.metric("PROGRESSIVE", "11", "3 (27.3%)")
col3.metric("LONG PASSES", "12", "4 (33.3%)")

col4, col5, col6 = st.columns(3)

col4.metric("FINAL THIRD", "13", "5 (38.5%)")
col5.metric("OWN FIELD", "49", "45 (91.8%)")
col6.metric("OPP FIELD", "20", "12 (60.0%)")

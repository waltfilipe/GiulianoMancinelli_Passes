import streamlit as st
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import pandas as pd
import numpy as np
import ast

# Page Configuration
st.set_page_config(page_title="Opta Pass Analyzer", layout="wide")

st.title("⚽ Professional Pass Map (Opta Standard)")
st.sidebar.header("Data Input & Settings")

# ==========================
# Manual Data Entry
# ==========================
default_coords = "[(25.76, 49.31), (29.75, 74.08), (13.45, 56.79), (18.11, 30.36)]"
input_coords = st.sidebar.text_area("Paste coordinates here (List of Tuples):", 
                                   value=default_coords, height=300)

input_errados = st.sidebar.text_input("Unsuccessful pass numbers (comma separated):", 
                                     value="5, 10, 12, 25, 33, 34, 41, 43, 44, 62, 64, 69")

try:
    # Safe conversion from string to Python list
    coords_list = ast.literal_eval(input_coords)
    unsuccessful_passes = [int(x.strip()) for x in input_errados.split(",") if x.strip()]
    
    # Data Processing
    num_passes = len(coords_list) // 2
    clean_coords = coords_list[:num_passes * 2]
    
    data = []
    for i in range(0, len(clean_coords), 2):
        start, end = clean_coords[i], clean_coords[i+1]
        number = int(i/2) + 1
        data.append({
            "number": number,
            "x_start": start[0], "y_start": start[1],
            "x_end": end[0], "y_end": end[1]
        })

    df = pd.DataFrame(data)

    # ==========================
    # Opta Progressive Logic
    # ==========================
    goal_x, goal_y = 120, 40

    def dist_to_goal(x, y):
        return np.sqrt((goal_x - x)**2 + (goal_y - y)**2)

    df["dist_start"] = dist_to_goal(df.x_start, df.y_start)
    df["dist_end"] = dist_to_goal(df.x_end, df.y_end)
    df["unsuccessful"] = df["number"].isin(unsuccessful_passes)

    # Opta Rule: Starts in attacking 2/3 (>40m) and reduces distance to goal by 25%
    df["progressive"] = (
        (~df["unsuccessful"]) & 
        (df["x_start"] > 40) & 
        (df["dist_end"] <= df["dist_start"] * 0.75)
    )

    # ==========================
    # Streamlit Visualization
    # ==========================
    col1, col2 = st.columns([3, 1])

    with col1:
        # Drawing the Pitch
        pitch = Pitch(pitch_type='statsbomb', pitch_color='#1e1e1e', line_color='#888888')
        fig, ax = pitch.draw(figsize=(12, 9))

        for _, row in df.iterrows():
            if row["unsuccessful"]:
                color, alpha, width = '#ff4b4b', 0.6, 1.5 # Red
            elif row["progressive"]:
                color, alpha, width = '#0068c9', 0.9, 2.5 # Blue
            else:
                color, alpha, width = '#808495', 0.4, 1.2 # Grey (Successful Common)

            pitch.arrows(row.x_start, row.y_start, row.x_end, row.y_end,
                         color=color, alpha=alpha, width=width,
                         headwidth=3, headlength=3, ax=ax)

        st.pyplot(fig)

    with col2:
        st.subheader("Performance Metrics")
        tot = len(df)
        err = df["unsuccessful"].sum()
        prog = df["progressive"].sum()
        
        st.metric("Total Passes", tot)
        st.metric("Pass Accuracy", f"{((tot-err)/tot)*100:.1f}%")
        st.metric("Progressive Passes", prog)
        
        st.write("---")
        st.caption("**Legend:**")
        st.markdown("🔴 **Unsuccessful**")
        st.markdown("🔵 **Progressive (Opta)**")
        st.markdown("⚪ **Successful (Common)**")

except Exception as e:
    st.error(f"Error processing data: {e}")
    st.info("Make sure the coordinates are formatted correctly: [(x,y), (x,y), ...]")

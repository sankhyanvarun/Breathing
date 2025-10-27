import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time
import math

# Page config
st.set_page_config(page_title="🌿 Breathing Meditation", layout="centered")

# ---------------------------
# Initialize Session State
# ---------------------------
if "running" not in st.session_state:
    st.session_state.running = False
if "state" not in st.session_state:
    st.session_state.state = "IDLE"
if "cycle_count" not in st.session_state:
    st.session_state.cycle_count = 0

# ---------------------------
# UI Header
# ---------------------------
st.markdown(
    """
    <h1 style='text-align:center; color:#7cd1b8;'>🌿 Guided Breathing Exercise</h1>
    <p style='text-align:center; color:#cbd5e1;'>
    Breathe in... hold... and exhale slowly.<br>
    Let your mind relax and follow the calm rhythm.
    </p>
    """,
    unsafe_allow_html=True
)

# ---------------------------
# Controls
# ---------------------------
col1, col2, col3 = st.columns(3)
if col1.button("▶️ Start"):
    st.session_state.running = True
if col2.button("⏸ Pause"):
    st.session_state.running = False
if col3.button("🔄 Reset"):
    st.session_state.running = False
    st.session_state.state = "IDLE"
    st.session_state.cycle_count = 0

# ---------------------------
# Background Styling (CSS)
# ---------------------------
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #e0f7fa, #fce4ec, #f3e5f5);
    background-size: 400% 400%;
    animation: gradientFlow 12s ease infinite;
}

@keyframes gradientFlow {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

h1, p {
    font-family: 'Trebuchet MS', sans-serif;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ---------------------------
# Circle Drawer Function
# ---------------------------
def draw_circle(radius, color):
    fig, ax = plt.subplots(figsize=(4, 4))
    circle = plt.Circle((0, 0), radius, color=color, alpha=0.7)
    ax.add_artist(circle)
    ax.set_xlim(-6, 6)
    ax.set_ylim(-6, 6)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor("none")
    return fig

# ---------------------------
# Placeholders
# ---------------------------
placeholder = st.empty()
status_text = st.empty()

# ---------------------------
# Parameters
# ---------------------------
min_radius = 1.0
max_radius = 5.5
breath_duration = 5.0  # seconds per inhale/exhale
fps = 30  # frames per second
frame_delay = 1.0 / fps

# ---------------------------
# Breathing Colors
# ---------------------------
inhale_color = "#8fd9b6"
hold_color = "#ffcf91"
exhale_color = "#f6a5c0"

# ---------------------------
# Animation Loop
# ---------------------------
while st.session_state.running:
    t = np.linspace(0, math.pi, int(breath_duration * fps))

    # 🌿 INHALE (expand)
    st.session_state.state = "INHALE"
    for x in t:
        if not st.session_state.running:
            break
        radius = min_radius + (max_radius - min_radius) * (math.sin(x / 2)) ** 2
        fig = draw_circle(radius, inhale_color)
        placeholder.pyplot(fig)
        status_text.markdown("<h4 style='text-align:center; color:#4caf50;'>🫁 Inhale deeply...</h4>", unsafe_allow_html=True)
        time.sleep(frame_delay)

    # ✋ HOLD
    st.session_state.state = "HOLD"
    for _ in range(int(2 * fps)):
        if not st.session_state.running:
            break
        fig = draw_circle(max_radius, hold_color)
        placeholder.pyplot(fig)
        status_text.markdown("<h4 style='text-align:center; color:#ff9800;'>✋ Hold your breath...</h4>", unsafe_allow_html=True)
        time.sleep(frame_delay)

    # 🌬️ EXHALE (contract)
    st.session_state.state = "EXHALE"
    for x in t:
        if not st.session_state.running:
            break
        radius = max_radius - (max_radius - min_radius) * (math.sin(x / 2)) ** 2
        fig = draw_circle(radius, exhale_color)
        placeholder.pyplot(fig)
        status_text.markdown("<h4 style='text-align:center; color:#e91e63;'>🌬️ Exhale slowly...</h4>", unsafe_allow_html=True)
        time.sleep(frame_delay)

    st.session_state.cycle_count += 1
    status_text.markdown(
        f"<h4 style='text-align:center; color:#7cd1b8;'>✅ Completed cycles: {st.session_state.cycle_count}</h4>",
        unsafe_allow_html=True
    )
    time.sleep(1)

# ---------------------------
# Idle State Display
# ---------------------------
if not st.session_state.running:
    fig = draw_circle(3, "#aee2ff")
    placeholder.pyplot(fig)
    status_text.markdown(
        f"<h4 style='text-align:center; color:#607d8b;'>🧘 State: {st.session_state.state} | Cycles: {st.session_state.cycle_count}</h4>",
        unsafe_allow_html=True
    )

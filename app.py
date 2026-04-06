import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.express as px
from folium.plugins import HeatMap
import base64
from pathlib import Path
from fpdf import FPDF

# --------------------------
# PAGE CONFIG
# --------------------------
st.set_page_config(
    page_title="CrossLife Ministries — Malawi",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------
# BRAND COLORS
# --------------------------
GREEN       = "#00E676"
GREEN_DARK  = "#00C853"
GREEN_DEEP  = "#00796B"
CHARCOAL    = "#333D42"
WHITE       = "#FFFFFF"
LIGHT_BG    = "#F5FAF7"
CARD_BG     = "#FFFFFF"
BORDER      = "#D0EFE0"
MUTED       = "#7A9080"

# --------------------------
# LOAD LOGO
# --------------------------
def get_logo_base64():
    logo_path = Path("logo.jpg")
    if logo_path.exists():
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

logo_b64 = get_logo_base64()

# --------------------------
# GLOBAL CSS
# --------------------------
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Poppins:wght@600;700&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
    background-color: {LIGHT_BG};
    color: {CHARCOAL};
}}

/* Hide default Streamlit chrome */
#MainMenu {{ visibility: hidden; }}
header {{ visibility: hidden; }}
footer {{ visibility: hidden; }}

/* Sidebar — always open, collapse arrow hidden */
[data-testid="collapsedControl"] {{ display: none !important; }}
section[data-testid="stSidebar"] {{
    transform: none !important;
    visibility: visible !important;
    display: block !important;
    min-width: 250px !important;
    width: 250px !important;
    position: relative !important;
}}
section[data-testid="stSidebar"][aria-expanded="false"] {{
    margin-left: 0 !important;
    transform: none !important;
}}

/* App background */
.stApp {{ background-color: {LIGHT_BG}; }}

/* Sidebar */
[data-testid="stSidebar"] {{
    background: {CHARCOAL} !important;
    border-right: 3px solid {GREEN} !important;
    min-width: 250px !important;
}}
[data-testid="stSidebar"] * {{ color: #E8F5E9 !important; }}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stCheckbox label {{
    color: #A5D6A7 !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    letter-spacing: 0.8px !important;
    text-transform: uppercase !important;
}}
[data-testid="stSidebar"] [data-baseweb="select"] {{
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(0,230,118,0.3) !important;
    border-radius: 8px !important;
}}
[data-testid="stSidebar"] .stCheckbox {{
    background: rgba(255,255,255,0.05);
    border-radius: 8px;
    padding: 4px 8px;
}}

/* File uploader */
[data-testid="stFileUploader"] {{
    background: rgba(255,255,255,0.10) !important;
    border: 2px dashed {GREEN} !important;
    border-radius: 12px !important;
    padding: 12px !important;
}}
[data-testid="stFileUploader"] * {{ color: #E8F5E9 !important; }}
[data-testid="stFileUploader"] small,
[data-testid="stFileUploader"] span {{ color: #A5D6A7 !important; font-size: 11px !important; }}
[data-testid="stFileUploader"] button {{
    background: {GREEN} !important;
    color: {CHARCOAL} !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
}}

/* Main content */
.block-container {{
    padding: 1.5rem 2rem 2rem !important;
    max-width: 100% !important;
}}

/* Metric cards */
[data-testid="metric-container"] {{
    background: {CARD_BG} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 12px !important;
    padding: 16px 20px !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
}}
[data-testid="metric-container"] [data-testid="stMetricValue"] {{
    font-family: 'Poppins', sans-serif !important;
    font-size: 28px !important;
    font-weight: 700 !important;
    color: {GREEN_DEEP} !important;
}}
[data-testid="metric-container"] [data-testid="stMetricLabel"] {{
    font-size: 11px !important;
    font-weight: 500 !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    color: {MUTED} !important;
}}

/* Buttons */
.stButton > button {{
    background: {GREEN} !important;
    color: {CHARCOAL} !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 24px !important;
    font-size: 13px !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 2px 8px rgba(0,230,118,0.25) !important;
}}
.stButton > button:hover {{
    background: {GREEN_DARK} !important;
    box-shadow: 0 4px 14px rgba(0,230,118,0.4) !important;
    transform: translateY(-1px) !important;
}}

/* Section headers */
.section-header {{
    font-family: 'Poppins', sans-serif;
    font-size: 15px;
    font-weight: 600;
    color: {CHARCOAL};
    letter-spacing: 0.3px;
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 2px solid {GREEN};
    display: inline-block;
    background: transparent !important;
}}

/* Inputs */
.stTextInput input, .stPasswordInput input {{
    border-radius: 8px !important;
    border: 1px solid {BORDER} !important;
    font-size: 13px !important;
}}
.stTextInput input:focus, .stPasswordInput input:focus {{
    border-color: {GREEN} !important;
    box-shadow: 0 0 0 2px rgba(0,230,118,0.2) !important;
}}

/* Mobile responsive */
@media (max-width: 768px) {{
    .block-container {{ padding: 0.5rem 0.8rem !important; }}
    [data-testid="stSidebar"] {{
        min-width: 100% !important;
        width: 100% !important;
    }}
    [data-testid="metric-container"] {{ padding: 10px 12px !important; }}
    [data-testid="metric-container"] [data-testid="stMetricValue"] {{
        font-size: 20px !important;
    }}
    .section-header {{ font-size: 13px !important; }}
    div[data-testid="column"] {{ min-width: 100% !important; }}
}}
</style>
""", unsafe_allow_html=True)

# --------------------------
# HEADER
# --------------------------
def render_header():
    logo_html = (
        f'<img src="data:image/jpeg;base64,{logo_b64}" style="height:48px;object-fit:contain;" />'
        if logo_b64 else
        f'<div style="font-family:Poppins,sans-serif;font-size:22px;font-weight:700;color:{GREEN};">✟ CrossLife</div>'
    )
    st.markdown(f"""
    <div style="
        background:{CHARCOAL};border-radius:14px;padding:14px 24px;
        display:flex;align-items:center;justify-content:space-between;
        margin-bottom:24px;box-shadow:0 2px 12px rgba(0,0,0,0.1);
    ">
        <div style="display:flex;align-items:center;gap:16px;">
            {logo_html}
            <div>
                <div style="font-family:Poppins,sans-serif;font-size:16px;font-weight:600;color:{WHITE};line-height:1.2;">CrossLife Ministries</div>
                <div style="font-size:11px;color:#A5D6A7;letter-spacing:1.5px;text-transform:uppercase;">DASHBOARD</div>
            </div>
        </div>
        <div style="font-size:11px;color:#A5D6A7;text-align:right;">
            Member Distribution System<br>
            <span style="color:{GREEN};font-weight:600;">● Live</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --------------------------
# PDF EXPORT
# --------------------------
def export_pdf(df):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_fill_color(51, 61, 66)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 12, "CrossLife Ministries — Member Data", ln=True, fill=True, align="C")
    pdf.ln(4)

    pdf.set_fill_color(0, 200, 83)
    pdf.set_text_color(51, 61, 66)
    pdf.set_font("Helvetica", "B", 10)
    for col, w in [("District", 60), ("Center", 90), ("Members", 40)]:
        pdf.cell(w, 9, col, border=1, fill=True)
    pdf.ln()

    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(0, 0, 0)
    for i, row in df.reset_index(drop=True).iterrows():
        if i % 2 == 0:
            pdf.set_fill_color(245, 250, 247)
        else:
            pdf.set_fill_color(255, 255, 255)
        pdf.cell(60, 7, str(row["District"]),     border=1, fill=True)
        pdf.cell(90, 7, str(row["Center"]),       border=1, fill=True)
        pdf.cell(40, 7, str(int(row["Members"])), border=1, fill=True, align="R")
        pdf.ln()

    pdf.ln(6)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 6, "CrossLife Ministries Malawi © 2026", align="C")

    return bytes(pdf.output())

# --------------------------
# LOGIN
# --------------------------
USERNAME = "admin"
PASSWORD = "Crosslife26"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    if logo_b64:
        st.markdown(f"""
        <div style="text-align:center;margin:40px 0 8px;">
            <img src="data:image/jpeg;base64,{logo_b64}" style="height:80px;object-fit:contain;" />
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="text-align:center;margin-bottom:32px;">
        <div style="font-family:Poppins,sans-serif;font-size:26px;font-weight:700;color:{CHARCOAL};">Welcome Back</div>
        <div style="font-size:13px;color:{MUTED};margin-top:4px;">Sign in to access the CrossLife dashboard</div>
    </div>
    """, unsafe_allow_html=True)

    col_l, col_m, col_r = st.columns([1, 1.2, 1])
    with col_m:
        st.markdown(f'<div style="background:{CARD_BG};border:1px solid {BORDER};border-radius:16px;padding:32px 28px;box-shadow:0 4px 24px rgba(0,0,0,0.07);">', unsafe_allow_html=True)
        u = st.text_input("Username", placeholder="Enter username")
        p = st.text_input("Password", type="password", placeholder="Enter password")
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if st.button("Sign In →", use_container_width=True):
            if u == USERNAME and p == PASSWORD:
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid credentials. Please try again.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(f'<div style="text-align:center;margin-top:24px;font-size:11px;color:{MUTED};">CrossLife Ministries © 2026 · Malawi</div>', unsafe_allow_html=True)
    st.stop()

# --------------------------
# MAIN APP
# --------------------------
render_header()

# --------------------------
# SIDEBAR — always open
# --------------------------
with st.sidebar:
    if logo_b64:
        st.markdown(f"""
        <div style="text-align:center;padding:16px 0 20px;">
            <img src="data:image/jpeg;base64,{logo_b64}" style="height:52px;object-fit:contain;filter:brightness(1.1);" />
            <div style="font-size:10px;color:#A5D6A7;letter-spacing:2px;text-transform:uppercase;margin-top:8px;">Dashboard Controls</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<p style="font-size:10px;letter-spacing:1.5px;text-transform:uppercase;color:#A5D6A7;margin-bottom:4px;">Data</p>', unsafe_allow_html=True)
    file = st.file_uploader("Upload Excel File", type=["xlsx"], label_visibility="collapsed")
    st.markdown("---")

    if st.button("🚪 Sign Out", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

# --------------------------
# NO FILE STATE
# --------------------------
if not file:
    st.markdown(f"""
    <div style="
        background:{CARD_BG};border:2px dashed {BORDER};border-radius:16px;
        text-align:center;padding:60px 40px;margin-top:20px;
    ">
        <div style="font-size:36px;margin-bottom:12px;">📂</div>
        <div style="font-family:Poppins,sans-serif;font-size:18px;font-weight:600;color:{CHARCOAL};margin-bottom:8px;">Upload Your Data</div>
        <div style="font-size:13px;color:{MUTED};">Upload an Excel (.xlsx) file with columns:<br><strong>District, Center, Members, Latitude, Longitude</strong></div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# --------------------------
# LOAD + VALIDATE DATA
# --------------------------
df = pd.read_excel(file)
required = {"District", "Center", "Members", "Latitude", "Longitude"}
if not required.issubset(df.columns):
    st.error(f"Missing columns. File must contain: {', '.join(required)}")
    st.stop()

# --------------------------
# SIDEBAR FILTERS
# --------------------------
with st.sidebar:
    st.markdown('<p style="font-size:10px;letter-spacing:1.5px;text-transform:uppercase;color:#A5D6A7;margin-bottom:4px;">Filters</p>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<p style="font-size:10px;letter-spacing:1.5px;text-transform:uppercase;color:#A5D6A7;margin-bottom:4px;">Map Options</p>', unsafe_allow_html=True)
    show_labels  = st.checkbox("Show Center Labels", value=True)
    show_heatmap = st.checkbox("Show Heatmap", value=False)

    districts = st.multiselect("District", df["District"].unique(), default=df["District"].unique())
    filtered_df = df[df["District"].isin(districts)]

    centers = st.multiselect("Center", filtered_df["Center"].unique(), default=filtered_df["Center"].unique())
    filtered_df = filtered_df[filtered_df["Center"].isin(centers)]


# --------------------------
# KPIs
# --------------------------
total_members   = int(filtered_df["Members"].sum())
total_centers   = len(filtered_df["Center"].unique())
total_districts = len(filtered_df["District"].unique())
avg_per_center  = int(filtered_df["Members"].mean()) if len(filtered_df) > 0 else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Members",  f"{total_members:,}")
c2.metric("Active Centers", f"{total_centers:,}")
c3.metric("Districts",      f"{total_districts:,}")
c4.metric("Avg per Center", f"{avg_per_center:,}")

st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

# --------------------------
# MAP
# --------------------------
st.markdown('<div class="section-header">📍 Geographic Distribution</div>', unsafe_allow_html=True)

m = folium.Map(
    location=[filtered_df["Latitude"].mean(), filtered_df["Longitude"].mean()],
    zoom_start=7,
    tiles="CartoDB Positron"
)

# Heatmap rendered first so dots appear on top
if show_heatmap:
    heat_data = [[r["Latitude"], r["Longitude"], r["Members"]] for _, r in filtered_df.iterrows()]
    HeatMap(heat_data, radius=25, blur=15,
            gradient={"0.0": "green", "0.5": "yellow", "1.0": "red"}).add_to(m)

for _, row in filtered_df.iterrows():
    tooltip_html = f"""
    <div style="font-family:Inter,sans-serif;font-size:12px;font-weight:600;
        color:{CHARCOAL};background:white;padding:6px 10px;border-radius:6px;
        border-left:3px solid {GREEN};box-shadow:0 2px 8px rgba(0,0,0,0.12);white-space:nowrap;">
        {row['Center']}<br>
        <span style="font-weight:400;color:{MUTED};font-size:11px;">
            {row['District']} · {int(row['Members'])} members
        </span>
    </div>"""

    folium.CircleMarker(
        location=[row["Latitude"], row["Longitude"]],
        radius=6,
        color=GREEN_DEEP,
        fill=True,
        fill_color=GREEN,
        fill_opacity=0.9,
        weight=2,
        tooltip=folium.Tooltip(tooltip_html, sticky=False),
    ).add_to(m)

    if show_labels:
        folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
            icon=folium.DivIcon(
                html=f"""<div style="
                    font-family:Inter,sans-serif;
                    font-size:10px;
                    font-weight:600;
                    color:#000000;
                    background:rgba(255,255,255,0.88);
                    padding:2px 6px;
                    border-radius:4px;
                    border:1px solid {BORDER};
                    white-space:nowrap;
                    box-shadow:0 1px 4px rgba(0,0,0,0.1);
                    pointer-events:none;
                    position:relative;
                    top:-22px;
                    left:8px;
                ">{row['Center']}</div>""",
                icon_size=(120, 20),
                icon_anchor=(0, 0)
            )
        ).add_to(m)

st_folium(m, width="100%", height=480, returned_objects=[])

st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

# --------------------------
# CHARTS
# --------------------------
st.markdown('<div class="section-header">📊 Analytics</div>', unsafe_allow_html=True)

CHART_COLORS = [GREEN, GREEN_DARK, GREEN_DEEP, "#69F0AE", "#00BFA5", "#1B5E20", "#B2DFDB", "#004D40"]

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    pie_data = filtered_df.groupby("District")["Members"].sum().reset_index()
    fig1 = px.pie(pie_data, values="Members", names="District",
                  title="Members by District",
                  color_discrete_sequence=CHART_COLORS, hole=0.42)
    fig1.update_layout(
        font_family="Inter",
        title_font=dict(size=14, color=CHARCOAL, family="Poppins"),
        title_x=0, paper_bgcolor="white", plot_bgcolor="white",
        margin=dict(t=40, b=20, l=10, r=10),
        legend=dict(font=dict(size=11, color=CHARCOAL)),
    )
    fig1.update_traces(textfont_size=11, marker=dict(line=dict(color="white", width=2)))
    st.plotly_chart(fig1, use_container_width=True)

with chart_col2:
    bar_data = filtered_df.groupby("Center")["Members"].sum().reset_index().sort_values("Members", ascending=True)
    fig2 = px.bar(bar_data, x="Members", y="Center", orientation="h",
                  title="Members per Center", color="Members",
                  color_continuous_scale=[[0, "#B2DFDB"], [0.5, GREEN], [1, GREEN_DEEP]])
    fig2.update_layout(
        font_family="Inter",
        title_font=dict(size=14, color=CHARCOAL, family="Poppins"),
        title_x=0, paper_bgcolor="white", plot_bgcolor="white",
        margin=dict(t=40, b=20, l=10, r=20),
        xaxis=dict(showgrid=True, gridcolor="#F0F4F0", title=""),
        yaxis=dict(showgrid=False, title="", tickfont=dict(color="#000000", size=11)),
        coloraxis_showscale=False,
        bargap=0.25,
    )
    fig2.update_traces(marker_line_width=0)
    st.plotly_chart(fig2, use_container_width=True)

# --------------------------
# DATA TABLE
# --------------------------
st.markdown('<div class="section-header">📋 Data Table</div>', unsafe_allow_html=True)
st.dataframe(
    filtered_df[["District", "Center", "Members"]].sort_values("Members", ascending=False).reset_index(drop=True),
    use_container_width=True,
    height=220,
)

# --------------------------
# FOOTER
# --------------------------
st.markdown(f"""
<div style="
    margin-top:40px;padding:16px 24px;background:{CHARCOAL};border-radius:12px;
    display:flex;align-items:center;justify-content:space-between;
">
    <div style="font-size:11px;color:#A5D6A7;">CrossLife Ministries Malawi · Member Distribution Dashboard</div>
    <div style="font-size:11px;color:#A5D6A7;">© 2026</div>
</div>
""", unsafe_allow_html=True)

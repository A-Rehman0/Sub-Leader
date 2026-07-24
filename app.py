import streamlit as st
import pandas as pd
from datetime import datetime
import pickle
import os
import folium
from streamlit_folium import st_folium
from fpdf import FPDF
@st.cache_data(ttl=300)
def load_sheet_csv(url):
    return pd.read_csv(url)

# ── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="Blue Planet Dashboard", layout="wide")

# ── GLOBAL CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');           
#MainMenu,footer,header{visibility:hidden;}
.block-container{padding:0 2rem 3rem !important;margin-top:0 !important;background:#eef3fb;max-width:100% !important;}
.stTabs{margin-top:-20px;}
.stTabs [data-baseweb="tab-list"]{gap:6px !important;margin-bottom:0 !important;padding-bottom:0 !important;background:transparent;}
.stTabs [data-baseweb="tab"]{
    height:38px !important;
    padding:10px 24px !important;
    background:#dce8f9 !important;
    color:#0d47a1 !important;
    font-weight:700 !important;
    font-size:14px !important;
    border-radius:12px 12px 0 0 !important;
    border:1px solid #b0c8f0 !important;
    border-bottom:none !important;
    display:flex !important;
    align-items:center !important;
    transition:all 0.3s cubic-bezier(0.4,0,0.2,1) !important;
}

/* Custom Scrollbar - Thicker & More Visible */
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: #e2e8f0; border-radius: 10px; }
::-webkit-scrollbar-thumb { 
    background: linear-gradient(180deg, #0C4A6E, #06B6D4); 
    border-radius: 10px; 
    border: 2px solid #e2e8f0;
}
::-webkit-scrollbar-thumb:hover { background: linear-gradient(180deg, #06B6D4, #0C4A6E); }

.stTabs [data-baseweb="tab-panel"]{padding-top:8px !important;}
.stTabs [data-baseweb="tab"]:hover{background:#c5d8f7 !important;transform:translateY(-3px);box-shadow:0 6px 15px rgba(12,74,110,.1);}
.stTabs [aria-selected="true"]{
    background:linear-gradient(135deg, #0C4A6E, #06B6D4) !important;
    color:#fff !important;
    border-color:#0d47a1 !important;
    box-shadow:0 6px 20px rgba(6,182,212,0.4) !important;
    transform:translateY(-3px);
}

/* ── Animations ── */
@keyframes fadeInUp {
    0% { opacity: 0; transform: translate3d(0, 30px, 0) scale(0.98); }
    100% { opacity: 1; transform: translate3d(0, 0, 0) scale(1); }
}
@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
@keyframes shimmer {
    0% { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}
@keyframes pulseGlow {
    0%, 100% { box-shadow: 0 4px 15px rgba(12,74,110,0.2); }
    50% { box-shadow: 0 8px 25px rgba(6,182,212,0.45); }
}
@keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-4px); }
}

.animate-fade-up { animation: fadeInUp 0.7s cubic-bezier(0.25, 0.1, 0.25, 1) forwards; opacity: 0; }

/* Stagger KPI cards */
.kpi-wrap > div:nth-child(1) { animation-delay: 0.1s; }
.kpi-wrap > div:nth-child(2) { animation-delay: 0.2s; }
.kpi-wrap > div:nth-child(3) { animation-delay: 0.3s; }
.kpi-wrap > div:nth-child(4) { animation-delay: 0.4s; }
.kpi-wrap > div:nth-child(5) { animation-delay: 0.5s; }
.kpi-wrap > div:nth-child(6) { animation-delay: 0.6s; }

/* Sidebar Dark Theme */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020617 0%, #0f172a 100%) !important;
    border-right: 2px solid #06B6D4 !important;
    box-shadow: 4px 0 20px rgba(0,0,0,0.3);
}
section[data-testid="stSidebar"] .stMarkdown, section[data-testid="stSidebar"] label {
    color: #e2e8f0 !important;
}
section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {
    color: #ffffff !important;
    text-shadow: 0 2px 4px rgba(0,0,0,0.3);
}

.topbar::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 4px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.7), transparent);
    animation: shimmer 3s infinite;
}
.topbar h2 { margin: 0; font-size: 30px; font-weight: 800; color: #fff; letter-spacing: -0.5px; text-shadow: 0 2px 4px rgba(0,0,0,0.2); }
.topbar p { margin: 4px 0 0; font-size: 13px; color: #e0f2fe; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 600; }
.topbar-live { 
    margin-left: auto; text-align: right; color: #fff; 
    background: rgba(255,255,255,0.15); padding: 12px 20px; border-radius: 12px; 
    backdrop-filter: blur(8px); 
    border: 1px solid rgba(255,255,255,0.3);
    box-shadow: inset 0 2px 4px rgba(255,255,255,0.1);
}
.topbar-live .time { font-size: 24px; font-weight: 800; line-height: 1; font-variant-numeric: tabular-nums; }
.topbar-live .date { font-size: 12px; opacity: 0.9; margin-top: 4px; font-weight: 500; }

.stTabs [data-baseweb="tab-highlight"]{display:none;}
.stTabs [data-baseweb="tab-border"]{display:none;}
.stTabs [data-baseweb="tab-panel"]{padding-top:0 !important;}           

.topbar{
    background:linear-gradient(135deg, #0C4A6E, #06B6D4) !important;
    background-size:300% 300%;
    animation:gradientShift 10s ease infinite;
    padding:14px 28px;
    display:flex;
    align-items:center;
    gap:14px;
    margin-bottom:24px;
    border-radius:0 0 14px 14px;
    box-shadow:0 10px 30px rgba(12,74,110,0.3);
    border-bottom:4px solid #06B6D4;
    position:relative;
    overflow:hidden;
}

.link-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:14px;margin-top:10px;}
.link-card{background:#fff;border:1.5px solid #dce8f9;border-radius:14px;padding:20px;box-shadow:0 2px 8px rgba(13,71,161,.06);transition:all 0.3s ease;animation:fadeInUp 0.6s ease-out forwards;opacity:0;position:relative;overflow:hidden;}
.link-card:hover{transform:translateY(-6px);box-shadow:0 12px 28px rgba(6,182,212,0.12);border-color:#06B6D4;}
.link-card .icon{font-size:26px;margin-bottom:10px;display:inline-block;animation:float 3s ease-in-out infinite;}
.link-card .title{font-weight:800;color:#0d47a1;font-size:15px;margin-bottom:14px;}
.link-card a{display:block;text-align:center;background:linear-gradient(135deg,#0C4A6E,#06B6D4);color:#fff !important;text-decoration:none;font-size:13px;font-weight:700;padding:9px 0;border-radius:8px;transition:all 0.3s ease;box-shadow:0 4px 10px rgba(12,74,110,0.2);border:1px solid rgba(255,255,255,0.1);}
.link-card a:hover{filter:brightness(1.12);transform:translateY(-2px);box-shadow:0 6px 15px rgba(6,182,212,0.4);}

.topbar h2{margin:0;font-size:33px;font-weight:800;color:#fff;}
.topbar p{margin:2px 0 0;font-size:12px;color:#90caf9;text-transform:uppercase;letter-spacing:.05em;}
.topbar-badge{margin-left:auto;background:rgba(255,255,255,.15);color:#fff;font-size:11px;font-weight:700;padding:4px 12px;border-radius:20px;}

.sh{font-size:13px;font-weight:800;color:#0d47a1;text-transform:uppercase;letter-spacing:.08em;margin:22px 0 10px;padding:0 0 8px;border-bottom:2px solid #c5d8f7;}

.kpi{background:#fff;border-radius:14px;padding:22px 18px;text-align:center;border:1px solid #dce8f9;border-top:4px solid #0d47a1;box-shadow:0 2px 8px rgba(13,71,161,.06);transition:transform 0.3s cubic-bezier(0.175,0.885,0.32,1.275),box-shadow 0.3s ease,border-color 0.3s ease;position:relative;overflow:hidden;}
.kpi::after{content:'';position:absolute;top:-50%;left:-50%;width:200%;height:200%;background:linear-gradient(45deg,transparent,rgba(255,255,255,0.4),transparent);transform:translateX(-100%);transition:transform 0.6s ease;pointer-events:none;}
.kpi:hover{transform:translateY(-8px);box-shadow:0 15px 30px rgba(12,74,110,0.15);border-color:#06B6D4;}
.kpi:hover::after{transform:translateX(100%);}
.kpi-val{font-size:42px;font-weight:900;line-height:1;color:#0d47a1;margin-bottom:6px;}
.kpi-lbl{font-size:11px;font-weight:700;color:#78909c;text-transform:uppercase;letter-spacing:.07em;}
.kpi.green{border-top-color:#2e7d32;} .kpi.green .kpi-val{color:#2e7d32;}
.kpi.green:hover{box-shadow:0 15px 30px rgba(46,125,50,0.15);border-color:#2e7d32;}
.kpi.purple{border-top-color:#6a1b9a;} .kpi.purple .kpi-val{color:#6a1b9a;}
.kpi.purple:hover{box-shadow:0 15px 30px rgba(106,27,154,0.15);border-color:#6a1b9a;}
.kpi.amber{border-top-color:#bf360c;} .kpi.amber .kpi-val{color:#bf360c;}
.kpi.amber:hover{box-shadow:0 15px 30px rgba(191,54,12,0.15);border-color:#bf360c;}

div.stLinkButton a{display:block;width:100%;text-align:center;padding:13px 20px !important;border-radius:10px !important;font-size:15px !important;font-weight:700 !important;text-decoration:none !important;color:#fff !important;background:#0d47a1 !important;border:none !important;transition:filter .18s,transform .15s !important;}
div.stLinkButton a:hover{filter:brightness(1.12) !important;transform:translateY(-1px) !important;color:#fff !important;}
[data-testid="column"]:last-child div.stLinkButton a{background:#2e7d32 !important;}

[data-testid="stDataFrame"]{border-radius:12px;overflow:hidden;border:1.5px solid #b0c8f0 !important;animation:fadeInUp 0.8s ease-out forwards;opacity:0;box-shadow:0 4px 12px rgba(0,0,0,0.05);}
[data-testid="stDataFrameContainer"] th{background:#dce8f9 !important;color:#0d47a1 !important;font-weight:800 !important;font-size:12px !important;padding:10px 12px !important;border-bottom:2px solid #90b4e8 !important;}
[data-testid="stDataFrameContainer"] td{font-size:13px !important;padding:9px 12px !important;border-bottom:1px solid #edf2fb !important;}
[data-testid="stDataFrameContainer"] tr:nth-child(even) td{background:#f5f8fe !important;}

div[data-baseweb="select"]>div{background:#fff !important;border:1.5px solid #b0c8f0 !important;border-radius:10px !important;min-height:44px !important;box-shadow:none !important;}
div[data-baseweb="select"]:focus-within>div{border-color:#0d47a1 !important;box-shadow:0 0 0 3px rgba(13,71,161,.1) !important;}

.no-sheet{background:#fce4ec;border:1.5px solid #f48fb1;color:#880e4f;padding:13px 18px;border-radius:10px;font-weight:700;text-align:center;}
.empty-state{background:#fff8e1;border:1.5px solid #ffe082;color:#bf360c;padding:14px;border-radius:10px;font-weight:700;text-align:center;height:100px;animation:fadeInUp 0.5s ease-out;box-shadow:0 4px 15px rgba(252,211,77,0.2);}
.footer-note{margin-top:20px;padding:11px 16px;border-radius:10px;background:#dce8f9;color:#0d47a1;font-size:12px;font-weight:600;display:flex;gap:20px;}
[data-testid="stExpander"]{border:1.5px solid #0d47a1 !important;border-radius:10px !important;}

/* Toast - Glowing Pulse */
.toast{position:fixed;bottom:24px;right:24px;background:linear-gradient(135deg,#0C4A6E,#06B6D4);color:white;padding:18px 26px;border-radius:12px;box-shadow:0 10px 25px rgba(12,74,110,0.3);z-index:9999;transform:translateX(120%);transition:transform 0.4s cubic-bezier(0.175,0.885,0.32,1.275);font-weight:600;display:flex;align-items:center;gap:12px;border:1px solid rgba(255,255,255,0.2);animation:pulseGlow 2.5s infinite;}
.toast.show{transform:translateX(0);}
</style>
""", unsafe_allow_html=True)


# ── TOPBAR ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="topbar">
    <span class="topbar-icon"></span>
    <div><h2>Blue Planet Infosolutions Pvt. Ltd.</h2><p>Intern Task Dashboard</p></div>
   
</div>
""", unsafe_allow_html=True)


# ── LOAD DATA ────────────────────────────────────────────────────────────────
MAIN_SHEET = "https://docs.google.com/spreadsheets/d/1zPkZg6lNEnHDySAIHUBAB8xFbZ7dM7MKN-mlSV8AKnY/export?format=csv"

try:
    with open("data.pkl", "rb") as f:
        df = pickle.load(f)
except Exception as e:
    st.error(f"❌ Error loading data: {e}")
    st.stop()

df = df.iloc[:, 1:]
df.drop(columns=["Google Maps", "Google Maps Link"], errors="ignore", inplace=True)


if 'Date' not in df.columns or 'Intern Name' not in df.columns:
    st.error("Missing required columns: 'Date' or 'Intern Name'")
    st.stop()

df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df = df.dropna(subset=['Date'])

today = pd.Timestamp.now(tz="Asia/Kolkata").date()
df['Date'] = df['Date'].dt.tz_localize(None)
df = df[df['Date'].dt.date <= today].sort_values("Date")
df['Day'] = df['Date'].dt.strftime('%A')
df['Intern Name'] = df['Intern Name'].astype(str).str.strip()


# ── INTERN SHEET LINKS ───────────────────────────────────────────────────────
intern_links = {
    "AT":             "https://docs.google.com/spreadsheets/d/xxxxx",
    "Rahul":          "https://docs.google.com/spreadsheets/d/yyyyy",
    "Harshada Magar": "https://docs.google.com/spreadsheets/d/14m3yRqwbPmHpWmgYxP9RnudDsHPgA3ki0vKeZLUyYwU/edit?usp=sharing",
    "Sreeja M":       "https://docs.google.com/spreadsheets/d/1xOBQkgZMIYjQuHNTttOW1CTLn86j4fRzS7znODu0WHE/edit?usp=sharing",
    "Devatha Siri":   "https://docs.google.com/spreadsheets/d/1saAd0onz12WhMpnCckIqy2tHdVXHst7SvK7y-Ep0gyM/edit?hl=id&gid=0#gid=0",
    "H. Lahari":      "https://docs.google.com/spreadsheets/d/19Ugy_pFKaPZgzKjEiHHhMmBvKFx-Mjf1ixnbOe0QfA4/edit?gid=0#gid=0",
    "Nasiya": "https://docs.google.com/spreadsheets/d/1kPQSAkEn07XLkSlWXmWTkvuFKdZWWKrwi8f5Yy1_aPA/edit?usp=sharing",
    "Zahid": "https://docs.google.com/spreadsheets/d/17VHHSF3oeCxTxUHzrYw77CwJkMt2L_qoUmUR1nk49b0/edit?usp=sharing",
    "Swetha":"https://docs.google.com/spreadsheets/d/1D5nWF-vhN155aZkPfYu2wXGetA4PAdwnjPvpRC5Pom4/edit?usp=sharing",
    "Riya":"https://docs.google.com/spreadsheets/d/1BmGbpYnwOlw6Vjx0voFa4WzIVHvC_-tC5cmuLCXfzck/edit?usp=sharing",
    "Kalyani":"https://docs.google.com/spreadsheets/d/1XgENzr4GJptLUpJTU3qVRITfIaTf1mU5uiy2D7Oxlrw/edit?gid=0#gid=0",
    "Saanvi":"https://docs.google.com/spreadsheets/d/1X1hhc0USSr2X-Mg1QDBNosRm8Fygy0nuV0uVWVjISOw/edit?gid=0#gid=0",
    "Zainab":"https://docs.google.com/spreadsheets/d/1WgOGMKu-cEXd2Bl7d2xTtAPd5ZzLF43G6B514RWNlxg/edit?gid=0#gid=0",
    "Abishek":"https://docs.google.com/spreadsheets/d/1NxjGAuZWVqTlCESNrpTwtAicR2UMECblC_neev3TXTY/edit?gid=0#gid=0",
    "Khushi":"https://docs.google.com/spreadsheets/d/1tKHaXIawLgRxwsV1PBDcogDGONV64a2AcNrSIZ45kXY/edit?gid=0#gid=0",
    "Vidyanand":"https://docs.google.com/spreadsheets/d/1d1Zm0FqO06502POWty34O1okxAJA-FgpvPpThqALDuc/edit?gid=0#gid=0",
    "Saheeb":"https://docs.google.com/spreadsheets/d/1OdQaurem2Mmch7DWzgdTHnrEP_BVPgOaXTWkiHVdyCY/edit?gid=0#gid=0",
    "Afrah":"https://docs.google.com/spreadsheets/d/1xQVxMyCt0O1CQNy4VwZJqZW3WNznwrD2MyB2aPLxHsM/edit?usp=sharing_eip_se_dm&ts=6a435747",
    "Vishvesh":"https://docs.google.com/spreadsheets/d/1yY6mCyf1xvJ9qr0JGk-tAGd4O0asjLMXA3fHNSw7bSU/edit?gid=0#gid=0",
    "Anshika":"https://docs.google.com/spreadsheets/d/1qYQ0k7fr5ft30k9Thq1bWL0OZGN_qWXVwgDOxhC74Rg/edit?gid=0#gid=0",
    
}

def is_valid_link(url):
    return url and "xxxxx" not in url and "yyyyy" not in url

def sheet_csv_url(link):
    try:
        sid = link.split("/d/")[1].split("/")[0]
        return f"https://docs.google.com/spreadsheets/d/{sid}/export?format=csv"
    except Exception:
        return None

intern_ids = {
    "AT":             1,
    "Rahul":          2,
    "Harshada Magar": 3438073,
    "Sreeja M":       3420257,
    "Devatha Siri":   3437858,
    "H. Lahari":      3437861,
    "Nasiya":         3489116,
    "Zahid":          3489114,
    "Swetha":         3489115,
    "Riya":           3489117,
    "Kalyani":        3489111,
    "Saanvi":         3489118,
    "Zainab":         3489797,
    "Abishek":        3489176,
    "Khushi":"",
    "Vidyanand":""   ,
    "Saheeb":"",
    "Afrah":"",
    "Vishvesh":"",
    "Anshika":"",
}
weekend_warrior_interns = {
    "Zainab",
    "Saheeb",
    "Zahid",
    "Afrah",
    "Nasiya",
            
    # add exact intern names here that should get the tag
}

def format_intern_name(name):
    return f"{name} (Weekend Warrior) " if name.strip() in weekend_warrior_interns else name


def get_day_clubs_count(csv_url, date_):
    """Count club rows collected on a specific date from intern's data sheet."""
    try:
        sheet_df = load_sheet_csv(csv_url)
    except Exception:
        return 0, 0
    total = len(sheet_df)
    date_col = None
    for c in ["Timestamp", "Date", "Submitted Date", "Submission Date", "Collected Date"]:
        if c in sheet_df.columns:
            date_col = c
            break
    if date_col is None:
        return total, 0
    sheet_df[date_col] = pd.to_datetime(sheet_df[date_col], errors="coerce")
    day_count = len(sheet_df[sheet_df[date_col].dt.date == date_])
    return total, day_count
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    ["📊 Dashboard","🔗 Links","Email Format","Analysis Task","ℹ️ Guide","🧑‍💼 Sub Leader"]
)

with tab1:

# ── FILTERS ──────────────────────────────────────────────────────────────────
    st.markdown('<div class="sh">🔍 &nbsp;Filters</div>', unsafe_allow_html=True)
    f1, f2 = st.columns([2, 2])

    with f1:
        intern = st.selectbox(
            "Select Intern",
            sorted(df['Intern Name'].unique()),
            label_visibility="visible"
        )

    with f2:
        selected_date = st.date_input("Select Date", value=today)

    intern_df = df[df['Intern Name'] == intern].sort_values('Date')

    # ── MERGE CLUBS COUNT INTO TASK TABLE ────────────────────────────────────────
    if is_valid_link(intern_links.get(intern.strip(), "")):
        csv_url = sheet_csv_url(intern_links.get(intern.strip(), ""))
        if csv_url:
            try:
                _idf = load_sheet_csv(csv_url)
                _idf['SchoolID'] = _idf['SchoolID'].astype(str).str.strip()
                clubs_count = _idf.groupby('SchoolID').size().reset_index(name='Clubs Collected')
                intern_df = intern_df.copy()
                intern_df['SchoolID'] = intern_df['SchoolID'].astype(str).str.strip()
                intern_df = intern_df.merge(clubs_count, on='SchoolID', how='left')
                intern_df['Clubs Collected'] = intern_df['Clubs Collected'].fillna(0).astype(int)
            except Exception:
                intern_df['Clubs Collected'] = 0
    else:
        intern_df['Clubs Collected'] = 0


    # ── CLUB COUNT ───────────────────────────────────────────────────────────────
    sheet_task_count = 0
    distinct_contacts = 0
    distinct_emails = 0
    sheet_url = intern_links.get(intern.strip(), "")

    if is_valid_link(sheet_url):
        csv_url = sheet_csv_url(sheet_url)
        if csv_url:
            try:
                intern_sheet_df = load_sheet_csv(csv_url)
                sheet_task_count = len(intern_sheet_df)
                if 'ClubContactNumber' in intern_sheet_df.columns:
                    distinct_contacts = intern_sheet_df['ClubContactNumber'].dropna().astype(str).str.strip().replace('', pd.NA).dropna().nunique()
                if 'ClubEmail' in intern_sheet_df.columns:
                    distinct_emails = intern_sheet_df['ClubEmail'].dropna().astype(str).str.strip().replace('', pd.NA).dropna().nunique()
            except Exception:
                sheet_task_count = 0

    # ── KPIs ─────────────────────────────────────────────────────────────────────
    st.markdown('<div class="sh">📊 &nbsp;Overview</div>', unsafe_allow_html=True)

    task_count  = len(intern_df)
    today_tasks = len(intern_df[intern_df['Date'].dt.date == today])
    active_days = intern_df['Date'].dt.date.nunique()

    k1, k2, k3, k4, k5, k6 = st.columns(6)
    with k1:
        st.markdown(f'<div class="kpi blue"><div class="kpi-val">{task_count}</div><div class="kpi-lbl">Total Tasks</div></div>', unsafe_allow_html=True)
    with k2:
        st.markdown(f'<div class="kpi green"><div class="kpi-val">{today_tasks}</div><div class="kpi-lbl">Today\'s Tasks</div></div>', unsafe_allow_html=True)
    with k3:
        st.markdown(f'<div class="kpi purple"><div class="kpi-val">{sheet_task_count}</div><div class="kpi-lbl">Total Clubs Collected</div></div>', unsafe_allow_html=True)
    with k4:
        st.markdown(f'<div class="kpi amber"><div class="kpi-val">{active_days}</div><div class="kpi-lbl">Active Days</div></div>', unsafe_allow_html=True)
    with k5:
        st.markdown(f'<div class="kpi green"><div class="kpi-val">{distinct_contacts} </div><div class="kpi-lbl">Distinct Contacts ({(distinct_contacts / sheet_task_count) * 100:.2f}%)</div></div>', unsafe_allow_html=True)
    with k6:
        st.markdown(f'<div class="kpi purple"><div class="kpi-val">{distinct_emails}</div><div class="kpi-lbl">Distinct Emails ({(distinct_emails / sheet_task_count) * 100:.2f}%)</div></div>', unsafe_allow_html=True)

    # ── TASK TABLE ───────────────────────────────────────────────────────────────
    st.markdown('<div class="sh">📋 &nbsp;Task Details</div>', unsafe_allow_html=True)

    day_result = intern_df[intern_df['Date'].dt.date == selected_date]

    if not day_result.empty:
        display_result = day_result.copy()
        display_result['Date'] = display_result['Date'].dt.strftime('%d-%b-%Y')
        st.dataframe(display_result, use_container_width=True, hide_index=True)
    else:
        st.markdown(
            '<div class="empty-state">⚠️ Task: Club contact details and email are missing. Kindly collect them </div>',
            unsafe_allow_html=True
        )


    # ── ACTION BUTTONS ───────────────────────────────────────────────────────────
    st.markdown('<div class="sh">🔗 &nbsp;Quick Actions</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if is_valid_link(sheet_url):
                st.link_button("📊 Open Your Data Sheet", sheet_url, use_container_width=True)
        else:
            st.markdown('<div class="no-sheet">⚠️ Spreadsheet Not Submitted</div>', unsafe_allow_html=True)
    with c2:
        st.link_button("📝 Mark Attendance", "https://docs.google.com/forms/d/e/1FAIpQLScHz7fdRGl0RbMTyh_8N5VH9G0K1LDsszsZRqwHMe9CsXcqlA/viewform", use_container_width=True)


    # ── INTERN SHEET DATA ────────────────────────────────────────────────────────
    if is_valid_link(sheet_url):
        csv_url = sheet_csv_url(sheet_url)
        if csv_url:
            st.markdown('<div class="sh">📂 &nbsp;Collected Data</div>', unsafe_allow_html=True)
            with st.expander(f"📄 View {intern}'s Sheet"):
                try:
                    intern_sheet_df = pd.read_csv(csv_url)
                    st.dataframe(intern_sheet_df, use_container_width=True, hide_index=True)
                except Exception:
                    st.error("Unable to load sheet data.")

    intern_id = intern_ids.get(intern.strip(), "")
    # ── PROMPT BUILDER ───────────────────────────────────────────────────────────
    st.markdown('<div class="sh">🧠 &nbsp;Prompt Builder</div>', unsafe_allow_html=True)

    institutes = day_result[['Institute Name','SchoolID']].dropna(subset=['Institute Name']).drop_duplicates().values.tolist() if not day_result.empty else []
    with st.expander("Click an institute to generate a research prompt"):
        if not institutes:
            st.warning("No institute names found for the selected date.")
        else:
            cols = st.columns(min(len(institutes), 5))
            for i, (inst, school_id) in enumerate(institutes):
                with cols[i % 5]:
                    if st.button(f"🏫 {inst}", key=f"pb_{i}", use_container_width=True):
                        prompt = f"""You are a web research agent with live browsing access.

    Your ONLY job: find every student club, committee, cell,

    association, and organization at {inst} and output a table.

    NO explanations. NO excuses. NO asking for more info.

    If a field is not found after exhaustive search, leave it blank. Start the table immediately.

    ════════════════════════════════

    STEP 1 — SEARCH (do this silently)

    ════════════════════════════════

    Search the web for ALL of the following one by one:

    "{inst} student clubs"
    "{inst} student organizations"
    "{inst} technical clubs"
    "{inst} cultural clubs"
    "{inst} NSS NCC"
    "{inst} IEEE ISTE CSI ACM chapter"
    "{inst} entrepreneurship cell innovation cell"
    "{inst} coding club robotics club"
    "{inst} dance music drama club"
    "{inst} photography literary club"
    "{inst} placement committee student council"
    "{inst} women development cell"
    "{inst} environment club"
    "{inst} fest committee"
    "{inst} committees cells"
    "{inst} clubs site:instagram.com"
    "{inst} clubs site:linkedin.com"
    "{inst} annual report filetype:pdf"
    "{inst} NAAC report filetype:pdf"

    Also directly visit:
    Official college website homepage
    [college website]/clubs
    [college website]/committees
    [college website]/student-activities
    [college website]/nss
    [college website]/ncc

    ────────────────────────────────
    STEP 1B — MANDATORY CONTACT/EMAIL/LEADERSHIP SEARCH (per club)
    ────────────────────────────────

    For EVERY club identified in Step 1, before writing its row, run an additional targeted search pass to find its ClubContactNumber, ClubEmail, ClubWebsite, ClubPresidentName, and ClubPresidentContact. Do not skip this pass even if Step 1 already surfaced a name for the club.

    For each club, search:
    "[Club Name] {inst} contact"
    "[Club Name] {inst} email"
    "[Club Name] {inst} president OR convenor OR coordinator"
    "[Club Name] {inst} president contact"
    "[Club Name] {inst} Instagram OR LinkedIn OR website"
    site:instagram.com "[Club Name]" {inst}
    site:linkedin.com "[Club Name]" {inst}

    Also check:
    - The club's listing on [college website]/clubs or /committees (often has a contact block)
    - The college's official social media bio/link tree for club sub-pages
    - Any fest or department page that lists club coordinators' or presidents' contact details
    - Official club/society leadership pages, "office bearers" or "team" pages

    These five fields — ClubContactNumber, ClubEmail, ClubWebsite, ClubPresidentName, ClubPresidentContact — are REQUIRED fields — do not treat them as optional. Every club row must show a genuine, verified value in these columns whenever such information exists anywhere online. Only leave them blank if, after this dedicated search pass, no such information could be found anywhere. Never guess, construct, or infer a plausible-looking number, email, name, or URL — an invented value is worse than a blank one.

    ════════════════════════════════

    STEP 2 — OUTPUT TABLE (immediately after searching)

    ════════════════════════════════

    Output one row per club. All 26 columns, every row, no exceptions.

    | GroupMemberID | SchoolID | ClubID | SchoolClubID | ClubName | ClubSchoolName | ClubDescription | ClubCategoryID | ClubStatus | ClubContactNumber | ClubLocation | ClubWebsite | ClubEmail | SocialLinks | ClubImagePath | PrimarySponsorID | PrimarySponsorName | ClubBudget | ClubPresidentID | ClubPresidentName | ClubPresidentPRN | ClubPresidentContact | ClubMentorID | ClubMentorName | DataCollectedByID | DataCollectedByName |

    COLUMN RULES:

    GroupMemberID → always set to 6
    SchoolID → always set to {school_id}
    ClubID → leave blank
    SchoolClubID → generate using the initials of {inst} + a 3-digit sequential number padded with zeros.

    INITIALS RULE: Take the first letter of each significant word in the college name (skip common words like "of", "and", "the", "for"). Then append 001, 002, 003… for each club.

    Examples:

    → "Christian College of Engineering and Technology" → CCET001, CCET002, CCET003…

    → "Government Polytechnic Mungeli" → GPM001, GPM002, GPM003…

    → "Indian Institute of Technology Bombay" → IITB001, IITB002…

    → "Dr. Ambedkar Institute of Technology" → DAIT001, DAIT002…

    ClubName → official full name of the club
    ClubSchoolName → common short name or abbreviation
    ClubDescription → one sentence describing the club's purpose
    ClubCategoryID → use one of: Technical, Cultural, Social, Sports, Literary, Entrepreneurship, Professional, Other
    ClubStatus → Active (default unless known otherwise)
    ClubContactNumber → MANDATORY — search exhaustively per Step 1B; only found real values, never invent; leave blank only if truly unfindable
    ClubLocation → college name and address
    ClubWebsite → MANDATORY — search exhaustively per Step 1B; only found real URLs (official page or social media), never invent; leave blank only if truly unfindable
    ClubEmail → MANDATORY — search exhaustively per Step 1B; only found real emails, never invent; leave blank only if truly unfindable
    SocialLinks → only if found; never invent
    ClubImagePath → leave blank
    PrimarySponsorID → leave blank
    PrimarySponsorName → sponsoring body if known (e.g. Ministry of Youth Affairs, IEEE, AICTE)
    ClubBudget → leave blank
    ClubPresidentID → leave blank
    ClubPresidentName → MANDATORY — search exhaustively per Step 1B; only found real names, never invent; leave blank only if truly unfindable
    ClubPresidentPRN → only if found; never invent
    ClubPresidentContact → MANDATORY — search exhaustively per Step 1B; only found real phone numbers or emails, never invent; leave blank only if truly unfindable
    ClubMentorID → leave blank
    ClubMentorName → only if found; never invent
    DataCollectedByID → always set to {intern_ids}
    DataCollectedByName → always set to {intern}

    STRICT RULES:

    ✗ Never invent names, emails, phone numbers, or URLs — even to satisfy a mandatory field
    ✗ Never write "BLANK" — just leave the cell empty
    ✗ Never truncate the table
    ✗ Never skip the Step 1B search pass for any club, including ones found late in Step 1
    ✓ Blank cells for ClubContactNumber/ClubEmail/ClubWebsite/ClubPresidentName/ClubPresidentContact are acceptable ONLY after the mandatory search pass turns up nothing

    After the table write:

    Total clubs found: [N]
    Sources visited: [list]
    Clubs with incomplete data: [N]
    Clubs missing contact/email/website/president info after mandatory search: [N]
    """
                        st.components.v1.html(f"""
    <textarea id="prompt-box" style="width:100%;height:200px;font-family:monospace;font-size:12px;padding:10px;border:1px solid #b0c8f0;border-radius:10px;resize:vertical;background:#f8faff;color:#1a1a2e">{prompt}</textarea>
    <button onclick="
    navigator.clipboard.writeText(document.getElementById('prompt-box').value);
    this.textContent='✅ Copied!';
    this.style.background='#2e7d32';
    setTimeout(()=>{{this.textContent='📋 Copy Prompt';this.style.background='#0d47a1'}},2000)
    " style="margin-top:8px;width:100%;padding:10px;background:#0d47a1;color:white;border:none;border-radius:8px;font-size:14px;font-weight:700;cursor:pointer">📋 Copy Prompt</button>
    """, height=280)


    # ── FOOTER NOTE ──────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="footer-note">
        <span>✔ After completing tasks, report to Team Leader</span>
        <span>✔ Share updates in communication group for HR tracking</span>
    </div>
    """, unsafe_allow_html=True)

with tab2:
    st.markdown(
        '<div class="sh">🔗 &nbsp;Important Links</div>',
        unsafe_allow_html=True
    )

    important_links = [
        {
            "title": "Startup Wolrd",
            "icon": "",
            "url": "https://startupworld.in/"
        },
        {
            "title": "Smart-Cookie",
            "icon": "",
            "url": "https://smartcookie.in/"
        },
        {
            "title": "Continous Job Network(CJN)",
            "icon": "",
            "url": "https://cjnnow.com/"
        },
      
    ]

    cards_html = '<div class="link-grid">'

    cards_html = '<div class="link-grid">'

    for item in important_links:
        cards_html += (
            f'<div class="link-card">'
            f'<div class="icon">{item["icon"]}</div>'
            f'<div class="title">{item["title"]}</div>'
            f'<a href="{item["url"]}" target="_blank">Open Link ↗</a>'
            f'</div>'
        )

    cards_html += "</div>"

    st.markdown(cards_html, unsafe_allow_html=True)
    st.markdown(
        '<div class="sh">🔗 &nbsp;Meeting Links</div>',
        unsafe_allow_html=True
    )

    important_links = [
        {
            "title": "JRS",
            "icon": "",
            "url": "https://meet.google.com/exu-yrsk-jrs"
        },
        {
            "title": "PIX",
            "icon": "",
            "url": "https://meet.google.com/wap-gkof-pix"
        },
       
      
    ]

    cards_html = '<div class="link-grid">'

    cards_html = '<div class="link-grid">'

    for item in important_links:
        cards_html += (
            f'<div class="link-card">'
            f'<div class="icon">{item["icon"]}</div>'
            f'<div class="title">{item["title"]}</div>'
            f'<a href="{item["url"]}" target="_blank">Open Link ↗</a>'
            f'</div>'
        )

    cards_html += "</div>"
    st.markdown(cards_html, unsafe_allow_html=True)
    st.markdown(
        '<div class="sh">🔗 &nbsp;Other Links</div>',
        unsafe_allow_html=True
    )

    important_links = [
        {
            "title": "Club Email Send",
            "icon": "",
            "url": "https://autoemail.smartcookie.in/"
        },
       
       
      
    ]

    cards_html = '<div class="link-grid">'

    cards_html = '<div class="link-grid">'

    for item in important_links:
        cards_html += (
            f'<div class="link-card">'
            f'<div class="icon">{item["icon"]}</div>'
            f'<div class="title">{item["title"]}</div>'
            f'<a href="{item["url"]}" target="_blank">Open Link ↗</a>'
            f'</div>'
        )

    cards_html += "</div>"

    st.markdown(cards_html, unsafe_allow_html=True)
import re
import pydeck as pdk
    
# import re 

with tab4:
    st.markdown('<div class="sh">🗺️ &nbsp;Location Analysis</div>', unsafe_allow_html=True)

    # Add more interns here: "Name": (sheet_url, sheet_tab_name)
    location_sheets = {
        "Harshada": ("https://docs.google.com/spreadsheets/d/1gWNeGKM505eOz87wGod13-JBBR7azJt5haa69WxOiCk/edit", "Harshada"),
        "Riya": ("https://docs.google.com/spreadsheets/d/1-l7ZuZuNcP81XPZewwU70L-8cRVzYtNrNN4RF1FjSnU/edit", "Riya"),
    }

    loc_intern = st.selectbox("Select Intern", list(location_sheets.keys()), key="loc_intern")
    sheet_url, sheet_name = location_sheets[loc_intern]

    @st.cache_data(ttl=300)
    def load_sheet(url, sheet_name):
        sid = re.search(r"/d/([a-zA-Z0-9-_]+)", url).group(1)
        return pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sid}/gviz/tq?tqx=out:csv&sheet={sheet_name}")

    df4 = load_sheet(sheet_url, sheet_name)

    if {"Sum of Latitude", "Sum of Longitude"}.issubset(df4.columns):
        df4["lat"] = pd.to_numeric(df4["Sum of Latitude"], errors="coerce")
        df4["lon"] = pd.to_numeric(df4["Sum of Longitude"], errors="coerce")
    else:
        def extract_lat_lon(url):
            if pd.isna(url):
                return None, None
            url = str(url)

            if "goo.gl" in url or "maps.app" in url:
                try:
                    import requests
                    resp = requests.get(url, allow_redirects=True, timeout=5)
                    url = resp.url
                except Exception:
                    pass

            m = re.search(r"!3d(-?\d+\.\d+)!4d(-?\d+\.\d+)", url)
            if m:
                return float(m.group(1)), float(m.group(2))

            m = re.search(r"@(-?\d+\.\d+),(-?\d+\.\d+)", url)
            if m:
                return float(m.group(1)), float(m.group(2))

            return None, None

        df4[["lat", "lon"]] = df4["Google Maps Link"].apply(lambda x: pd.Series(extract_lat_lon(x)))

    df4 = df4.dropna(subset=["lat", "lon"])

    if df4.empty:
        st.warning(f"⚠️ No valid location data found for **{loc_intern}**. Check the sheet name/columns.")
        st.stop()

    # ── TASK / INSTRUCTIONS PANEL (replaces KPI metrics) ──────────────────────
    st.markdown('<div class="sh">🧭 &nbsp;Dashboard Structure to Replicate</div>', unsafe_allow_html=True)

    spec_html = (
'<div class="link-card" style="animation:none;opacity:1;padding:24px 28px;">'
'<div class="title" style="font-size:17px;margin-bottom:16px;">🏫 Club Dashboard — Build Spec</div>'
'<div style="font-size:13.5px;color:#37474f;line-height:1.7;">'

'<b style="color:#0d47a1;">Title:</b> "Club Dashboard" (top-left, bold heading)<br><br>'

'<b style="color:#0d47a1;">Row 1 — Filter + 5 KPI Cards (top of page):</b>'
'<ul style="margin-top:6px;">'
'<li>Dropdown filter: <b>College Name</b> (with "All" option)</li>'
'<li>Card 1: Total Colleges (count)</li>'
'<li>Card 2: Total States (count)</li>'
'<li>Card 3: Total Clubs (count)</li>'
'<li>Card 4: Total Emails (count)</li>'
'<li>Card 5: Total Contacts (count)</li>'
'</ul>'

'<b style="color:#0d47a1;">Row 2 — 3 panels:</b>'
'<ol style="margin-top:6px;">'
'<li><b>Map visual</b> (left, largest): plots colleges by City/Latitude/Longitude, color-coded by city</li>'
'<li><b>Table</b> (middle): Top 10 Sponsors — columns: Sponsor Name, Count, with a Total row</li>'
'<li><b>2 stacked Gauge charts</b> (right):'
'<ul>'
'<li>Gauge A: Avg clubs per college (with min/max range)</li>'
'<li>Gauge B: % Clubs with Contact &amp; Email (with min/max range)</li>'
'</ul>'
'</li>'
'</ol>'

'<b style="color:#0d47a1;">Row 3 — 3 panels:</b>'
'<ol style="margin-top:6px;">'
'<li><b>Vertical bar chart</b> (left): Club count by individual Club Name (ranked, descending)</li>'
'<li><b>Horizontal bar chart</b> (middle): Club count by Club Category</li>'
'<li><b>Table</b> (right): Category-wise breakdown — columns: Category, Total Club Count, with a Total row</li>'
'</ol>'

'</div>'
'</div>'
    )

    st.markdown(spec_html, unsafe_allow_html=True)

    cols = [c for c in ["College Name", "City", "District", "State", "lat", "lon"] if c in df4.columns]
    st.subheader("College Details")
    st.dataframe(df4[cols], use_container_width=True, hide_index=True)

    st.subheader("📍 College Locations")
    m = folium.Map(location=[df4["lat"].mean(), df4["lon"].mean()], zoom_start=6, tiles="OpenStreetMap")
    for _, row in df4.iterrows():
        popup = f"<b>{row['College Name']}</b><br>City: {row.get('City','')}<br>District: {row.get('District','')}<br>State: {row.get('State','')}"
        folium.Marker([row["lat"], row["lon"]], popup=popup, tooltip=row["College Name"],
                      icon=folium.Icon(color="red", icon="glyphicon-education", prefix="glyphicon")).add_to(m)
    st_folium(m, width=None, height=650)

    with st.expander("🔍 Debug Coordinates"):
        st.dataframe(df4[["College Name", "lat", "lon"]], use_container_width=True, hide_index=True)



with tab3:
    st.markdown("")

    sender_names =  ["Tade A Rehman",
    "Harshada Magar",
    "Zahid Khan",
    "P. R. Nasiya",
    "Appireddipally Swetha",
    "Riya Chand",
    "Kalyani Pawar",
    "Saanvi Gothe",
    "Abishek Sharma",
    "Zainab Rahman",
    "Khushi Singh",
    "Vidyanand Prasad",
    "Afrah Ashraf",
    "Vishvesh Kashyap",
    "Anshika Verma",
]  # 👈 add/edit names in this list
    
    

    

    text1 = "aictefdc360@smartcookie.in (default)"

    st.markdown(
    f"""
    <div style="margin-bottom:4px;font-weight:600;margin-top:7px; margin-left:4px;font-weight:800;color:#0d47a1;text-transform:uppercase;letter-spacing:.08em;">
        Send From
    </div>

    <div style="
        padding:10px;
        border:1px solid #b0c8f0;
        border-radius:10px;
        background:#f8faff;
        font-family:'Serif';
        font-size:14px;
        margin-top:0;
    ">
        {text1}
    </div>
    """,
        unsafe_allow_html=True,
    )
    
    
    text2 ="Club Outreach India"
    # st.markdown("")
    st.markdown(
    f"""
    <div style="margin-bottom:4px;font-weight:600;margin-top:7px; margin-left:4px;font-weight:800;color:#0d47a1;text-transform:uppercase;letter-spacing:.08em;">
        Campaign name
    </div>

    <div style="
        padding:10px;
        border:1px solid #b0c8f0;
        border-radius:10px;
        background:#f8faff;
        font-family:'Serif';
        font-size:14px;
        margin-top:0;
    ">
        {text2}
    </div>
    """,
        unsafe_allow_html=True,
    )
    text3 ="Invitation to Explore Student Club Collaboration with Avi Kulkarni – Smart Cookie & CJN"
    FONT = "Georgia, serif"

# ---------- Subject ----------
    st.markdown(
        f"""
        <div style="width:100%; box-sizing:border-box; margin-top:7px; font-family:{FONT} !important;">
            <div style="
                font-family:{FONT} !important;
                font-weight:800;
                font-size:14px;
                color:#0d47a1;
                text-transform:uppercase;
                letter-spacing:.08em;
                margin:0 0 6px 0;
            ">Subject</div>
            <div style="
                box-sizing:border-box;
                width:100%;
                padding:10px;
                border:1px solid #b0c8f0;
                border-radius:10px;
                background:#f8faff;
                font-family:{FONT} !important;
                font-size:14px;
                color:#1a1a2e;
            "><span style="font-family:{FONT} !important;">{text3}</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c="""{{club_name}}"""
    s="""{{intern_name}}"""

    text4 = f"""<body style="margin:0; padding:0; background-color:#eef1f5; font-family:'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace;">

<!-- Preheader (hidden preview text) -->
<div style="display:none; max-height:0; overflow:hidden; opacity:0;">
Mr. Avi Kulkarni would like to schedule a short call to explore collaboration opportunities with your club.
</div>

<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color:#eef1f5; padding:32px 16px;">
<tr>
<td align="center">

<table role="presentation" width="600" cellpadding="0" cellspacing="0" style="max-width:600px; width:100%; background-color:#ffffff; border-radius:10px; overflow:hidden; box-shadow:0 2px 10px rgba(15,32,67,0.08);">

  <!-- Header / letterhead -->
  <tr>
    <td style="background-color:#0f2043; padding:28px 40px;">
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0">
        <tr>
          <td style="font-family:Arial, Helvetica, sans-serif; color:#ffffff; font-size:20px; font-weight:bold; letter-spacing:0.3px;">
            Smart Rewards Inc.
          </td>
          <td align="right" style="font-family:Arial, Helvetica, sans-serif; color:#9fb0cc; font-size:12px; letter-spacing:1px; text-transform:uppercase;">
            Campus Outreach
          </td>
        </tr>
      </table>
    </td>
  </tr>

  <!-- Accent line -->
  <tr>
    <td style="height:4px; background-color:#c98a3e; line-height:0; font-size:0;">&nbsp;</td>
  </tr>

  <!-- Body -->
  <tr>
    <td style="padding:36px 40px 8px 40px; font-family:Arial, Helvetica, sans-serif; color:#26324a; font-size:14px; line-height:1.65;">

      <p style="margin:0 0 18px 0;">Dear <strong>{c}</strong> Team,</p>

      <p style="margin:0 0 18px 0;">Greetings from Smart Rewards Inc.</p>

      <p style="margin:0 0 18px 0;">
        My name is <strong>{s}</strong>, and I am part of the Campus Outreach Team at Smart Rewards Inc.
      </p>

      <p style="margin:0 0 18px 0;">
        I am writing on behalf of <strong>Mr. Avi Kulkarni</strong>, Founder of Smart Rewards Inc., who has been working with educational institutions, students, startups, and industry leaders to create opportunities that bridge the gap between education and employment.
      </p>

      <p style="margin:0 0 26px 0;">
        Mr. Kulkarni would appreciate the opportunity to have a brief <strong>20–30 minute conference call</strong> with you to learn more about your student club and discuss possible collaboration in the areas of internships, entrepreneurship, AI, career development, innovation, and industry engagement.
      </p>

      <p style="margin:0 0 14px 0;">To introduce our work, here is brief information on two of our initiatives:</p>

    </td>
  </tr>

  <!-- Initiative cards -->
  <tr>
    <td style="padding:0 40px 8px 40px;">
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border-collapse:separate;">
        <tr>
          <td style="padding:16px 18px; background-color:#f5f7fb; border-left:3px solid #0f2043; border-radius:6px;">
            <table role="presentation" width="100%" cellpadding="0" cellspacing="0">
              <tr>
                <td style="font-family:Arial, Helvetica, sans-serif; font-size:14px; color:#0f2043; font-weight:bold; padding-bottom:4px;">
                  <a href="https://smartcookie.in/" target="_blank" style="color:#0f2043; text-decoration:none;">Smart Cookie</a>
                </td>
              </tr>
              <tr>
                <td style="font-family:Arial, Helvetica, sans-serif; font-size:13px; color:#4b5876; line-height:1.55;">
                  A student engagement platform that recognizes participation in academic, extracurricular, leadership, volunteering, innovation, and skill-development activities through a structured rewards ecosystem.
                </td>
              </tr>
            </table>
          </td>
        </tr>
        <tr><td style="height:14px; line-height:14px; font-size:0;">&nbsp;</td></tr>
        <tr>
          <td style="padding:16px 18px; background-color:#f5f7fb; border-left:3px solid #c98a3e; border-radius:6px;">
            <table role="presentation" width="100%" cellpadding="0" cellspacing="0">
              <tr>
                <td style="font-family:Arial, Helvetica, sans-serif; font-size:14px; color:#0f2043; font-weight:bold; padding-bottom:4px;">
                  <a href="https://cjnnow.com/" target="_blank" style="color:#0f2043; text-decoration:none;">CJN — Continuous Job Network</a>
                </td>
              </tr>
              <tr>
                <td style="font-family:Arial, Helvetica, sans-serif; font-size:13px; color:#4b5876; line-height:1.55;">
                  An AI-powered platform designed to continuously connect students with internships, employers, startup opportunities, career guidance, skill-development resources, and industry insights.
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
    </td>
  </tr>

  <!-- Continued body -->
  <tr>
    <td style="padding:24px 40px 8px 40px; font-family:Arial, Helvetica, sans-serif; color:#26324a; font-size:14px; line-height:1.65;">
      <p style="margin:0 0 18px 0;">
        We believe your students could benefit from exposure to these initiatives, and we would welcome the opportunity to explore how we might work together with your club and institution.
      </p>
      <p style="margin:0 0 8px 0;">
        If convenient, could you kindly suggest a few suitable time slots for a conference call with Mr. Kulkarni during the coming week? I will coordinate the meeting at your convenience.
      </p>
    </td>
  </tr>
  <tr>
    <td style="height:24px; line-height:0; font-size:0;">&nbsp;</td>
  </tr>

  <!-- Divider -->
  <tr>
    <td style="padding:0 40px;">
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0">
        <tr><td style="border-top:1px solid #e4e8f0; line-height:0; font-size:0;">&nbsp;</td></tr>
      </table>
    </td>
  </tr>

  <!-- Sign-off -->
  <tr>
    <td style="padding:24px 40px 8px 40px; font-family:Arial, Helvetica, sans-serif; color:#26324a; font-size:14px; line-height:1.6;">
      <p style="margin:0;">Thank you for your time and consideration. We look forward to the opportunity to connect with you.</p>
    </td>
  </tr>

  <tr>
    <td style="padding:20px 40px 36px 40px; font-family:Arial, Helvetica, sans-serif; color:#26324a; font-size:14px; line-height:1.6;">
      <p style="margin:0;">Warm regards,</p>
      <p style="margin:12px 0 0 0; font-weight:bold; color:#0f2043;">{s}</p>
      <p style="margin:2px 0 14px 0; color:#4b5876; font-size:13px;">Campus Outreach Team, Smart Rewards Inc.</p>

      <p style="margin:0; color:#8b95ab; font-size:11px; text-transform:uppercase; letter-spacing:0.5px;">On behalf of</p>
      <p style="margin:4px 0 0 0; font-weight:bold; color:#0f2043; font-size:14px;">
        Avi Kulkarni <span style="font-weight:normal; color:#4b5876; font-size:13px;">— Founder</span>
      </p>
      <p style="margin:2px 0 0 0; font-size:13px;">
        <a href="mailto:avi@smartrewardsinc.com" style="color:#0f2043; text-decoration:none;">avi@smartrewardsinc.com</a>
      </p>
    </td>
  </tr>

  <!-- Footer -->
  <tr>
    <td style="background-color:#f5f7fb; padding:18px 40px; text-align:center; font-family:Arial, Helvetica, sans-serif; font-size:11px; color:#8b95ab;">
      Smart Rewards Inc. &nbsp;•&nbsp; Bridging Education and Employment
    </td>
  </tr>

</table>

</td>
</tr>
</table>

</body>
"""

    # ---------- Campaign name ----------
    st.components.v1.html(
        f"""
        <html>
        <head>
        <style>
            * {{
                box-sizing:border-box;
                font-family:{FONT} !important;
            }}
            html, body {{
                margin:0;
                padding:0;
                width:100%;
                font-family:{FONT} !important;
            }}
            .wrap {{
                width:100%;
                margin-top:7px;
            }}
            .label {{
                font-family:{FONT} !important;
                font-weight:800;
                font-size:14px;
                color:#0d47a1;
                text-transform:uppercase;
                letter-spacing:.08em;
                margin:0 0 6px 0;
            }}
            textarea {{
                font-family:{FONT} !important;
                box-sizing:border-box;
                width:100%;
                padding:10px;
                border:1px solid #b0c8f0;
                border-radius:10px;
                background:#f8faff;
                font-size:14px;
                color:#1a1a2e;
                height:220px;
                resize:vertical;
                display:block;
            }}
            button {{
                font-family:{FONT} !important;
                width:100%;
                box-sizing:border-box;
                margin-top:8px;
                padding:10px;
                background:#0d47a1;
                color:white;
                border:none;
                border-radius:8px;
                font-size:14px;
                font-weight:700;
                cursor:pointer;
            }}
        </style>
        </head>
        <body>
        <div class="wrap">
            <div class="label">Body</div>
            <textarea id="prompt-box" readonly>{text4}</textarea>
            <button onclick="
                navigator.clipboard.writeText(document.getElementById('prompt-box').value);
                this.textContent='✅ Copied!';
                this.style.background='#2e7d32';
                setTimeout(() => {{
                    this.textContent='📋 Copy Prompt';
                    this.style.background='#0d47a1';
                }}, 2000);
            ">📋 Copy Body</button>
        </div>
        </body>
        </html>
        """,
        height=300,
    ) 

    st.markdown('<div class="sh">📥 &nbsp;Attachments</div>', unsafe_allow_html=True)

    st.markdown("""
    <style>
    div.stDownloadButton button{width:100%;text-align:center;padding:13px 20px !important;border-radius:10px !important;font-size:15px !important;font-weight:700 !important;color:#fff !important;background:#0d47a1 !important;border:none !important;transition:filter .18s,transform .15s !important;}
    div.stDownloadButton button:hover{filter:brightness(1.12) !important;transform:translateY(-1px) !important;color:#fff !important;}
    </style>
    """, unsafe_allow_html=True)

    files = [
        ("📄", "Smartcookie PDF", "SmartCookie_Writeup_20251209_RK1.pdf", "application/pdf"),
        ("📄", "CJN PDF", "CJN_AI_WriteUp_20251209_RK2.pdf", "application/pdf"),
        ("🖼️", "Smartcookie Flow Chart Image", "SmartcookieFlowchart.jpg", "image/jpeg"),
    ]
    links = [
        ("🎬", "CJN Video", "https://drive.google.com/file/d/16guetxkYPvsA4hvYhSpKSis7dZyvNF57/view"),
    ]

    cols = st.columns(len(files) + len(links))
    for col, (icon, label, path, mime) in zip(cols, files):
        with col:
            if os.path.exists(path):
                with open(path, "rb") as f:
                    st.download_button(f"{icon} {label}", f, file_name=path, mime=mime, use_container_width=True)
            else:
                st.markdown(f'<div class="no-sheet">⚠️ {label} missing</div>', unsafe_allow_html=True)
    for col, (icon, label, url) in zip(cols[len(files):], links):
        with col:
            st.link_button(f"{icon} {label}", url, use_container_width=True)
    




with tab5:
    st.markdown("""
    ### How to use this dashboard
    - Select an intern and date in **Filters** to view their tasks
    - **Overview** shows total tasks, today's tasks, clubs collected, and active days
    - **Task Details** lists tasks for the selected date
    - **Quick Actions** opens the intern's sheet or attendance form
    - **Prompt Builder** generates a research prompt per institute
    """)

with tab6:
    st.markdown('<div class="sh">🧑‍💼 &nbsp;Sub Leader Summary</div>', unsafe_allow_html=True)
    sl_date = st.date_input("Select Date", value=today, key="sl_date")

    def get_intern_stats(csv_url):
        """Return (total_emails, total_contacts) - distinct, non-blank."""
        try:
            sdf = load_sheet_csv(csv_url)
        except Exception:
            return 0, 0

        def nunique(d, col):
            return d[col].dropna().astype(str).str.strip().replace('', pd.NA).dropna().nunique() if col in d.columns else 0

        return nunique(sdf, 'ClubEmail'), nunique(sdf, 'ClubContactNumber')

    id_cols = [c for c in ["SchoolID", "Institute Name", "State", "District", "City"] if c in df.columns]

    rows, detail_frames = [], []
    for name in sorted(df['Intern Name'].unique()):
        day_df = df[(df['Intern Name'] == name) & (df['Date'].dt.date == sl_date)].copy()
        tasks = len(day_df)
        total_clubs_n = day_clubs_n = total_e = total_c = 0
        url = intern_links.get(name.strip(), "")

        if is_valid_link(url):
            csv_url = sheet_csv_url(url)
            if csv_url:
                try:
                    _idf = load_sheet_csv(csv_url)
                    total_clubs_n = len(_idf)
                    _idf['SchoolID'] = _idf['SchoolID'].astype(str).str.strip()
                    clubs_count = _idf.groupby('SchoolID').size().reset_index(name='Clubs Collected')
                    day_df['SchoolID'] = day_df['SchoolID'].astype(str).str.strip()
                    day_df = day_df.merge(clubs_count, on='SchoolID', how='left')
                    day_df['Clubs Collected'] = day_df['Clubs Collected'].fillna(0).astype(int)
                    day_clubs_n = day_df['Clubs Collected'].sum()
                except Exception:
                    pass
                total_e, total_c = get_intern_stats(csv_url)

        rows.append({
            "Intern": name, "Tasks": tasks,
            "Clubs (Day)": day_clubs_n, "Clubs (Total)": total_clubs_n,
            "Emails (Total)": total_e,
            "Contacts (Total)": total_c,
        })

        if id_cols:
            dd = day_df[id_cols].dropna(how='all').drop_duplicates().copy()
            if not dd.empty:
                dd.insert(0, "Intern", format_intern_name(name))
                detail_frames.append(dd)            

    summary_df = pd.DataFrame(rows)
    summary_df["Intern"] = summary_df["Intern"].apply(format_intern_name)
    detail_df = pd.concat(detail_frames, ignore_index=True) if detail_frames else pd.DataFrame(columns=["Intern"] + id_cols)

    # ── MERGE: institute rows + that intern's summary stats, in one table ──
    if not detail_df.empty:
        merged_df = detail_df.merge(summary_df, on="Intern", how="left")
    else:
        merged_df = summary_df.copy()
        for c in id_cols:
            merged_df[c] = ""

    ordered_cols = ["Intern"] + id_cols + ["Tasks", "Clubs (Day)", "Clubs (Total)", "Emails (Total)", "Contacts (Total)"]
    ordered_cols = [c for c in ordered_cols if c in merged_df.columns]
    merged_df = merged_df[ordered_cols]

    totals = {c: summary_df[c].sum() for c in summary_df.columns if c != "Intern"}
    total_row = {c: "" for c in ordered_cols}
    total_row["Intern"] = "TOTAL"
    total_row.update(totals)
    merged_display = pd.concat([merged_df, pd.DataFrame([total_row])], ignore_index=True)

    st.markdown('<div class="sh">📋 &nbsp;Intern + Institute Summary</div>', unsafe_allow_html=True)
    st.dataframe(merged_display, use_container_width=True, hide_index=True)

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f'<div class="kpi blue"><div class="kpi-val">{totals["Tasks"]}</div><div class="kpi-lbl">Tasks ({sl_date})</div></div>', unsafe_allow_html=True)
    with k2:
        st.markdown(f'<div class="kpi green"><div class="kpi-val">{totals["Clubs (Day)"]}</div><div class="kpi-lbl">Clubs Today</div></div>', unsafe_allow_html=True)
    with k3:
        st.markdown(f'<div class="kpi purple"><div class="kpi-val">{totals["Emails (Total)"]}</div><div class="kpi-lbl">Total Emails</div></div>', unsafe_allow_html=True)
    with k4:
        st.markdown(f'<div class="kpi amber"><div class="kpi-val">{totals["Contacts (Total)"]}</div><div class="kpi-lbl">Total Contacts</div></div>', unsafe_allow_html=True)

    def sanitize(text):
        text = str(text)
        replacements = {
            "\u2026": "...", "\u2018": "'", "\u2019": "'",
            "\u201c": '"', "\u201d": '"', "\u2013": "-", "\u2014": "-",
        }
        for bad, good in replacements.items():
            text = text.replace(bad, good)
        return text.encode("latin-1", "ignore").decode("latin-1")

    def wrap_text(pdf_obj, text, width, pad=3):
        """Manually word-wrap text to fit `width` mm, using current font. Returns list of lines."""
        words = text.split(" ")
        lines = []
        current = ""
        for word in words:
            trial = (current + " " + word).strip()
            if pdf_obj.get_string_width(trial) <= width - pad:
                current = trial
            else:
                if current:
                    lines.append(current)
                # if a single word itself is too long, hard-break it
                while pdf_obj.get_string_width(word) > width - pad and len(word) > 1:
                    cut = len(word)
                    while cut > 1 and pdf_obj.get_string_width(word[:cut]) > width - pad:
                        cut -= 1
                    lines.append(word[:cut])
                    word = word[cut:]
                current = word
        if current:
            lines.append(current)
        return lines if lines else [""]

    def build_pdf(merged_, date_):
        pdf = FPDF(orientation="L", format="A4")
        pdf.set_auto_page_break(auto=True, margin=10)
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 10, "Intern Task & Institute Report", ln=1, align="C")
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 7, f"Date: {date_}", ln=1)
        pdf.ln(2)

        cols = list(merged_.columns)
        page_w = 277

        WIDE_COLS = {"Institute Name", "Intern"}
        MED_COLS = {"State", "District", "City"}

        pdf.set_font("Helvetica", "", 8)
        min_w, max_w = 14, 70
        raw_widths = []
        for c in cols:
            if c == "Institute Name":
                raw_widths.append(60)
                continue
            if c == "Intern":
                raw_widths.append(45)
                continue
            header_w = pdf.get_string_width(sanitize(c)) + 6
            sample_w = merged_[c].astype(str).head(200).map(
                lambda v: pdf.get_string_width(sanitize(v)[:30])
            ).max() + 6
            w = max(header_w, sample_w)
            w = max(min_w, min(w, max_w if c not in MED_COLS else 40))
            raw_widths.append(w)

        remaining = page_w - sum(w for c, w in zip(cols, raw_widths) if c in WIDE_COLS)
        other_total = sum(w for c, w in zip(cols, raw_widths) if c not in WIDE_COLS)
        scale = (remaining / other_total) if other_total else 1
        widths = [w if c in WIDE_COLS else w * scale for c, w in zip(cols, raw_widths)]

        row_h = 6

        def draw_header():
            pdf.set_font("Helvetica", "B", 8)
            pdf.set_fill_color(220, 232, 249)
            for c, w in zip(cols, widths):
                pdf.cell(w, 8, sanitize(c), border=1, fill=True, align="C")
            pdf.ln()

        draw_header()
        pdf.set_font("Helvetica", "", 7.5)

        for _, r in merged_.iterrows():
            is_total = str(r["Intern"]) == "TOTAL"
            font_style = "B" if is_total else ""
            pdf.set_font("Helvetica", font_style, 7.5)

            wrapped_cells = []
            max_lines = 1
            for c, w in zip(cols, widths):
                text = sanitize(r[c])
                if c in WIDE_COLS:
                    lines = wrap_text(pdf, text, w)
                    wrapped_cells.append((lines, w, True))
                    max_lines = max(max_lines, len(lines))
                else:
                    while pdf.get_string_width(text) > w - 3 and len(text) > 1:
                        text = text[:-1]
                    if text != sanitize(r[c]):
                        text = (text[:-3] + "...") if len(text) > 3 else text
                    wrapped_cells.append(([text], w, False))

            this_row_h = row_h * max_lines

            if pdf.get_y() + this_row_h > pdf.page_break_trigger:
                pdf.add_page()
                draw_header()
                pdf.set_font("Helvetica", font_style, 7.5)

            x_start = pdf.get_x()
            y_start = pdf.get_y()

            for lines, w, is_wide in wrapped_cells:
                x = pdf.get_x()
                y = pdf.get_y()
                if is_wide:
                    # draw outer border box for full row height
                    pdf.rect(x, y, w, this_row_h)
                    for i, line in enumerate(lines):
                        pdf.set_xy(x + 1, y + i * row_h)
                        pdf.cell(w - 2, row_h, line, border=0, align="L")
                    pdf.set_xy(x + w, y)
                else:
                    pdf.cell(w, this_row_h, lines[0], border=1, align="C")
            pdf.set_xy(x_start, y_start + this_row_h)

        out = pdf.output(dest="S")
        return out.encode("latin-1") if isinstance(out, str) else bytes(out)    

    pdf_bytes = build_pdf(merged_display, sl_date)
    st.download_button(
        "📥 Export PDF Report",
        data=pdf_bytes,
        file_name=f"SubLeader_Report_{sl_date}.pdf",
        mime="application/pdf",
        use_container_width=True,
        key="subleader_pdf_export",
    )   
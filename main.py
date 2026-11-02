# AI-Based University Timetable Generator
# Next-Level Multi-Perspective Scheduling System (Section, Faculty, Room, Analytics)

import streamlit as st
import pandas as pd

from data.sample_data import (
    DAYS,
    PERIODS,
    COURSES,
    ROOMS,
    FACULTY_PREFERENCES
)

from ai.csp import create_variables
from ai.optimizer import generate_optimized_timetable
from ai.constraints import validate_timetable

from ui.timetable_view import (
    display_timetable,
    display_faculty_timetable,
    create_schedule_dataframe
)
from ui.analysis_view import (
    display_analysis,
    display_algorithm_comparison
)


# ==========================================
# Page Configuration & Modern Theme Styling
# ==========================================

st.set_page_config(
    page_title="AI University Timetable Generator",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)
# ==========================================
# Theme Manager
# ==========================================

if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

with st.sidebar:

    theme = st.selectbox(
        "🎨 Theme",
        ["Dark", "Light"],
        index=0 if st.session_state.theme == "Dark" else 1
    )

    st.session_state.theme = theme

dark_mode = theme == "Dark"

if dark_mode:
    page_bg = "#0f172a"
    container_bg = "rgba(30,41,59,0.95)"
    card_bg = "rgba(30,41,59,0.7)"
    text_color = "#ffffff"
    subtitle_color = "#94a3b8"
    border_color = "rgba(59,130,246,0.25)"
    metric_shadow = "rgba(0,0,0,0.25)"
    input_bg = "#1e293b"
    input_border = "rgba(59,130,246,0.35)"
    dropdown_bg = "#1e293b"
    dropdown_hover = "#2563eb"
else:
    page_bg = "#f5f7fb"
    container_bg = "#ffffff"
    card_bg = "#ffffff"
    text_color = "#0f172a"
    subtitle_color = "#475569"
    border_color = "#cbd5e1"
    metric_shadow = "rgba(0,0,0,0.08)"
    input_bg = "#ffffff"
    input_border = "#cbd5e1"
    dropdown_bg = "#ffffff"
    dropdown_hover = "#3b82f6"


# Custom Next-Level UI CSS Injection
st.markdown(f"""
<style>

@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

:root {{
    --text-color: {text_color};
    --primary-color: #3b82f6;
    --background-color: {page_bg};
    --secondary-background-color: {input_bg};
}}

html,
body,
[class*="css"] {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: {text_color};
}}

.stApp {{
    --text-color: {text_color};
    --primary-color: #3b82f6;
    --background-color: {page_bg};
    --secondary-background-color: {input_bg};
    background-color: {page_bg};
    color: {text_color};
    transition: all .3s ease;
}}

[data-testid="stSidebar"] {{
    background: {container_bg};
}}

.hero-header {{
    background: {container_bg};
    border: 1px solid {border_color};
    border-radius: 18px;
    padding: 25px;
    margin-bottom: 20px;
    box-shadow: 0px 10px 30px rgba(0,0,0,0.15);
}}

.hero-title {{
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(135deg,#2563eb,#0891b2,#9333ea);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}

.hero-subtitle {{
    color: {subtitle_color};
}}

.hero-badges {{
    display:flex;
    gap:8px;
    flex-wrap:wrap;
    margin-top:12px;
}}

.hero-pill {{
    background: rgba(59,130,246,.15);
    color:#3b82f6;
    border-radius:999px;
    padding:5px 11px;
    font-size:.75rem;
    font-weight:600;
}}

div[data-testid="stMetric"] {{
    background:{card_bg};
    border-radius:15px;
    padding:15px;
    border:1px solid {border_color};
    box-shadow:0 5px 15px {metric_shadow};
    transition:all .2s ease;
}}

div[data-testid="stMetric"]:hover {{
    transform:translateY(-3px);
}}

button[data-baseweb="tab"] {{
    font-weight:600 !important;
    padding:10px 18px !important;
}}

.stButton button {{
    border-radius:12px !important;
}}

.stDataFrame {{
    border-radius:12px;
}}

/* Universal Text Color */
h1, h2, h3, h4, h5, h6,
p, span, div, label,
.stMarkdown,
.stText,
.stCaption {{
    color: {text_color} !important;
}}

/* Sidebar Text */
[data-testid="stSidebar"] * {{
    color: {text_color} !important;
}}

/* Metrics */
div[data-testid="stMetric"] label,
div[data-testid="stMetric"] div {{
    color: {text_color} !important;
}}

/* Tabs */
button[data-baseweb="tab"] {{
    color: {text_color} !important;
}}

/* Tables & DataFrames */
table,
thead,
tbody,
tr,
th,
td {{
    color: {text_color} !important;
}}

/* Select Boxes */
div[data-baseweb="select"] * {{
    color: {text_color} !important;
}}

/* Sliders */
.stSlider label {{
    color: {text_color} !important;
}}

/* Expanders */
.streamlit-expanderHeader {{
    color: {text_color} !important;
}}

/* Radio Buttons */
.stRadio label {{
    color: {text_color} !important;
}}

/* Checkboxes */
.stCheckbox label {{
    color: {text_color} !important;
}}

/* Radio Buttons */

[data-testid="stRadio"] * {{
    color: {text_color} !important;
}}

/* All Select Boxes */

.stSelectbox * {{
    color: {text_color} !important;
}}

/* Success/Info/Warning Text */
[data-testid="stNotification"] * {{
    color: {text_color} !important;
}}

html, body, .stApp {{
    color: var(--text-color) !important;
}}

/* =========================
   TIMETABLE TABLES
   ========================= */

table {{
    color: {text_color} !important;
}}

thead tr th {{
    color: {text_color} !important;
    background-color: {card_bg} !important;
}}

tbody tr td {{
    color: {text_color} !important;
    background-color: {card_bg} !important;
}}

/* Streamlit Dataframe */

[data-testid="stDataFrame"] * {{
    color: {text_color} !important;
}}

/* AG Grid Tables */

.ag-root-wrapper,
.ag-root-wrapper-body,
.ag-header,
.ag-row,
.ag-cell,
.ag-header-cell {{
    color: {text_color} !important;
    background-color: {card_bg} !important;
}}

/* =========================
   TAB CONTENT
   ========================= */

.stTabs * {{
    color: {text_color} !important;
}}

/* =========================
   DOWNLOAD BUTTONS
   ========================= */

[data-testid="stDownloadButton"] button {{

    background-color: #3b82f6 !important;
    color: white !important;

    border: none !important;
    border-radius: 12px !important;

    font-weight: 600 !important;

    transition: all 0.2s ease;
}}

[data-testid="stDownloadButton"] button:hover {{

    background-color: #2563eb !important;

    transform: translateY(-2px);

    box-shadow: 0px 5px 15px rgba(59,130,246,0.4);
}}

/* =========================
   TIMETABLE SELECTORS
   ========================= */

.stSelectbox * {{
    color: {text_color} !important;
}}

.stMultiSelect * {{
    color: {text_color} !important;
}}

/* =========================
   MARKDOWN INSIDE TABS
   ========================= */

.stMarkdown,
.stMarkdown p,
.stMarkdown li,
.stMarkdown span {{
    color: {text_color} !important;
}}

/* Timetable Header Row */

thead th {{
    background-color: {container_bg} !important;
    color: {text_color} !important;
    border: 1px solid {border_color} !important;
    font-weight: 700 !important;
}}

/* Dataframe Headers */

.col_heading {{
    background-color: {container_bg} !important;
    color: {text_color} !important;
}}

/* Reset Button */

.stButton button {{
    background-color: {card_bg} !important;
    color: {text_color} !important;
    border: 1px solid {border_color} !important;
}}

.stButton button:hover {{
    background-color: #3b82f6 !important;
    color: white !important;
}}

/* =========================
   FORM CONTROLS (SELECTBOX, MULTISELECT, INPUTS)
   ========================= */

/* Labels */
[data-testid="stSelectbox"] label,
[data-testid="stSelectbox"] label p,
[data-testid="stSelectbox"] [data-testid="stWidgetLabel"] p,
[data-testid="stMultiSelect"] label,
[data-testid="stMultiSelect"] label p,
[data-testid="stTextInput"] label,
[data-testid="stTextInput"] label p {{
    color: {text_color} !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
}}

/* The Selectbox / Input Box Container */
[data-testid="stSelectbox"] [class*="e1oobldh0"],
[data-testid="stSelectbox"] > div > div > div,
[data-testid="stMultiSelect"] [class*="ew56mvo0"],
[data-testid="stMultiSelect"] > div > div > div,
[data-testid="stTextInput"] > div > div,
div[data-baseweb="select"],
div[data-baseweb="select"] > div {{
    background-color: {input_bg} !important;
    background: {input_bg} !important;
    color: {text_color} !important;
    border: 1.5px solid {input_border} !important;
    border-radius: 10px !important;
    box-shadow: 0 1px 3px {metric_shadow} !important;
}}

[data-testid="stSelectbox"] div:has(> input) {{
    background-color: {input_bg} !important;
    background: {input_bg} !important;
    color: {text_color} !important;
    border: 1.5px solid {input_border} !important;
    border-radius: 10px !important;
}}

/* Value / Text Input Display */
[data-testid="stSelectbox"] input,
[data-testid="stSelectbox"] [class*="e1oobldh1"],
[data-testid="stMultiSelect"] input,
[data-testid="stMultiSelect"] [class*="ew56mvo6"],
[data-testid="stTextInput"] input,
div[data-baseweb="select"] input {{
    background-color: transparent !important;
    background: transparent !important;
    color: {text_color} !important;
    -webkit-text-fill-color: {text_color} !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
}}

/* Placeholder */
[data-testid="stSelectbox"] input::placeholder,
[data-testid="stMultiSelect"] input::placeholder,
[data-testid="stTextInput"] input::placeholder {{
    color: {subtitle_color} !important;
    -webkit-text-fill-color: {subtitle_color} !important;
}}

/* Selectbox Dropdown Arrow & Buttons */
[data-testid="stSelectbox"] button,
[data-testid="stSelectbox"] svg,
[data-testid="stSelectbox"] [class*="e1oobldh2"],
[data-testid="stSelectbox"] [class*="e1oobldh3"],
[data-testid="stMultiSelect"] button,
[data-testid="stMultiSelect"] svg,
div[data-baseweb="select"] svg {{
    color: {text_color} !important;
    fill: {text_color} !important;
}}

/* =========================
   DROPDOWN MENU / POPOVER
   ========================= */

[data-testid="stSelectboxVirtualDropdown"],
[data-testid="stSelectboxVirtualDropdown"] [class*="e1oobldh4"],
[data-testid="stSelectboxVirtualDropdown"] [class*="e1oobldh5"],
[data-testid="stMultiSelectDropdown"],
div[data-baseweb="popover"],
div[data-baseweb="popover"] > div,
ul[role="listbox"],
div[role="listbox"] {{
    background-color: {dropdown_bg} !important;
    background: {dropdown_bg} !important;
    color: {text_color} !important;
    border: 1.5px solid {input_border} !important;
    border-radius: 12px !important;
    box-shadow: 0 10px 30px rgba(0,0,0,0.18) !important;
}}

/* Dropdown Menu Items */
[data-testid="stSelectboxVirtualDropdown"] li,
[data-testid="stSelectboxVirtualDropdown"] [class*="e1oobldh7"],
[data-testid="stSelectboxVirtualDropdown"] [class*="e1oobldh8"],
[data-testid="stSelectboxVirtualDropdown"] div,
[data-testid="stSelectboxVirtualDropdown"] span,
[data-testid="stMultiSelectDropdown"] li,
[data-testid="stMultiSelectDropdown"] div,
[data-testid="stMultiSelectDropdown"] span,
ul[role="listbox"] li,
div[role="option"] {{
    background-color: {dropdown_bg} !important;
    color: {text_color} !important;
    -webkit-text-fill-color: {text_color} !important;
    font-size: 0.92rem !important;
}}

/* Dropdown Option Hover & Active State */
[data-testid="stSelectboxVirtualDropdown"] li:hover,
[data-testid="stSelectboxVirtualDropdown"] li:hover *,
[data-testid="stSelectboxVirtualDropdown"] [class*="e1oobldh7"]:hover,
[data-testid="stSelectboxVirtualDropdown"] [class*="e1oobldh7"]:hover *,
[data-testid="stSelectboxVirtualDropdown"] [data-hovered],
[data-testid="stSelectboxVirtualDropdown"] [data-focused],
ul[role="listbox"] li:hover,
ul[role="listbox"] li:hover *,
div[role="option"]:hover,
div[role="option"]:hover * {{
    background-color: {dropdown_hover} !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}}

/* Sidebar Specific Overrides */
[data-testid="stSidebar"] {{
    background-color: {container_bg} !important;
}}

[data-testid="stSidebar"] * {{
    color: {text_color} !important;
}}

/* Sidebar Selectbox & Inputs */
[data-testid="stSidebar"] [data-testid="stSelectbox"] [class*="e1oobldh0"],
[data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div > div {{
    background-color: {input_bg} !important;
    background: {input_bg} !important;
    border: 1.5px solid {input_border} !important;
}}

/* Dataframe Headers */
[data-testid="stDataFrame"] th {{
    background-color: {container_bg} !important;
    color: {text_color} !important;
}}

/* Dataframe Cells */
[data-testid="stDataFrame"] td {{
    background-color: {card_bg} !important;
    color: {text_color} !important;
}}

/* Dataframe Index Column */
[data-testid="stDataFrame"] tbody th {{
    background-color: {container_bg} !important;
    color: {text_color} !important;
}}
</style>
""", unsafe_allow_html=True)

# ==========================================
# Hero Banner
# ==========================================

st.markdown("""
<div class="hero-header">
    <div class="hero-title">🎓 AI-Powered University Timetable Engine</div>
    <div class="hero-subtitle">
        Intelligent constraint satisfaction & heuristic multi-perspective scheduler.
        Generates clash-free, fatigue-aware weekly schedules for student cohorts and faculty members.
    </div>
    <div class="hero-badges">
        <span class="hero-pill">⚡ CSP Backtracking</span>
        <span class="hero-pill">🎯 MRV & Degree Heuristic</span>
        <span class="hero-pill">🔍 Forward Checking</span>
        <span class="hero-pill">⭐ Least Constraining Value (LCV)</span>
        <span class="hero-pill">👨‍🏫 Faculty Timetable Hub</span>
        <span class="hero-pill">🛡️ Hard & Soft Optimization</span>
    </div>
</div>
""", unsafe_allow_html=True)

if dark_mode:
    st.success("🌙 Dark Theme Enabled")
else:
    st.info("☀️ Light Theme Enabled")

# ==========================================
# Dashboard Campus Metrics
# ==========================================

total_sessions = sum(
    course["sessions_per_week"]
    for course in COURSES.values()
)

total_teachers = len({
    course["teacher"]
    for course in COURSES.values()
})

total_sections = len({
    course["section"]
    for course in COURSES.values()
})

total_rooms = len(ROOMS)
total_labs = sum(1 for r in ROOMS.values() if r.get("type") == "Lab")
total_classrooms = total_rooms - total_labs

m_col1, m_col2, m_col3, m_col4, m_col5 = st.columns(5)
m_col1.metric("Enrolled Courses", len(COURSES), delta="10 Total")
m_col2.metric("Faculty Members", total_teachers, delta="9 Professors")
m_col3.metric("Student Sections", total_sections, delta="CSE-A & CSE-B")
m_col4.metric("Required Sessions", f"{total_sessions} hrs/wk", delta="100% Demand")
m_col5.metric("Campus Infrastructure", f"{total_rooms} Rooms", delta=f"{total_labs} Labs / {total_classrooms} Lecture Halls")

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)


# ==========================================
# Sidebar: Advanced Optimization & Constraint Tuning
# ==========================================

with st.sidebar:
    st.header("⚙️ Scheduler Controls")
    st.caption("Configure optimization depth and operational constraint limits.")

    st.subheader("🎯 Optimization Settings")
    attempts = st.slider(
        "Search Iterations (Restarts)",
        min_value=1,
        max_value=20,
        value=5,
        help="Higher restarts explore diverse search branches to maximize quality score."
    )

    st.subheader("🛡️ Precision Constraint Controls")
    max_daily_teacher = st.slider(
        "Max Daily Sessions per Teacher",
        min_value=2,
        max_value=4,
        value=3,
        help="Prevents faculty overload by capping sessions per professor on any day."
    )

    max_consecutive_teacher = st.slider(
        "Max Consecutive Teaching Hours",
        min_value=1,
        max_value=3,
        value=2,
        help="Enforces rest periods by capping consecutive teaching hours without a break."
    )

    max_consecutive_section = st.slider(
        "Max Consecutive Student Classes",
        min_value=2,
        max_value=4,
        value=3,
        help="Prevents student cognitive fatigue by avoiding long blocks of continuous classes."
    )

    st.divider()

    with st.expander("🏛️ View Campus Data & Constraints", expanded=False):
        st.markdown("**Enrolled Courses:**")
        course_summary = [
            {"Course": c, "Teacher": d["teacher"], "Sec": d["section"], "Type": d["room_type"], "Hrs": d["sessions_per_week"]}
            for c, d in COURSES.items()
        ]
        st.dataframe(pd.DataFrame(course_summary), hide_index=True, use_container_width=True)

        st.markdown("**Rooms & Capacity:**")
        room_summary = [{"Room": r, "Cap": d["capacity"], "Type": d["type"]} for r, d in ROOMS.items()]
        st.dataframe(pd.DataFrame(room_summary), hide_index=True, use_container_width=True)

        st.markdown("**Faculty Preferred Slots:**")
        prefs_summary = [{"Teacher": t, "Preferred Slot": f"{p[0][0]} {p[0][1]}"} for t, p in FACULTY_PREFERENCES.items()]
        st.dataframe(pd.DataFrame(prefs_summary), hide_index=True, use_container_width=True)


# ==========================================
# Initialize Session State
# ==========================================

if "timetable_result" not in st.session_state:
    st.session_state["timetable_result"] = None


# ==========================================
# Timetable Generation Execution
# ==========================================

btn_col1, btn_col2 = st.columns([3, 1])
with btn_col1:
    generate_clicked = st.button(
        "🚀 Generate AI-Optimized Timetable",
        type="primary",
        use_container_width=True
    )
with btn_col2:
    if st.session_state["timetable_result"] is not None:
        if st.button("🔄 Reset Timetable", use_container_width=True):
            st.session_state["timetable_result"] = None
            st.rerun()

if generate_clicked:
    with st.spinner("AI Engine is executing CSP Backtracking with MRV, Forward Checking & LCV..."):
        try:
            result = generate_optimized_timetable(
                courses=COURSES,
                rooms=ROOMS,
                days=DAYS,
                periods=PERIODS,
                faculty_preferences=FACULTY_PREFERENCES,
                attempts=attempts,
                max_daily_teacher_sessions=max_daily_teacher,
                max_consecutive_teacher_sessions=max_consecutive_teacher,
                max_consecutive_section_sessions=max_consecutive_section
            )

            # Independently audit the generated timetable
            if result.get("success", False):
                variables = create_variables(COURSES)
                violations = validate_timetable(
                    result["timetable"],
                    variables,
                    ROOMS,
                    COURSES,
                    max_daily_teacher_sessions=max_daily_teacher,
                    max_consecutive_teacher_sessions=max_consecutive_teacher,
                    max_consecutive_section_sessions=max_consecutive_section,
                    periods_list=PERIODS
                )

                result["violations"] = violations

                if violations:
                    result["success"] = False
                    result["message"] = "The timetable failed hard-constraint validation."
                else:
                    result["message"] = "Timetable successfully generated and 100% verified against all hard constraints!"

            st.session_state["timetable_result"] = result

        except Exception as error:
            st.session_state["timetable_result"] = {
                "success": False,
                "message": f"An error occurred during scheduling: {error}",
                "timetable": {},
                "violations": []
            }


# ==========================================
# Results Presentation
# ==========================================

result = st.session_state["timetable_result"]

if result is None:
    st.info(
        "👋 Click **'Generate AI-Optimized Timetable'** above to compute an optimal schedule. "
        "The AI solver will satisfy 100% of hard constraints, honor faculty time preferences, and balance student workload."
    )
elif result.get("success", False):
    violations = result.get("violations", [])

    if violations:
        st.error(f"⚠️ {len(violations)} hard-constraint violations detected:")
        for v in violations:
            st.write(f"- {v}")
    else:
        st.success(f"🎉 **Success**: {result['message']} (Quality Score: **{result.get('score', 0)}/100**)")

    variables = create_variables(COURSES)
    schedule_df = create_schedule_dataframe(result["timetable"], variables)

    # Main Application Multi-Perspective Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📅 Weekly Timetables Hub",
        "👨‍🏫 Dedicated Faculty Hub",
        "📊 AI Quality & Constraint Audit",
        "⚡ Algorithm Benchmark",
        "📋 Constraint Engine Model"
    ])

    # --------------------------------------
    # Tab 1: Weekly Timetables (Section, Faculty, Room, Master)
    # --------------------------------------
    with tab1:
        display_timetable(
            result["timetable"],
            variables,
            DAYS,
            PERIODS,
            faculty_preferences=FACULTY_PREFERENCES
        )

    # --------------------------------------
    # Tab 2: Dedicated Faculty Hub
    # --------------------------------------
    with tab2:
        display_faculty_timetable(
            schedule_df,
            DAYS,
            PERIODS,
            faculty_preferences=FACULTY_PREFERENCES,
            key_prefix="dedicated_faculty"
        )

    # --------------------------------------
    # Tab 3: AI Quality & Constraint Audit
    # --------------------------------------
    with tab3:
        display_analysis(
            result,
            rooms=ROOMS,
            courses=COURSES,
            days=DAYS,
            periods=PERIODS
        )

    # --------------------------------------
    # Tab 4: Algorithm Benchmark
    # --------------------------------------
    with tab4:
        display_algorithm_comparison(
            COURSES,
            ROOMS,
            DAYS,
            PERIODS,
            FACULTY_PREFERENCES
        )

    # --------------------------------------
    # Tab 5: Constraint Engine Model Inspector
    # --------------------------------------
    with tab5:
        st.subheader("📋 Mathematical Constraint Engine Specifications")
        st.caption("Formal formulation of the University Course Timetabling Problem (UCTP).")

        st.markdown(r"""
        #### 1. Problem Formulation as Constraint Satisfaction Problem (CSP)
        The scheduling problem is represented as a triple $\langle X, D, C \rangle$:
        - **Variables ($X$)**: Every course session $s \in S$, total $= 18$ variables:
          $$X = \{ c_{i, j} \mid c_i \in \text{COURSES}, 1 \le j \le \text{sessions}(c_i) \}$$
        - **Domains ($D$)**: Possible triple assignments $\langle r, d, p \rangle \in \text{ROOMS} \times \text{DAYS} \times \text{PERIODS}$ matching capacity and room type:
          $$D(c_{i, j}) = \{ (r, d, p) \mid \text{cap}(r) \ge \text{students}(c_i) \land \text{type}(r) = \text{type}(c_i) \}$$
        - **Constraints ($C$)**: Hard operational constraints that must hold with 0 violations.

        ---

        #### 2. Hard Constraints Enforced (Must be 100% Satisfied)
        1. **Room Capacity**: For every assignment $(r, d, p)$ to variable $v$, $\text{capacity}(r) \ge \text{students}(v)$.
        2. **Room Type Match**: $\text{room\_type}(r) = \text{room\_type}(v)$ (Lab sessions require Lab rooms).
        3. **Teacher Clash Prevention**: No teacher can teach two sessions at the same $(d, p)$.
        4. **Section Clash Prevention**: No student cohort can have two classes at the same $(d, p)$.
        5. **Room Clash Prevention**: No physical room can host two sessions at the same $(d, p)$.
        6. **Daily Course Spacing**: Multiple sessions of the same course must occur on distinct days ($\le 1$ session/day).
        7. **Faculty Maximum Daily Load**: No professor can teach $> 3$ sessions on any single day.
        8. **Faculty Maximum Consecutive Sessions**: No professor can teach $> 2$ consecutive hours without rest.
        9. **Section Maximum Consecutive Sessions**: No student section can have $> 3$ consecutive class hours without rest.

        ---

        #### 3. Soft Constraints & Optimization Objective
        The soft optimization objective minimizes total penalty $P$:
        $$P = 3 \cdot \text{Gaps}_{\text{section}} + 5 \cdot \text{Consecutive}_{\text{difficult}} + 2 \cdot \text{PrefViolations} + 3 \cdot \text{Gaps}_{\text{faculty}} + 2 \cdot \text{Imbalance} + 8 \cdot \text{UnmetProfessors}$$
        $$\text{Quality Score} = \max(0, 100 - P)$$
        """)

else:
    st.error(result.get("message", "Unable to generate a valid timetable."))
    violations = result.get("violations", [])

    if violations:
        st.subheader("Validation Errors Detected:")
        for v in violations:
            st.write(f"- {v}")


# ==========================================
# Application Footer
# ==========================================

st.divider()
st.caption(
    "🎓 Advanced Academic AI Timetable Generation System | "
    "CSP Backtracking • MRV • Degree Heuristic • Forward Checking • LCV • Multi-Perspective Visualization"
)

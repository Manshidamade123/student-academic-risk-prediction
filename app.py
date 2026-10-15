import streamlit as st
from supabase import create_client
from datetime import date

st.set_page_config(
    page_title="PlaceTrack | Placement Companion",
    page_icon="🎓",
    layout="wide"
)

# ---------------- DESIGN ----------------

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #fffaf3 0%, #f4f8f4 100%);
}
h1, h2, h3 {
    color: #142d4e;
}
[data-testid="stMetric"] {
    background: white;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #e5e7eb;
}
div.stButton > button[kind="primary"] {
    background-color: #138808;
    color: white;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SUPABASE CONNECTION ----------------

try:
    SUPABASE_URL = st.secrets["supabase"]["url"]
    SUPABASE_KEY = st.secrets["supabase"]["key"]
except Exception:
    st.error(
        "Supabase credentials are missing. "
        "Add the project URL and publishable key in Streamlit Secrets."
    )
    st.stop()

if "supabase_client" not in st.session_state:
    try:
        st.session_state["supabase_client"] = create_client(
            SUPABASE_URL, SUPABASE_KEY
        )
    except Exception:
        st.error("Could not connect to Supabase. Check your configuration.")
        st.stop()

db = st.session_state["supabase_client"]

st.title("🎓 PlaceTrack")
st.markdown(
    "### Track your progress. Build your skills. Prepare for placements."
)
st.caption(
    "Your personal B.Tech academic tracker, technical skill manager "
    "and placement preparation companion."
)

# ---------------- LOGIN / SIGN UP ----------------

if "user_id" not in st.session_state:

    st.info("Sign in to access your saved academic and preparation data.")

    login_tab, signup_tab = st.tabs(["Login", "Create account"])

    with login_tab:
        with st.form("login_form"):
            login_email = st.text_input("Email address")
            login_password = st.text_input(
                "Password", type="password"
            )
            login_clicked = st.form_submit_button(
                "Login", type="primary"
            )

        if login_clicked:
            try:
                response = db.auth.sign_in_with_password({
                    "email": login_email.strip(),
                    "password": login_password
                })

                if response.user:
                    st.session_state["user_id"] = str(response.user.id)
                    st.session_state["user_email"] = response.user.email
                    st.rerun()
                else:
                    st.error("Login unsuccessful. Check your details.")

            except Exception:
                st.error(
                    "Login failed. Check your email and password. "
                    "If needed, verify your email first."
                )

    with signup_tab:
        with st.form("signup_form"):
            signup_email = st.text_input(
                "Email address", key="signup_email"
            )
            signup_password = st.text_input(
                "Create a password",
                type="password",
                key="signup_password"
            )
            signup_confirm = st.text_input(
                "Confirm password",
                type="password"
            )
            signup_clicked = st.form_submit_button(
                "Create account", type="primary"
            )

        if signup_clicked:
            if signup_password != signup_confirm:
                st.error("Your passwords do not match.")
            elif len(signup_password) < 8:
                st.error("Use a password with at least 8 characters.")
            else:
                try:
                    response = db.auth.sign_up({
                        "email": signup_email.strip(),
                        "password": signup_password
                    })

                    if response.user and response.session:
                        st.session_state["user_id"] = str(
                            response.user.id
                        )
                        st.session_state["user_email"] = (
                            response.user.email
                        )
                        st.success("Account created successfully!")
                        st.rerun()
                    elif response.user:
                        st.success(
                            "Account created. Check your email for "
                            "a verification link, then return here to log in."
                        )
                    else:
                        st.error("Account creation was unsuccessful.")

                except Exception:
                    st.error(
                        "Could not create the account. The email may "
                        "already be registered, or the password may "
                        "not meet the account requirements."
                    )

    st.stop()

# ---------------- AUTHENTICATED USER ----------------

user_id = st.session_state["user_id"]
user_email = st.session_state.get("user_email", "")

st.sidebar.success("Logged in")
st.sidebar.write(user_email)

if st.sidebar.button("Log out"):
    try:
        db.auth.sign_out()
    except Exception:
        pass

    for key in ["user_id", "user_email", "supabase_client"]:
        st.session_state.pop(key, None)

    st.rerun()


def fetch_rows(table, order_by=None):
    query = (
        db.table(table)
        .select("*")
        .eq("user_id", user_id)
    )

    if order_by:
        query = query.order(order_by)

    return query.execute().data or []


def save_message(success_text):
    st.success(success_text)


# ---------------- LOAD PROFILE ----------------

try:
    profile_records = fetch_rows("profiles")
    profile = profile_records[0] if profile_records else {}
except Exception:
    st.error(
        "Could not load your profile. Check the database connection "
        "and Row Level Security policies."
    )
    st.stop()

# ---------------- PROFILE ----------------

with st.expander(
    "👤 My Student Profile",
    expanded=not bool(profile)
):
    branch_options = [
        "CSE",
        "CSE (AI/ML)",
        "IT",
        "ECE",
        "Electrical",
        "Mechanical",
        "Civil",
        "Other"
    ]

    role_options = [
        "Software Developer",
        "Python Developer",
        "AI/ML Engineer",
        "Data Analyst",
        "QA/Test Engineer",
        "Other"
    ]

    old_branch = profile.get("branch", "CSE")
    old_role = profile.get("target_role", "Software Developer")

    with st.form("profile_form"):
        full_name = st.text_input(
            "Full name",
            value=profile.get("full_name") or ""
        )

        branch = st.selectbox(
            "B.Tech branch",
            branch_options,
            index=(
                branch_options.index(old_branch)
                if old_branch in branch_options else 0
            )
        )

        graduation_year = st.number_input(
            "Expected graduation year",
            min_value=2022,
            max_value=2035,
            value=int(profile.get("graduation_year") or 2027)
        )

        target_role = st.selectbox(
            "Target job role",
            role_options,
            index=(
                role_options.index(old_role)
                if old_role in role_options else 0
            )
        )

        current_cgpa = st.number_input(
            "Current official CGPA (0–10)",
            min_value=0.0,
            max_value=10.0,
            value=float(profile.get("current_cgpa") or 0.0),
            step=0.01,
            format="%.2f"
        )

        active_backlogs = st.number_input(
            "Current active backlogs",
            min_value=0,
            max_value=50,
            value=int(profile.get("active_backlogs") or 0)
        )

        attendance = st.number_input(
            "Attendance percentage",
            min_value=0.0,
            max_value=100.0,
            value=float(profile.get("attendance_percentage") or 0.0),
            step=1.0
        )

        save_profile = st.form_submit_button(
            "Save student profile",
            type="primary"
        )

    if save_profile:
        if not full_name.strip():
            st.error("Please enter your name.")
        else:
            try:
                db.table("profiles").upsert({
                    "user_id": user_id,
                    "full_name": full_name.strip(),
                    "branch": branch,
                    "graduation_year": int(graduation_year),
                    "target_role": target_role,
                    "current_cgpa": float(current_cgpa),
                    "active_backlogs": int(active_backlogs),
                    "attendance_percentage": float(attendance)
                }).execute()

                save_message("Your profile has been saved.")
                st.rerun()

            except Exception:
                st.error(
                    "Could not save your profile. Please check "
                    "the database tables and permissions."
                )

# ---------------- DASHBOARD ----------------

try:
    profile_records = fetch_rows("profiles")
    profile = profile_records[0] if profile_records else {}

    semester_rows = fetch_rows("semester_results")
    skill_rows = fetch_rows("skill_progress")
    daily_rows = fetch_rows("daily_logs")
    portfolio_rows = fetch_rows("portfolio_items")
    checklist_rows = fetch_rows("prep_checklist")

except Exception:
    st.error("Could not load your saved information from Supabase.")
    st.stop()

st.subheader("📊 Your Dashboard")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Current CGPA",
    f"{float(profile.get('current_cgpa') or 0):.2f}/10"
)

col2.metric(
    "Active backlogs",
    int(profile.get("active_backlogs") or 0)
)

col3.metric(
    "Completed topics",
    sum(
        1 for row in skill_rows
        if row.get("status") == "Completed"
    )
)

col4.metric(
    "Portfolio items",
    len(portfolio_rows)
)

st.caption(
    "CGPA is entered by you. PlaceTrack does not currently "
    "calculate or predict your actual probability of placement."
)

# ---------------- MAIN SECTIONS ----------------

academic_tab, skills_tab, daily_tab, projects_tab, checklist_tab, plan_tab = (
    st.tabs([
        "🎓 Academics",
        "💻 Technical Skills",
        "⏰ Daily Study Log",
        "🏆 Projects & Activities",
        "✅ Placement Checklist",
        "🗓️ Study Planner"
    ])
)

# ---------------- ACADEMICS ----------------

with academic_tab:
    st.subheader("Semester-wise SGPA")

    st.write(
        "Enter SGPA only for semesters you have completed. "
        "Your official CGPA can be entered in your profile."
    )

    with st.form("semester_form"):
        semester_number = st.selectbox(
            "Select semester",
            list(range(1, 9))
        )

        sgpa = st.number_input(
            "SGPA (0–10)",
            min_value=0.0,
            max_value=10.0,
            value=7.0,
            step=0.01
        )

        save_semester = st.form_submit_button(
            "Save semester result",
            type="primary"
        )

    if save_semester:
        try:
            db.table("semester_results").upsert(
                {
                    "user_id": user_id,
                    "semester_number": int(semester_number),
                    "sgpa": float(sgpa)
                },
                on_conflict="user_id,semester_number"
            ).execute()

            save_message("Semester result saved.")
            st.rerun()

        except Exception:
            st.error("Could not save the semester result.")

    if semester_rows:
        semester_rows = sorted(
            semester_rows,
            key=lambda row: row["semester_number"]
        )

        st.dataframe(
            [
                {
                    "Semester": row["semester_number"],
                    "SGPA": row["sgpa"]
                }
                for row in semester_rows
            ],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Your semester results will appear here after saving.")

# ---------------- TECHNICAL SKILLS ----------------

with skills_tab:
    st.subheader("Build your technical skill profile")

    skill_categories = {
        "Core Computer Science": [
            "DSA",
            "OOP",
            "DBMS",
            "Operating Systems",
            "Computer Networks",
            "SQL"
        ],
        "Python Development": [
            "Python fundamentals",
            "Python OOP",
            "Git and GitHub",
            "REST APIs",
            "Testing"
        ],
        "AI/ML": [
            "NumPy",
            "Pandas",
            "Statistics",
            "Scikit-learn",
            "Model evaluation",
            "Model deployment"
        ],
        "Data Analytics": [
            "SQL",
            "Pandas",
            "Statistics",
            "Data visualization"
        ],
        "Interview Preparation": [
            "Quantitative aptitude",
            "Logical reasoning",
            "Coding interviews",
            "Technical interview",
            "HR interview"
        ]
    }

    with st.form("skill_form"):
        category = st.selectbox(
            "Skill category",
            list(skill_categories.keys())
        )

        topic = st.selectbox(
            "Topic",
            skill_categories[category]
        )

        status = st.selectbox(
            "Learning status",
            ["Not started", "Learning", "Completed"]
        )

        save_skill = st.form_submit_button(
            "Save skill progress",
            type="primary"
        )

    if save_skill:
        try:
            db.table("skill_progress").upsert(
                {
                    "user_id": user_id,
                    "category": category,
                    "topic": topic,
                    "status": status
                },
                on_conflict="user_id,category,topic"
            ).execute()

            save_message("Skill progress saved.")
            st.rerun()

        except Exception:
            st.error("Could not save your skill progress.")

    if skill_rows:
        st.subheader("Your learning progress")
        st.dataframe(
            [
                {
                    "Category": row["category"],
                    "Topic": row["topic"],
                    "Status": row["status"]
                }
                for row in skill_rows
            ],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Start adding topics to track your progress.")

# ---------------- DAILY STUDY LOG ----------------

with daily_tab:
    st.subheader("Track what you accomplished today")

    today = date.today()
    today_record = next(
        (
            row for row in daily_rows
            if str(row["log_date"]) == str(today)
        ),
        {}
    )

    with st.form("daily_form"):
        st.write(f"Study date: **{today.strftime('%d %B %Y')}**")

        study_minutes = st.number_input(
            "Focused study time (minutes)",
            min_value=0,
            max_value=1440,
            value=int(today_record.get("study_minutes") or 0)
        )

        dsa_questions = st.number_input(
            "Coding / DSA questions solved",
            min_value=0,
            max_value=500,
            value=int(today_record.get("dsa_questions") or 0)
        )

        aptitude_minutes = st.number_input(
            "Aptitude practice (minutes)",
            min_value=0,
            max_value=1440,
            value=int(today_record.get("aptitude_minutes") or 0)
        )

        topics_learned = st.text_area(
            "Topics learned or revised",
            value=today_record.get("topics_learned") or ""
        )

        project_work = st.text_area(
            "Project work completed",
            value=today_record.get("project_work") or ""
        )

        notes = st.text_area(
            "Notes for tomorrow",
            value=today_record.get("notes") or ""
        )

        save_daily = st.form_submit_button(
            "Save today's progress",
            type="primary"
        )

    if save_daily:
        try:
            db.table("daily_logs").upsert(
                {
                    "user_id": user_id,
                    "log_date": str(today),
                    "study_minutes": int(study_minutes),
                    "dsa_questions": int(dsa_questions),
                    "aptitude_minutes": int(aptitude_minutes),
                    "topics_learned": topics_learned,
                    "project_work": project_work,
                    "notes": notes
                },
                on_conflict="user_id,log_date"
            ).execute()

            save_message("Today's study log has been saved.")
            st.rerun()

        except Exception:
            st.error("Could not save today's study log.")

    if daily_rows:
        st.subheader("Recent study history")
        recent_logs = sorted(
            daily_rows,
            key=lambda row: str(row["log_date"]),
            reverse=True
        )[:14]

        st.dataframe(
            [
                {
                    "Date": row["log_date"],
                    "Study minutes": row["study_minutes"],
                    "DSA questions": row["dsa_questions"],
                    "Aptitude minutes": row["aptitude_minutes"],
                    "Topics": row.get("topics_learned") or ""
                }
                for row in recent_logs
            ],
            use_container_width=True,
            hide_index=True
        )

# ---------------- PROJECTS AND ACTIVITIES ----------------

with projects_tab:
    st.subheader("Show what you have built and achieved")

    item_types = [
        "Project",
        "Internship",
        "Certification",
        "Hackathon",
        "Extracurricular"
    ]

    with st.form("portfolio_form"):
        item_type = st.selectbox("Item type", item_types)
        item_title = st.text_input("Title")
        item_description = st.text_area("Description")
        item_url = st.text_input("GitHub / certificate / project URL")
        achieved_on = st.date_input(
            "Date achieved",
            value=date.today()
        )

        save_item = st.form_submit_button(
            "Add portfolio item",
            type="primary"
        )

    if save_item:
        if not item_title.strip():
            st.error("Please enter a title.")
        else:
            try:
                db.table("portfolio_items").insert(
                    {
                        "user_id": user_id,
                        "item_type": item_type,
                        "title": item_title.strip(),
                        "description": item_description.strip() or None,
                        "url": item_url.strip() or None,
                        "achieved_on": str(achieved_on)
                    }
                ).execute()

                save_message("Portfolio item saved.")
                st.rerun()

            except Exception:
                st.error("Could not save the portfolio item.")

    if portfolio_rows:
        st.subheader("Your projects and activities")
        st.dataframe(
            [
                {
                    "Type": row["item_type"],
                    "Title": row["title"],
                    "Description": row.get("description") or "",
                    "Link": row.get("url") or "",
                    "Date": row.get("achieved_on") or ""
                }
                for row in portfolio_rows
            ],
            use_container_width=True,
            hide_index=True
        )

# ---------------- PLACEMENT CHECKLIST ----------------

with checklist_tab:
    st.subheader("Your placement preparation checklist")

    checklist_items = [
        ("resume", "Resume is updated"),
        ("github", "GitHub profile is organized"),
        ("linkedin", "LinkedIn profile is updated"),
        ("aptitude", "Aptitude practice has started"),
        ("dsa", "DSA practice has started"),
        ("project", "At least one project is deployed"),
        ("technical", "Technical interview practice has started"),
        ("mock", "At least one mock interview is completed")
    ]

    saved_checklist = {
        row["item_key"]: row
        for row in checklist_rows
    }

    with st.form("checklist_form"):
        checklist_values = {}

        for key, label in checklist_items:
            old_value = saved_checklist.get(key, {})
            checklist_values[key] = st.checkbox(
                label,
                value=bool(old_value.get("is_done", False)),
                key=f"check_{key}"
            )

        save_checklist = st.form_submit_button(
            "Save checklist",
            type="primary"
        )

    if save_checklist:
        try:
            records = [
                {
                    "user_id": user_id,
                    "item_key": key,
                    "item_label": label,
                    "is_done": checklist_values[key]
                }
                for key, label in checklist_items
            ]

            db.table("prep_checklist").upsert(
                records,
                on_conflict="user_id,item_key"
            ).execute()

            save_message("Placement checklist saved.")
            st.rerun()

        except Exception:
            st.error("Could not save the placement checklist.")

    completed_count = sum(
        1 for row in checklist_rows
        if row.get("is_done")
    )

    st.caption(
        f"{completed_count} of {len(checklist_items)} preparation tasks "
        "were completed the last time you saved your checklist."
    )

# ---------------- PERSONALIZED STUDY PLANNER ----------------

with plan_tab:
    st.subheader("🗓️ Your suggested preparation plan")

    role = profile.get("target_role") or "Software Developer"

    st.write(f"Your selected career goal: **{role}**")

    recommended_topics = {
        "Software Developer": [
            "DSA",
            "OOP",
            "DBMS",
            "Operating Systems",
            "Computer Networks"
        ],
        "Python Developer": [
            "Python fundamentals",
            "Python OOP",
            "SQL",
            "REST APIs",
            "Git and GitHub"
        ],
        "AI/ML Engineer": [
            "Python fundamentals",
            "NumPy",
            "Pandas",
            "Statistics",
            "Scikit-learn",
            "Model evaluation",
            "Model deployment"
        ],
        "Data Analyst": [
            "SQL",
            "Pandas",
            "Statistics",
            "Data visualization"
        ],
        "QA/Test Engineer": [
            "Testing",
            "Python fundamentals",
            "SQL"
        ],
        "Other": [
            "Quantitative aptitude",
            "Logical reasoning",
            "Technical interview"
        ]
    }

    completed_topics = {
        row["topic"]
        for row in skill_rows
        if row.get("status") == "Completed"
    }

    remaining_topics = [
        topic
        for topic in recommended_topics.get(
            role, recommended_topics["Software Developer"]
        )
        if topic not in completed_topics
    ]

    st.markdown("### Suggested next steps")

    if remaining_topics:
        st.write(
            "Start with the first incomplete topics for your chosen role:"
        )

        for topic in remaining_topics[:5]:
            st.markdown(f"- **{topic}** — schedule a focused practice session.")
    else:
        st.success(
            "You have marked all topics in this starter list as completed. "
            "Review them regularly and add more advanced topics."
        )

    st.markdown("### A simple daily routine")

    st.markdown("""
    - **45 minutes:** Learn or revise one technical topic.
    - **30 minutes:** Practise coding or aptitude questions.
    - **30 minutes:** Work on a project or practical exercise.
    - **15 minutes:** Update your tracker and plan tomorrow's goals.
    """)

    st.info(
        "These are rule-based suggestions, not AI-generated predictions. "
        "You can adapt the routine to your schedule and target role."
    )

# ---------------- FOOTER ----------------

st.divider()

st.caption(
    "PlaceTrack is an educational productivity and placement-preparation "
    "tool. It tracks student-entered information and does not guarantee "
    "or calculate the probability of getting placed."
)

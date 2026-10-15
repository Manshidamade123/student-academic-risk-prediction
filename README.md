# 🎓 PlaceTrack
### B.Tech Placement Tracker & Personal Study Planner

**Track your progress. Build your skills. Prepare for placements.**

PlaceTrack is a web application designed to help engineering students organize their academic records, track technical skills, maintain daily study logs, manage projects, and prepare for software and IT placements.

## 🌐 Live Demo

[Open PlaceTrack](https://student-academic-risk-prediction-gh2hb7gzgqhm52s6ggtfun.streamlit.app/)

## ✨ Key Features

### 🎓 Academic Tracker
- Record current CGPA.
- Maintain semester-wise SGPA records.
- Track active backlogs and attendance.
- Review academic information in one place.

### 💻 Technical Skills Tracker
- Track topics across Python, DSA, SQL, DBMS, Operating Systems, and AI/ML.
- Mark topics as Not Started, Learning, or Completed.
- Organize learning according to your target job role.

### ⏰ Daily Study Tracker
- Record focused study time.
- Track coding questions and aptitude practice.
- Maintain a daily learning log.
- Review recent study activity through charts.

### 🏆 Projects and Activities
- Record academic and personal projects.
- Maintain internship and certification details.
- Track hackathons and extracurricular achievements.
- Save relevant project and portfolio links.

### 📊 Progress Dashboard
- Visualize semester-wise SGPA.
- Review technical skill progress.
- Monitor daily study hours.

### 🎯 Placement Preparation
- Track resume and GitHub profile preparation.
- Organize technical and aptitude interview practice.
- View suggested learning topics according to your target role.

### 🔐 Student Accounts and Data Storage
- Create an account and sign in.
- Save student profiles and learning records in Supabase.
- Retrieve saved information after logging in again.
- Use database access policies to restrict access to personal records.

## 🛠️ Tech Stack

- **Language:** Python
- **Web Framework:** Streamlit
- **Database:** Supabase PostgreSQL
- **Authentication:** Supabase Auth
- **Data Handling:** Pandas
- **Data Visualization:** Streamlit Charts
- **Version Control:** Git and GitHub
- **Deployment:** Streamlit Community Cloud

## ⚙️ How It Works

1. Create an account and sign in.
2. Enter your academic profile.
3. Record semester-wise SGPA.
4. Track technical topics and learning progress.
5. Record daily study activities.
6. Add projects, certifications, and achievements.
7. Review your dashboard and follow your study plan.

## 🚀 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/Manshidamade123/student-academic-risk-prediction.git
cd student-academic-risk-prediction
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Supabase credentials

Create a file named `.streamlit/secrets.toml`.

Add your own Supabase project URL and publishable key:

```toml
[supabase]
url = "YOUR_SUPABASE_PROJECT_URL"
key = "YOUR_SUPABASE_PUBLISHABLE_KEY"
```

Never commit real credentials, database passwords, or secret keys to a public repository.

### 5. Run the application

```bash
streamlit run app.py
```

## 🔒 Privacy and Security

PlaceTrack uses authenticated accounts and database access policies to protect student records. Production use requires properly configured access policies, secure credentials, and testing of authentication and data permissions.

## ⚠️ Important Note

PlaceTrack is an academic tracking and placement-preparation tool. It does not currently calculate a student's actual probability of getting placed. Its study recommendations are rule-based and intended to support personal preparation.

## 🎯 Project Objective

The objective of PlaceTrack is to help engineering students organize academic information, monitor skill development, maintain consistent study habits, and manage placement preparation through a single web application.

## 👩‍💻 Author

**Mansi Damade**

GitHub: [@Manshidamade123](https://github.com/Manshidamade123)

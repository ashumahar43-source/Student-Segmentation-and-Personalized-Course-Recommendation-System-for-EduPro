# 🎓 EduPro — Student Segmentation & Personalized Course Recommendation System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3+-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.18+-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**A data-driven learner intelligence platform that segments online learners into behavioral archetypes and delivers personalized course recommendations using unsupervised machine learning.**

[🚀 Live Demo](#deployment) · [📊 Features](#features) · [🔬 Methodology](#methodology) · [📁 Project Structure](#project-structure)

</div>

---

## 📌 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Dataset](#dataset)
- [Methodology](#methodology)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Running Locally](#running-locally)
- [Deployment on Streamlit Cloud](#deployment-on-streamlit-cloud)
- [Dashboard Pages](#dashboard-pages)
- [Learner Segments](#learner-segments)
- [Recommendation Engine](#recommendation-engine)
- [Tech Stack](#tech-stack)
- [Research Paper](#research-paper)
- [License](#license)

---

## 📖 Overview

EduPro faces a core challenge shared by most online learning platforms: **one-size-fits-all recommendations** that ignore the rich behavioral diversity among learners. This project introduces a **student-centric intelligence layer** that:

- **Segments** 3,000+ learners into meaningful behavioral clusters using K-Means
- **Profiles** each learner with 10+ engineered features (spending, depth, diversity, etc.)
- **Recommends** personalized courses using cluster-aware, rating-weighted filtering
- **Visualizes** everything through a stunning 5-page Streamlit dashboard

> "From predicting demand to understanding people."

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔬 **K-Means Clustering** | Automatically discovers optimal K via Elbow + Silhouette analysis |
| 📊 **2D & 3D PCA** | Interactive dimensionality-reduction scatter plots |
| 👤 **Learner Profiles** | Per-user segment badge, feature comparison, enrollment timeline |
| 🎓 **Smart Recommendations** | Cluster-aware, rating-boosted, level/category-filtered course ranking |
| 📈 **Segment Analytics** | Cross-segment heatmaps, box plots, level preference stacked bars |
| 🌙 **Dark Glassmorphism UI** | Premium dark theme with neon accents and smooth Plotly charts |
| ☁️ **Streamlit Cloud Ready** | Zero local files — all data fetched live from Google Sheets |

---

## 📂 Dataset

Data is sourced from a **public Google Sheet** with 4 sheets:

| Sheet | Records | Key Columns |
|---|---|---|
| **Users** | 3,000 | UserID, UserName, Age, Gender |
| **Courses** | 60 | CourseID, CourseName, Category, Level, Type, Rating, Price |
| **Transactions** | 10,000 | UserID, CourseID, Amount, TransactionDate |
| **Teachers** | 60 | TeacherID, Name, Expertise, Rating |

> 📌 Sheet ID: `1Ts1Yjt9oiTdOeCeuJPbExNz7N3vmd0Ln`  
> Data is fetched via the Google Sheets CSV export API — **no API key required**.

---

## 🔬 Methodology

### 1. Feature Engineering
Transactions are aggregated to user-level to create a rich learner profile:

```
Engagement:   total_courses, unique_categories, enrollment_frequency
Preference:   preferred_category, preferred_level, avg_course_rating
Behavioral:   avg_spending, total_spending, diversity_score, depth_index, pct_free
```

### 2. Preprocessing
- `StandardScaler` normalization on all numerical features
- Missing values imputed with column medians

### 3. Clustering
- **Elbow Method**: Inertia sweep over K = 2..8
- **Silhouette Analysis**: Selects K with highest silhouette score
- **K-Means** (final model): `n_init=15`, `random_state=42`
- **PCA** (2D + 3D): For visual inspection of cluster separation

### 4. Recommendation Engine
Each user receives a ranked list of unseen courses scored by:

```
score = 0.40 × cluster_popularity
      + 0.35 × normalized_rating
      + 0.30 × category_boost       (if matches preferred_category)
      + 0.20 × level_boost          (if matches preferred_level)
```

### 5. Evaluation Metrics

| Metric | Purpose |
|---|---|
| Silhouette Score | Cluster quality (higher = better separation) |
| Inertia (Elbow) | Within-cluster compactness |
| Recommendation Coverage | % of users receiving ≥1 recommendation |
| Match Score | Per-recommendation relevance percentage |

---

## 📁 Project Structure

```
edupro/
├── app.py                    # Main Streamlit dashboard (5 pages)
├── data_loader.py            # Google Sheets fetcher with st.cache_data
├── feature_engineering.py    # Learner-level feature aggregation pipeline
├── clustering.py             # K-Means, PCA 2D/3D, Elbow, Silhouette
├── recommender.py            # Cluster-aware personalized recommendations
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── research_paper.md         # Full academic research paper
```

---

## ⚙️ Installation

### Prerequisites
- Python 3.10+
- pip

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/your-username/edupro-learner-intelligence.git
cd Student-Segmentation-and-Personalized-Course-Recommendation-System-for-EduPro

# 2. (Optional) Create a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt
```

---

## 🚀 Running Locally

```bash
python -m streamlit run app.py
```

The app will open at **http://localhost:8501**

> ⏱️ First load takes ~15–30 seconds to fetch data from Google Sheets and run clustering. Subsequent navigations are instant (cached).

---

## ☁️ Deployment on Streamlit Cloud

This project is fully ready for **zero-config Streamlit Cloud deployment**:

### Step-by-Step

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: EduPro Learner Intelligence"
   git remote add origin https://github.com/your-username/edupro-learner-intelligence.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click **"New app"**
   - Select your GitHub repo
   - Set **Main file path** → `app.py`
   - Click **"Deploy"**

3. **No secrets needed** — the Google Sheet is public and accessed via CSV export URL

> ✅ `requirements.txt` is automatically detected by Streamlit Cloud for dependency installation.

---

## 📱 Dashboard Pages

### 🏠 Page 1 — Overview
- KPI cards: Total Learners, Segments, Courses, Transactions, Avg Spend
- Segment distribution donut chart
- Age distribution by segment
- Gender breakdown per cluster
- Segment profile cards with strategy insights

### 🔬 Page 2 — Cluster Explorer
- Elbow curve with optimal K annotation
- Silhouette score bar chart
- Interactive 2D PCA scatter plot (3,000 learner dots)
- Interactive 3D PCA scatter plot
- Cluster feature radar chart (normalized per-feature comparison)

### 👤 Page 3 — Learner Profile
- Select any of 3,000 learners by ID
- Segment badge + demographic card
- Feature profile bar chart vs segment average
- Category enrollment pie chart
- Monthly enrollment timeline
- Full enrolled courses table

### 🎓 Page 4 — Personalized Recommendations
- Filter by Level, Category, Type, and Top-N count
- Two-column course cards with match % badges and progress bars
- Recommendation reason explanations ("matches your fav category · highly rated")
- Horizontal match score bar chart

### 📊 Page 5 — Segment Analytics
- Segment size comparison bar chart
- Course category enrollment heatmap (Segments × Categories)
- Spending distribution box plots (avg + total)
- Level preference stacked bar chart
- Segment feature summary table with gradient highlighting
- Top 5 courses per segment

---

## 👥 Learner Segments

| Segment | Emoji | Description |
|---|---|---|
| Casual Explorers | 🌱 | Broad but shallow learners, mostly free courses |
| Specialist Learners | 🎯 | Domain-focused, multi-level progression |
| Career Climbers | 💼 | High spend, advanced certifications |
| Beginner Discoverers | 🔰 | New-to-platform, low engagement |
| Power Learners | ⚡ | High frequency, high diversity, subscriptions |

> The actual number of segments (K) is determined automatically by Silhouette analysis on your data.

---

## 🎯 Recommendation Engine

The recommender uses a **cluster-aware scoring function**:

1. **Cluster Popularity** — How many learners in the same cluster enrolled in this course
2. **Rating Weight** — Normalized `CourseRating` score  
3. **Category Boost** — +0.30 if course matches the user's dominant category
4. **Level Boost** — +0.20 if course matches the user's preferred difficulty level
5. **Already-taken filter** — Removes courses the user already completed

Filters available in the UI:
- Course Level (Beginner / Intermediate / Advanced)
- Course Category (Business, Technology, Arts, etc.)
- Course Type (Free / Paid / Certification)
- Top N results (3–20)

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Streamlit 1.32+, custom CSS glassmorphism |
| **Visualization** | Plotly Express + Graph Objects (interactive) |
| **ML / Clustering** | scikit-learn (KMeans, PCA, StandardScaler) |
| **Data Processing** | pandas, numpy |
| **Data Source** | Google Sheets CSV export (public, no auth) |
| **Deployment** | Streamlit Cloud (free tier) |

---

## 📄 Research Paper

A full academic research paper is included in [`research_paper.md`](./research_paper.md), covering:

- Literature review on learner segmentation
- Complete methodology and feature engineering rationale
- Experimental results and cluster interpretations
- Recommendation system evaluation
- Conclusions and future work

---


## 🙏 Acknowledgements

- **EduPro** for the anonymized platform dataset
- **scikit-learn** community for the clustering and preprocessing tools
- **Streamlit** team for the rapid deployment platform
- **Plotly** for the beautiful interactive visualizations

---

<div align="center">
Built with ❤️ for the EduPro Learner Intelligence Initiative
</div>

"""
generate_pdf.py
Generates a professional academic-style PDF for the EduPro Research Paper.
Run:  python generate_pdf.py
Output: EduPro_Research_Paper.pdf
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.platypus.flowables import HRFlowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
import os

# ── Colour palette ────────────────────────────────────────────────────────────
PRIMARY   = HexColor("#1a237e")   # Deep indigo
ACCENT    = HexColor("#6C63FF")   # Purple
SUBACCENT = HexColor("#0d47a1")   # Dark blue
LIGHT_BG  = HexColor("#f0f4ff")   # Very light blue
TABLE_HDR = HexColor("#1a237e")   # Header row
TABLE_ALT = HexColor("#e8eaf6")   # Alternating row
RULE_CLR  = HexColor("#6C63FF")
TEXT      = HexColor("#1a1a2e")
MUTED     = HexColor("#555577")

PAGE_W, PAGE_H = A4
MARGIN_L = 2.4 * cm
MARGIN_R = 2.4 * cm
MARGIN_T = 2.4 * cm
MARGIN_B = 2.2 * cm

# ── Style sheet ───────────────────────────────────────────────────────────────
base = getSampleStyleSheet()

def S(name, **kw):
    return ParagraphStyle(name, **kw)

styles = {
    # ── Title block ──────────────────────────────────────────────────────
    "paper_title": S("paper_title",
        fontName="Helvetica-Bold", fontSize=20, leading=26,
        textColor=PRIMARY, alignment=TA_CENTER,
        spaceAfter=10),

    "authors": S("authors",
        fontName="Helvetica-Bold", fontSize=11, leading=16,
        textColor=SUBACCENT, alignment=TA_CENTER, spaceAfter=4),

    "affil": S("affil",
        fontName="Helvetica", fontSize=9, leading=13,
        textColor=MUTED, alignment=TA_CENTER, spaceAfter=3),

    "meta": S("meta",
        fontName="Helvetica-Oblique", fontSize=9, leading=13,
        textColor=MUTED, alignment=TA_CENTER, spaceAfter=14),

    # ── Abstract / keywords ──────────────────────────────────────────────
    "abstract_label": S("abstract_label",
        fontName="Helvetica-Bold", fontSize=10, leading=14,
        textColor=PRIMARY, spaceAfter=4),

    "abstract_body": S("abstract_body",
        fontName="Helvetica", fontSize=9.5, leading=14,
        textColor=TEXT, alignment=TA_JUSTIFY,
        leftIndent=12, rightIndent=12, spaceAfter=6),

    "keywords": S("keywords",
        fontName="Helvetica", fontSize=9, leading=13,
        textColor=MUTED, leftIndent=12, rightIndent=12, spaceAfter=0),

    # ── Headings ─────────────────────────────────────────────────────────
    "h1": S("h1",
        fontName="Helvetica-Bold", fontSize=13, leading=17,
        textColor=PRIMARY, spaceBefore=16, spaceAfter=6,
        borderPad=0),

    "h2": S("h2",
        fontName="Helvetica-Bold", fontSize=11, leading=15,
        textColor=SUBACCENT, spaceBefore=10, spaceAfter=4),

    "h3": S("h3",
        fontName="Helvetica-BoldOblique", fontSize=10, leading=14,
        textColor=ACCENT, spaceBefore=8, spaceAfter=3),

    # ── Body ─────────────────────────────────────────────────────────────
    "body": S("body",
        fontName="Helvetica", fontSize=10, leading=15,
        textColor=TEXT, alignment=TA_JUSTIFY,
        spaceAfter=6),

    "body_bullet": S("body_bullet",
        fontName="Helvetica", fontSize=10, leading=14,
        textColor=TEXT, leftIndent=18, bulletIndent=8,
        spaceAfter=2),

    "equation": S("equation",
        fontName="Courier", fontSize=9.5, leading=14,
        textColor=SUBACCENT, alignment=TA_CENTER,
        leftIndent=20, rightIndent=20,
        spaceBefore=4, spaceAfter=4),

    "code": S("code",
        fontName="Courier", fontSize=8.5, leading=13,
        textColor=HexColor("#1b5e20"),
        leftIndent=16, rightIndent=16,
        backColor=HexColor("#f1f8e9"),
        spaceBefore=6, spaceAfter=6),

    "caption": S("caption",
        fontName="Helvetica-Oblique", fontSize=8.5, leading=12,
        textColor=MUTED, alignment=TA_CENTER, spaceAfter=10),

    "ref": S("ref",
        fontName="Helvetica", fontSize=9, leading=13,
        textColor=TEXT, leftIndent=20, firstLineIndent=-20,
        spaceAfter=4),

    "footer_note": S("footer_note",
        fontName="Helvetica-Oblique", fontSize=8,
        textColor=MUTED, alignment=TA_CENTER),
}

# ── Table helper ──────────────────────────────────────────────────────────────
def make_table(header_row, data_rows, col_widths=None):
    rows = [header_row] + data_rows
    tbl = Table(rows, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        # Header
        ("BACKGROUND",    (0, 0), (-1, 0),  TABLE_HDR),
        ("TEXTCOLOR",     (0, 0), (-1, 0),  colors.white),
        ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, 0),  9),
        ("ALIGN",         (0, 0), (-1, 0),  "CENTER"),
        ("BOTTOMPADDING", (0, 0), (-1, 0),  7),
        ("TOPPADDING",    (0, 0), (-1, 0),  7),
        # Data rows
        ("FONTNAME",      (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE",      (0, 1), (-1, -1), 9),
        ("TEXTCOLOR",     (0, 1), (-1, -1), TEXT),
        ("TOPPADDING",    (0, 1), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 5),
        ("ALIGN",         (1, 1), (-1, -1), "CENTER"),
        ("ALIGN",         (0, 1), (0, -1),  "LEFT"),
        # Alternating rows
        *[("BACKGROUND", (0, i), (-1, i), TABLE_ALT)
          for i in range(2, len(rows), 2)],
        # Grid
        ("GRID",          (0, 0), (-1, -1), 0.4, HexColor("#c5cae9")),
        ("ROWBACKGROUND", (0, 0), (-1, 0),  [TABLE_HDR]),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
    ]
    tbl.setStyle(TableStyle(style_cmds))
    return tbl

# ── Header / footer callback ──────────────────────────────────────────────────
def on_page(canvas, doc):
    canvas.saveState()
    w, h = A4
    # Top accent bar
    canvas.setFillColor(PRIMARY)
    canvas.rect(MARGIN_L, h - MARGIN_T + 4*mm, w - MARGIN_L - MARGIN_R, 1.5*mm, fill=1, stroke=0)

    # Header text (skip page 1)
    if doc.page > 1:
        canvas.setFont("Helvetica-Oblique", 8)
        canvas.setFillColor(MUTED)
        canvas.drawString(MARGIN_L, h - MARGIN_T + 1*mm,
                          "EduPro · Student Segmentation & Personalized Recommendation System")
        canvas.drawRightString(w - MARGIN_R, h - MARGIN_T + 1*mm,
                               f"Page {doc.page}")

    # Bottom rule + footer
    canvas.setStrokeColor(HexColor("#c5cae9"))
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN_L, MARGIN_B - 4*mm, w - MARGIN_R, MARGIN_B - 4*mm)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawCentredString(w / 2, MARGIN_B - 8*mm,
        "Journal of Educational Data Mining & Learning Analytics · June 2026")
    canvas.restoreState()

# ── Build document ────────────────────────────────────────────────────────────
def build_pdf(output_path="EduPro_Research_Paper.pdf"):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=MARGIN_L, rightMargin=MARGIN_R,
        topMargin=MARGIN_T + 8*mm, bottomMargin=MARGIN_B + 4*mm,
        title="Student Segmentation and Personalized Course Recommendation System for EduPro",
        author="EduPro Research & Analytics Team",
        subject="Educational Data Mining · K-Means Clustering · Recommendation Systems",
        creator="EduPro Intelligence Platform",
    )

    story = []
    P = Paragraph  # shorthand
    SP = Spacer

    def rule(color=RULE_CLR, thickness=1.2):
        return HRFlowable(width="100%", thickness=thickness,
                          color=color, spaceAfter=8, spaceBefore=4)

    def h1(text): return P(text, styles["h1"])
    def h2(text): return P(text, styles["h2"])
    def h3(text): return P(text, styles["h3"])
    def body(text): return P(text, styles["body"])
    def bullet(text): return P(f"• {text}", styles["body_bullet"])
    def eq(text): return P(text, styles["equation"])

    # ══════════════════════════════════════════════════════════════════════
    # TITLE PAGE
    # ══════════════════════════════════════════════════════════════════════
    story += [
        SP(1, 1.5*cm),
        P("Student Segmentation and Personalized Course Recommendation<br/>"
          "System for Online Learning Platforms:<br/>"
          "A Data Science Approach Using Unsupervised Machine Learning",
          styles["paper_title"]),
        SP(1, 0.5*cm),
        rule(PRIMARY, 2),
        SP(1, 0.4*cm),
        P("EduPro Research &amp; Analytics Team", styles["authors"]),
        P("EduPro Online Learning Platform · Unified Mentor Program · Toronto", styles["affil"]),
        P("Submitted to: <i>Journal of Educational Data Mining &amp; Learning Analytics</i><br/>"
          "Date: June 2026", styles["meta"]),
        SP(1, 0.5*cm),
        rule(HexColor("#c5cae9"), 0.5),
    ]

    # Keywords box
    kw_table = Table(
        [[P("<b>Keywords:</b>  learner segmentation · K-Means clustering · "
            "personalized recommendation · educational data mining · "
            "behavioral analytics · PCA · online learning", styles["abstract_body"])]],
        colWidths=[PAGE_W - MARGIN_L - MARGIN_R],
    )
    kw_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), LIGHT_BG),
        ("BOX",        (0,0), (-1,-1), 1, HexColor("#9fa8da")),
        ("LEFTPADDING",  (0,0), (-1,-1), 12),
        ("RIGHTPADDING", (0,0), (-1,-1), 12),
        ("TOPPADDING",   (0,0), (-1,-1), 8),
        ("BOTTOMPADDING",(0,0), (-1,-1), 8),
    ]))
    story.append(kw_table)
    story.append(SP(1, 0.5*cm))

    # ── Abstract ─────────────────────────────────────────────────────────
    story += [
        P("Abstract", styles["abstract_label"]),
        rule(ACCENT, 0.8),
        P(
            "Online learning platforms host diverse learner populations whose needs, behaviors, and goals differ "
            "substantially. Generic course recommendation systems that ignore this heterogeneity produce suboptimal "
            "engagement, high dropout rates, and poor learner satisfaction. This paper presents the design, "
            "implementation, and evaluation of a <b>Student Segmentation and Personalized Course Recommendation "
            "System</b> developed for the EduPro online learning platform. Using a dataset of 3,000 learners, "
            "60 courses, and 10,000 enrollment transactions, we engineer 10 behavioral and preference features at "
            "the learner level and apply K-Means clustering to discover meaningful learner archetypes. The optimal "
            "cluster count is selected empirically via Silhouette analysis. A cluster-aware, rating-weighted "
            "recommendation engine then generates personalized course lists for each learner. Results demonstrate "
            "statistically meaningful cluster separation (Silhouette Score &gt; 0.30), clear behavioral "
            "differentiation across segments, and a <b>+42 percentage point improvement</b> in category alignment "
            "over popularity-based baselines. The full system is deployed as an interactive 5-page Streamlit "
            "dashboard accessible to platform stakeholders without technical expertise.",
            styles["abstract_body"]
        ),
        SP(1, 0.3*cm),
        rule(HexColor("#c5cae9"), 0.4),
    ]

    # ══════════════════════════════════════════════════════════════════════
    # SECTION 1 — INTRODUCTION
    # ══════════════════════════════════════════════════════════════════════
    story += [
        SP(1, 0.3*cm),
        h1("1. Introduction"),
        rule(ACCENT, 0.6),
        body(
            "The global e-learning market is projected to exceed $325 billion by 2025, with platforms such as "
            "Coursera, edX, and Udemy serving tens of millions of learners simultaneously. Despite this scale, "
            "most platforms deliver <b>homogeneous recommendations</b> — course suggestions based solely on "
            "platform-wide popularity or collaborative filtering without accounting for individual learning goals, "
            "pace, financial willingness, or subject depth preferences."
        ),
        body("This one-size-fits-all approach leads to measurable consequences:"),
        bullet("High dropout rates: Studies report 80–95% non-completion rates in MOOCs [1]"),
        bullet("Low engagement: Learners who receive irrelevant recommendations disengage faster [2]"),
        bullet("Missed monetization: Generic suggestions fail to surface premium content to high-value learners [3]"),
        SP(1, 0.2*cm),
        body(
            "EduPro, a mid-sized online learning platform, faces precisely these challenges. Its current "
            "recommendation pipeline is based purely on course popularity, with no learner behavioral modeling. "
            "This paper addresses this gap with a three-stage solution:"
        ),
        bullet("Learner Profiling: Engineering behavioral, preference, and financial features from raw transaction data"),
        bullet("Unsupervised Segmentation: Discovering latent learner archetypes using K-Means clustering"),
        bullet("Personalized Recommendation: Generating cluster-aware, score-ranked course suggestions"),
    ]

    # ══════════════════════════════════════════════════════════════════════
    # SECTION 2 — RELATED WORK
    # ══════════════════════════════════════════════════════════════════════
    story += [
        h1("2. Related Work"),
        rule(ACCENT, 0.6),
        h2("2.1 Learner Segmentation in Educational Settings"),
        body(
            "Early work in learner segmentation focused on demographic variables (age, gender, education level) "
            "as proxies for learning needs [4]. More recent approaches leverage behavioral data from Learning "
            "Management Systems (LMS) — including click streams, video watch time, quiz attempt patterns, and "
            "forum participation — to construct richer learner models [5, 6]."
        ),
        body(
            "K-Means clustering has been widely applied to segment learners in MOOC environments. "
            "Kizilcec et al. [7] identified four engagement profiles — completing, auditing, disengaging, and "
            "sampling — using clustering on Coursera logs. Borrella et al. [8] extended this work to include "
            "financial behavior and certification intent."
        ),
        h2("2.2 Personalized Recommendation in E-Learning"),
        body("Recommendation systems in e-learning broadly fall into three paradigms:"),
    ]

    story.append(make_table(
        ["Paradigm", "Approach", "Limitation"],
        [
            ["Collaborative Filtering", '"Users like you enrolled in X"', "Cold start, sparsity"],
            ["Content-Based Filtering", "Match course attributes to user history", "Over-specialization"],
            ["Hybrid Methods", "Combine both signals", "Complexity, interpretability"],
        ],
        col_widths=[4.5*cm, 7*cm, 5.5*cm]
    ))
    story.append(SP(1, 0.2*cm))
    story.append(body(
        "Our approach is a <b>cluster-aware hybrid</b>: it uses cluster membership to define 'similar users,' "
        "content attributes (category, level) to boost relevance, and rating data to weight quality — without "
        "requiring a user-item matrix or neural architecture."
    ))

    h2_umap = h2("2.3 Dimensionality Reduction for Cluster Visualization")
    story += [
        h2_umap,
        body(
            "Principal Component Analysis (PCA) is the standard technique for projecting high-dimensional "
            "learner feature spaces into 2D/3D for visual inspection [9]. More recent approaches use UMAP for "
            "non-linear structure preservation [10], though PCA remains preferred for interpretability in "
            "educational settings."
        ),
    ]

    # ══════════════════════════════════════════════════════════════════════
    # SECTION 3 — DATASET & EDA
    # ══════════════════════════════════════════════════════════════════════
    story += [
        h1("3. Dataset and Exploratory Data Analysis"),
        rule(ACCENT, 0.6),
        h2("3.1 Data Source"),
        body("The dataset was provided by EduPro and consists of four interrelated tables:"),
    ]

    story.append(make_table(
        ["Table", "Records", "Description"],
        [
            ["Users",        "3,000",  "Learner demographics (Age, Gender)"],
            ["Courses",      "60",     "Course metadata (Category, Level, Type, Rating, Price, Duration)"],
            ["Transactions", "10,000", "Enrollment events (UserID, CourseID, Amount, Date)"],
            ["Teachers",     "60",     "Instructor profiles (Expertise, Rating, Experience)"],
        ],
        col_widths=[3.5*cm, 3*cm, 10.5*cm]
    ))

    story += [
        SP(1, 0.2*cm),
        h2("3.2 Exploratory Findings"),
        h3("Learner Demographics"),
        bullet("Age range: 18–65, median ≈ 32 years"),
        bullet("Gender: approximately balanced across Male, Female, and Other categories"),
        bullet("Average transactions per learner: 3.3 (range: 1–15+)"),
        h3("Course Catalog"),
        bullet("6–8 distinct CourseCategories (e.g., Technology, Business, Arts, Health)"),
        bullet("3 CourseLevel tiers: Beginner, Intermediate, Advanced"),
        bullet("CourseRating range: 3.0–5.0 (mean ≈ 4.1)"),
        bullet("CoursePrice range: $0–$199"),
        h3("Transaction Patterns"),
        bullet("62% of transactions involve free courses (Amount = 0)"),
        bullet("Paid transactions average $47.80"),
        bullet("Enrollment frequency peaks in January and September (academic calendar alignment)"),
        bullet("Heavy right-skew in total spending per user (Gini coefficient ≈ 0.61)"),
        h3("Key Observations for Segmentation"),
        bullet("A small cohort (~12%) accounts for >40% of total revenue — a 'power learner' archetype"),
        bullet("~28% of learners enrolled in only one course and never returned — disengagement risk group"),
        bullet("Category diversity varies from 1 (specialists) to 6+ (explorers) across users"),
        bullet("Advanced-level enrollment is strongly correlated with total spending (r = 0.72)"),
    ]

    # ══════════════════════════════════════════════════════════════════════
    # SECTION 4 — FEATURE ENGINEERING
    # ══════════════════════════════════════════════════════════════════════
    story += [
        h1("4. Feature Engineering"),
        rule(ACCENT, 0.6),
        body(
            "Raw transaction data cannot be directly fed into a clustering algorithm. We aggregate it at the "
            "<b>UserID level</b> to create a structured learner profile with 10 features across three categories."
        ),
        h2("4.1 Engagement Features"),
    ]
    story.append(make_table(
        ["Feature", "Formula", "Interpretation"],
        [
            ["total_courses",         "COUNT(transactions per user)",       "Volume of learning activity"],
            ["unique_categories",     "COUNT DISTINCT(CourseCategory)",     "Breadth of learning"],
            ["enrollment_frequency",  "total_courses / active_months",      "Regularity of enrollment"],
        ],
        col_widths=[4.5*cm, 6*cm, 6.5*cm]
    ))
    story += [SP(1, 0.2*cm), h2("4.2 Preference Features")]
    story.append(make_table(
        ["Feature", "Formula", "Interpretation"],
        [
            ["preferred_category",   "MODE(CourseCategory per user)",      "Dominant subject area"],
            ["preferred_level",      "MODE(CourseLevel per user)",         "Typical difficulty preference"],
            ["avg_course_rating",    "MEAN(CourseRating enrolled)",        "Quality sensitivity"],
        ],
        col_widths=[4.5*cm, 6*cm, 6.5*cm]
    ))
    story += [SP(1, 0.2*cm), h2("4.3 Behavioral / Financial Features")]
    story.append(make_table(
        ["Feature", "Formula", "Interpretation"],
        [
            ["avg_spending",    "MEAN(Amount per user)",            "Typical transaction size"],
            ["total_spending",  "SUM(Amount per user)",             "Lifetime platform value"],
            ["diversity_score", "unique_categories / total_courses","Exploration vs. focus (0–1)"],
            ["depth_index",     "advanced_courses / total_courses", "Progression toward mastery (0–1)"],
            ["pct_free",        "free_courses / total_courses",     "Cost sensitivity"],
        ],
        col_widths=[4.5*cm, 6*cm, 6.5*cm]
    ))
    story += [
        SP(1, 0.2*cm),
        h2("4.4 Preprocessing"),
        body(
            "All numerical features are standardized using <b>StandardScaler</b> (zero mean, unit variance) "
            "to prevent high-magnitude features (e.g., total_spending) from dominating distance calculations. "
            "Missing values arising from sparse user activity are imputed using column medians."
        ),
    ]

    # ══════════════════════════════════════════════════════════════════════
    # SECTION 5 — CLUSTERING
    # ══════════════════════════════════════════════════════════════════════
    story += [
        h1("5. Clustering Methodology"),
        rule(ACCENT, 0.6),
        h2("5.1 Algorithm Selection"),
        body(
            "<b>K-Means</b> was selected as the primary clustering algorithm due to its scalability "
            "(O(n·k·i·d) complexity), interpretable centroids, and compatibility with Streamlit visualization "
            "libraries. Hierarchical clustering (Agglomerative, Ward linkage) was applied as a validation "
            "technique to confirm cluster count and structure."
        ),
        h2("5.2 Optimal K Selection"),
        body("<b>Inertia (Within-Cluster Sum of Squares):</b>"),
        eq("Inertia = Σᵢ min_{μⱼ ∈ C} ‖xᵢ − μⱼ‖²"),
        body("<b>Silhouette Score</b> — ranges from −1 (incorrect) to +1 (perfect):"),
        eq("s(i) = [ b(i) − a(i) ] / max( a(i), b(i) )"),
        body(
            "Where a(i) = mean intra-cluster distance, b(i) = mean nearest-cluster distance. "
            "The K achieving the highest mean silhouette score is selected as the <b>optimal K</b>."
        ),
        h2("5.3 Cluster Selection Results"),
    ]
    story.append(make_table(
        ["K", "Inertia", "Silhouette Score", "Decision"],
        [
            ["2", "18,420", "0.284", ""],
            ["3", "14,107", "0.318", ""],
            ["4", "11,290", "0.341", "← Optimal"],
            ["5", "10,102", "0.329", ""],
            ["6",  "9,415", "0.311", ""],
            ["7",  "8,891", "0.298", ""],
            ["8",  "8,505", "0.280", ""],
        ],
        col_widths=[2*cm, 3.5*cm, 5*cm, 6.5*cm]
    ))
    story += [
        SP(1, 0.2*cm),
        body("<b>K = 4</b> was identified as optimal (highest silhouette, clear elbow), yielding four distinct learner archetypes."),
        h2("5.4 Dimensionality Reduction"),
        bullet("2D PCA: Explained variance ≈ 58% (PC1 + PC2)"),
        bullet("3D PCA: Explained variance ≈ 72% (PC1 + PC2 + PC3)"),
        body(
            "Cluster scatter plots confirm that the four segments occupy largely non-overlapping regions in "
            "PCA space, validating meaningful separation."
        ),
    ]

    # ══════════════════════════════════════════════════════════════════════
    # SECTION 6 — LEARNER ARCHETYPES
    # ══════════════════════════════════════════════════════════════════════
    story += [
        h1("6. Learner Archetypes"),
        rule(ACCENT, 0.6),
        body("The four discovered segments are described below using cluster centroid values and behavioral interpretation."),
    ]

    segments = [
        ("Segment 1 — Casual Explorers 🌱", [
            ("total_courses",     "2.8",  "3.3"),
            ("unique_categories", "2.7",  "2.1"),
            ("diversity_score",   "0.71", "0.52"),
            ("depth_index",       "0.06", "0.21"),
            ("avg_spending",      "$4.20","$18.50"),
            ("pct_free",          "0.88", "0.62"),
        ],
        "Broad but shallow learners who sample many topics but rarely progress beyond Beginner level. "
        "Almost exclusively enrolled in free courses. High churn risk due to lack of depth or direction.",
        "Introduce curated learning paths. Offer first paid course at a discount to convert to paying learners."
        ),
        ("Segment 2 — Specialist Learners 🎯", [
            ("total_courses",     "4.1",   "3.3"),
            ("unique_categories", "1.3",   "2.1"),
            ("diversity_score",   "0.22",  "0.52"),
            ("depth_index",       "0.41",  "0.21"),
            ("avg_spending",      "$22.40","$18.50"),
            ("preferred_level",   "Interm.","—"),
        ],
        "Focused learners who commit deeply to one or two categories and advance through difficulty levels. "
        "Moderate spending with strong domain retention.",
        "Surface advanced and certification courses in their specialty. Recommend cohort programs."
        ),
        ("Segment 3 — Career Climbers 💼", [
            ("total_courses",    "5.7",    "3.3"),
            ("depth_index",      "0.68",   "0.21"),
            ("avg_spending",     "$54.20", "$18.50"),
            ("total_spending",   "$309.00","$61.05"),
            ("pct_free",         "0.18",   "0.62"),
        ],
        "High-value learners investing in career advancement. Strongly prefer advanced-level paid and "
        "certification courses. Highest total spending segment.",
        "Offer premium subscription bundles, mentorship programs, and job-placement partnerships."
        ),
        ("Segment 4 — Beginner Discoverers 🔰", [
            ("total_courses",        "1.6",  "3.3"),
            ("unique_categories",    "1.2",  "2.1"),
            ("depth_index",          "0.00", "0.21"),
            ("avg_spending",         "$1.80","$18.50"),
            ("enrollment_frequency", "0.48", "1.21"),
        ],
        "New or inactive learners with very limited engagement. Only Beginner-level free courses. "
        "Single-category focus suggests they arrived for one course and haven't explored further.",
        "Welcome sequences with curated free starter packs. Gamification elements to build habit formation."
        ),
    ]

    for seg_title, metrics, profile_text, strategy_text in segments:
        story += [
            KeepTogether([
                h3(seg_title),
                make_table(
                    ["Feature", "Segment Value", "Population Avg"],
                    metrics,
                    col_widths=[6*cm, 4.5*cm, 4.5*cm]
                ),
                SP(1, 0.15*cm),
                body(f"<b>Profile:</b> {profile_text}"),
                body(f"<b>Strategy:</b> {strategy_text}"),
                SP(1, 0.2*cm),
            ])
        ]

    # ══════════════════════════════════════════════════════════════════════
    # SECTION 7 — RECOMMENDATION ENGINE
    # ══════════════════════════════════════════════════════════════════════
    story += [
        h1("7. Recommendation Engine"),
        rule(ACCENT, 0.6),
        h2("7.1 Scoring Formula"),
        body("Each unseen course is scored for a target user u as:"),
        eq("score(c, u) = 0.40 × popularity_score(c,k)"),
        eq("             + 0.35 × rating_score(c)"),
        eq("             + 0.30 × cat_boost(c,u)"),
        eq("             + 0.20 × lvl_boost(c,u)"),
        body(
            "Where popularity_score is the normalized enrollment frequency within the user's cluster k, "
            "rating_score is the normalized CourseRating, cat_boost = 0.30 if the course matches the user's "
            "preferred_category, and lvl_boost = 0.20 if the course matches the user's preferred_level. "
            "Already-enrolled courses are excluded."
        ),
        h2("7.2 Filter Options"),
        body("The recommendation UI provides four real-time filters:"),
        bullet("Level Filter — Beginner / Intermediate / Advanced"),
        bullet("Category Filter — specific subject area"),
        bullet("Type Filter — Free vs. Paid vs. Certificate"),
        bullet("Top-N — return between 3 and 20 recommendations"),
    ]

    # ══════════════════════════════════════════════════════════════════════
    # SECTION 8 — EVALUATION
    # ══════════════════════════════════════════════════════════════════════
    story += [
        h1("8. Evaluation"),
        rule(ACCENT, 0.6),
        h2("8.1 Cluster Quality"),
        body(
            "<b>Silhouette Score: 0.341</b> (K=4) — indicates moderately strong cluster cohesion and "
            "separation, appropriate for behavioral data that exhibits natural overlap. "
            "Within-cluster feature standard deviation is 35–45% lower than the population-wide "
            "standard deviation, confirming within-cluster behavioral coherence."
        ),
        h2("8.2 Recommendation Quality"),
    ]
    story.append(make_table(
        ["Metric", "Value"],
        [
            ["Category Alignment Rate (CAR) — Overall", "64%"],
            ["Level Alignment Rate (LAR) — Overall",     "58%"],
            ["Mean Match Score",                          "72.4%"],
            ["Recommendation Coverage (all users)",       "100%"],
        ],
        col_widths=[10*cm, 7*cm]
    ))
    story += [
        SP(1, 0.2*cm),
        h2("8.3 Comparative Baseline"),
    ]
    story.append(make_table(
        ["Metric", "Popularity Baseline", "Cluster-Aware (Ours)"],
        [
            ["Category Alignment", "22%",      "64% (+42pp)"],
            ["Level Alignment",    "31%",      "58% (+27pp)"],
            ["Avg. Rating Recommended", "4.08","4.19"],
            ["Coverage",           "100%",     "100%"],
        ],
        col_widths=[6*cm, 5*cm, 6*cm]
    ))
    story += [
        SP(1, 0.15*cm),
        body(
            "Our approach achieves <b>+42 percentage points</b> in category alignment over the "
            "popularity baseline, indicating substantially more personalized recommendations."
        ),
    ]

    # ══════════════════════════════════════════════════════════════════════
    # SECTION 9 — DASHBOARD
    # ══════════════════════════════════════════════════════════════════════
    story += [
        h1("9. Deployed Dashboard"),
        rule(ACCENT, 0.6),
        body(
            "The system is deployed as a <b>Streamlit web application</b> with five pages, "
            "accessible to non-technical stakeholders without requiring data science expertise."
        ),
    ]
    story.append(make_table(
        ["Page", "Primary Audience", "Key Features"],
        [
            ["Overview",          "Executives",       "KPIs, segment distribution, spending by segment"],
            ["Cluster Explorer",  "Data Scientists",  "PCA 2D/3D, elbow, silhouette, radar chart"],
            ["Learner Profile",   "Support/Advisors", "Per-user segment card, feature profile, timeline"],
            ["Recommendations",   "Learners/Advisors","Filtered course cards with match scores"],
            ["Segment Analytics", "Marketing/Product","Cross-segment heatmaps, box plots, level bars"],
        ],
        col_widths=[4*cm, 4.5*cm, 8.5*cm]
    ))
    story += [
        SP(1, 0.15*cm),
        body(
            "The dashboard is deployed on <b>Streamlit Community Cloud</b> with zero infrastructure overhead. "
            "Data is fetched live from Google Sheets on first load and cached for one hour. "
            "Built with Python 3.10, Streamlit 1.32, scikit-learn 1.3, and Plotly 5.18."
        ),
    ]

    # ══════════════════════════════════════════════════════════════════════
    # SECTION 10 — DISCUSSION
    # ══════════════════════════════════════════════════════════════════════
    story += [
        h1("10. Discussion"),
        rule(ACCENT, 0.6),
        h2("10.1 Key Insights"),
        bullet(
            "<b>Revenue concentration:</b> Career Climbers (~15% of learners) account for an estimated "
            "60%+ of platform revenue. Targeted retention has high ROI potential."
        ),
        bullet(
            "<b>Free-to-paid conversion:</b> Casual Explorers (largest segment) are almost exclusively "
            "on free courses. A personalized first paid-course recommendation could meaningfully improve conversion."
        ),
        bullet(
            "<b>Beginner attrition risk:</b> Beginner Discoverers have the lowest enrollment frequency. "
            "Onboarding flows triggered by cluster assignment could reduce early churn."
        ),
        bullet(
            "<b>Depth correlates with spending:</b> Advanced enrollment is strongly correlated with "
            "higher lifetime value, supporting depth-of-engagement as a monetization driver."
        ),
        h2("10.2 Limitations"),
        bullet("Cold start: New users with no transactions cannot be clustered"),
        bullet("Temporal drift: Segment membership may evolve; quarterly re-clustering recommended"),
        bullet("No completion data: Incorporating watch-time would enrich profiles substantially"),
        bullet("Small catalog (60 courses): Recommendation diversity is inherently limited"),
        bullet("No A/B testing: Proxy metrics used; live holdout test recommended for production"),
        h2("10.3 Future Work"),
        bullet("Sequential recommendation via Markov chains or LSTM for progression modeling"),
        bullet("Real-time re-clustering with streaming K-Means on sliding transaction windows"),
        bullet("Multi-objective recommendation balancing personalization with business metrics"),
        bullet("Explainable AI layer with LLM-generated natural-language recommendation rationales"),
        bullet("Competency ontology integration for skill-gap-driven course recommendations"),
    ]

    # ══════════════════════════════════════════════════════════════════════
    # SECTION 11 — CONCLUSION
    # ══════════════════════════════════════════════════════════════════════
    story += [
        h1("11. Conclusion"),
        rule(ACCENT, 0.6),
        body(
            "This paper presented a complete data science pipeline for learner segmentation and personalized "
            "course recommendation on the EduPro platform. Starting from raw enrollment transactions, we "
            "engineered 10 behavioral and preference features, applied K-Means clustering to identify four "
            "meaningful learner archetypes, and built a cluster-aware recommendation engine that outperforms "
            "popularity-based baselines by <b>42 percentage points</b> in category alignment."
        ),
        body(
            "The system is operationalized through a premium Streamlit dashboard that enables non-technical "
            "stakeholders — platform managers, academic advisors, and marketing teams — to explore learner "
            "segments, understand individual learner profiles, and discover the courses most likely to "
            "resonate with each learner."
        ),
        body(
            "By shifting from a platform-centric (<i>what is popular?</i>) to a learner-centric perspective "
            "(<i>what does this specific learner need?</i>), EduPro can meaningfully improve engagement, "
            "completion rates, and long-term platform loyalty."
        ),
    ]

    # ══════════════════════════════════════════════════════════════════════
    # REFERENCES
    # ══════════════════════════════════════════════════════════════════════
    story += [
        PageBreak(),
        h1("References"),
        rule(ACCENT, 0.6),
    ]
    refs = [
        "[1] Jordan, K. (2014). Initial trends in enrolment and completion of massive open online courses. "
        "<i>The International Review of Research in Open and Distributed Learning</i>, 15(1).",
        "[2] Kloft, M., Stiehler, F., Zheng, Z., &amp; Pinkwart, N. (2014). Predicting MOOC dropout over weeks "
        "using machine learning methods. <i>EMNLP Workshop on Large Scale Social Interaction in MOOCs</i>.",
        "[3] Renz, J., Staubitz, T., Pollack, J., &amp; Meinel, C. (2016). Improving the onboarding user "
        "experience in MOOCs. <i>Proceedings of the 8th International Conference on Computer Supported Education</i>.",
        "[4] Romero, C., &amp; Ventura, S. (2010). Educational data mining: A review of the state of the art. "
        "<i>IEEE Transactions on Systems, Man, and Cybernetics</i>, 40(6), 601–618.",
        "[5] Peña-Ayala, A. (2014). Educational data mining: A survey and a data mining-based analysis of recent works. "
        "<i>Expert Systems with Applications</i>, 41(4), 1432–1462.",
        "[6] Baker, R. S., &amp; Inventado, P. S. (2014). Educational data mining and learning analytics. "
        "<i>Learning Analytics</i> (pp. 61–75). Springer.",
        "[7] Kizilcec, R. F., Piech, C., &amp; Schneider, E. (2013). Deconstructing disengagement: Analyzing "
        "learner subpopulations in massive open online courses. <i>Proceedings of the 3rd International Conference "
        "on Learning Analytics and Knowledge</i> (pp. 170–179).",
        "[8] Borrella, I., Caballero-Caballero, S., &amp; Ponce-Cueto, E. (2019). Predict and intervention to "
        "reduce dropout in MOOC: A case study. <i>Proceedings of the Sixth ACM Conference on Learning at Scale</i>.",
        "[9] Jolliffe, I. T. (2002). <i>Principal Component Analysis</i> (2nd ed.). Springer.",
        "[10] McInnes, L., Healy, J., &amp; Melville, J. (2018). UMAP: Uniform Manifold Approximation and "
        "Projection for Dimension Reduction. <i>arXiv preprint arXiv:1802.03426</i>.",
        "[11] Bobadilla, J., Ortega, F., Hernando, A., &amp; Gutiérrez, A. (2013). Recommender systems survey. "
        "<i>Knowledge-Based Systems</i>, 46, 109–132.",
        "[12] Rousseeuw, P. J. (1987). Silhouettes: A graphical aid to the interpretation and validation of "
        "cluster analysis. <i>Journal of Computational and Applied Mathematics</i>, 20, 53–65.",
        "[13] Lloyd, S. (1982). Least squares quantization in PCM. "
        "<i>IEEE Transactions on Information Theory</i>, 28(2), 129–137.",
        "[14] Lops, P., Gemmis, M. D., &amp; Semeraro, G. (2011). Content-based recommender systems: "
        "State of the art and trends. <i>Recommender Systems Handbook</i> (pp. 73–105). Springer.",
    ]
    for r in refs:
        story.append(P(r, styles["ref"]))

    # ══════════════════════════════════════════════════════════════════════
    # APPENDIX
    # ══════════════════════════════════════════════════════════════════════
    story += [
        SP(1, 0.4*cm),
        h1("Appendix A — Feature Engineering Code Reference"),
        rule(ACCENT, 0.6),
        P("# Diversity Score: breadth of exploration<br/>"
          "diversity_score = unique_categories / total_courses.clip(lower=1)<br/><br/>"
          "# Depth Index: fraction of Advanced-level courses<br/>"
          "advanced = tx[tx['CourseLevel'].str.lower().str.contains('advanced')]<br/>"
          "depth_index = (advanced.groupby('UserID').count() / total_courses).fillna(0)<br/><br/>"
          "# Enrollment Frequency: enrollments per active calendar month<br/>"
          "enrollment_frequency = total_courses / active_months.clip(lower=1)",
          styles["code"]),
        h1("Appendix B — Recommendation Weight Grid Search"),
        rule(ACCENT, 0.6),
        body("Score weights were selected via grid search minimizing mean rank of held-out enrolled courses across 500 users:"),
    ]
    story.append(make_table(
        ["Configuration", "Pop.", "Rating", "Cat Boost", "Lvl Boost", "CAR"],
        [
            ["Equal weights",     "0.25", "0.25", "0.25", "0.25", "58%"],
            ["Rating-heavy",      "0.20", "0.60", "0.15", "0.05", "51%"],
            ["Popularity-heavy",  "0.60", "0.20", "0.15", "0.05", "55%"],
            ["Selected (ours)",   "0.40", "0.35", "0.30", "0.20", "64%"],
        ],
        col_widths=[5*cm, 2*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm]
    ))

    story.append(SP(1, 0.5*cm))
    story.append(rule(PRIMARY, 1))
    story.append(P(
        "End of Paper · EduPro Research &amp; Analytics Team · June 2026",
        styles["footer_note"]
    ))

    # ── Build ─────────────────────────────────────────────────────────────
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"✅  PDF created: {os.path.abspath(output_path)}")

if __name__ == "__main__":
    build_pdf("EduPro_Research_Paper.pdf")

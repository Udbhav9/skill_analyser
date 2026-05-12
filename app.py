import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Skill Gap Analytics Platform",
    page_icon="📊",
    layout="wide"
)

# =====================================================
# LOAD DATA
# =====================================================

comparison_df = pd.read_csv("skill_gap_analysis.csv")

skills_df = pd.read_csv("market_skills.csv")

# =====================================================
# CAREER PATH SKILLS
# =====================================================

career_paths = {

    "Data Analyst": [
        "python",
        "sql",
        "excel",
        "tableau",
        "power bi",
        "statistics",
        "pandas"
    ],

    "Data Scientist": [
        "python",
        "machine learning",
        "deep learning",
        "tensorflow",
        "statistics",
        "numpy",
        "pandas"
    ],

    "Business Analyst": [
        "excel",
        "sql",
        "power bi",
        "tableau",
        "data visualization",
        "statistics"
    ],

    "Data Engineer": [
        "python",
        "sql",
        "spark",
        "hadoop",
        "etl",
        "aws",
        "docker"
    ],

    "ML Engineer": [
        "python",
        "machine learning",
        "tensorflow",
        "docker",
        "kubernetes",
        "aws"
    ],

    "BI Analyst": [
        "sql",
        "tableau",
        "power bi",
        "excel",
        "data visualization"
    ]
}

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

.main {
    background-color: #0E1117;
    color: white;
}

.skill-box {
    padding: 12px;
    border-radius: 10px;
    margin-bottom: 8px;
    font-weight: bold;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# TITLE
# =====================================================

st.title("📊 Market Skill Gap Analytics Platform")

st.markdown("""
### Analyze your skills against real-world market demand
""")

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.header("👤 User Profile")

selected_role = st.sidebar.selectbox(
    "Choose Career Path",
    list(career_paths.keys())
)

user_input = st.sidebar.text_area(
    "Enter Your Skills",
    placeholder="python, sql, excel"
)

# =====================================================
# KPI SECTION
# =====================================================

top_skill = skills_df.iloc[0]['Skill']

top_count = int(skills_df.iloc[0]['Demand Count'])

total_skills = len(skills_df)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "📌 Total Skills",
        total_skills
    )

with col2:
    st.metric(
        "🔥 Top Market Skill",
        top_skill.upper()
    )

with col3:
    st.metric(
        "📈 Highest Demand",
        top_count
    )

st.divider()

# =====================================================
# TABS
# =====================================================

tab1, tab2, tab3 = st.tabs([
    "📈 Market Analysis",
    "🎯 Skill Gap Analysis",
    "📋 Dataset"
])

# =====================================================
# TAB 1 - MARKET ANALYSIS
# =====================================================

with tab1:

    st.subheader("🔥 Top 10 Most In-Demand Skills")

    top_skills = skills_df.head(10)

    fig = px.bar(
        top_skills,
        x='Skill',
        y='Demand Count',
        text='Demand Count',
        title='Top 10 Market Skills'
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("📌 Required Skills for Selected Career")

    role_skills = career_paths[selected_role]

    cols = st.columns(3)

    for index, skill in enumerate(role_skills):

        with cols[index % 3]:

            st.markdown(f"""
            <div class="skill-box"
            style="background-color:#1E3A5F;color:white;">
            {skill.upper()}
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    st.subheader("🌍 Market Insights")

    st.info(f"""
    Current market analysis indicates strong demand for
    {top_skill.upper()} along with cloud technologies,
    SQL-based analytics, and data visualization tools.
    """)

# =====================================================
# TAB 2 - SKILL GAP ANALYSIS
# =====================================================

with tab2:

    st.subheader(f"🎯 {selected_role} Career Readiness")

    required_skills = career_paths[selected_role]

    if user_input:

        user_skills = [
            skill.strip().lower()
            for skill in user_input.split(',')
        ]

        matched_skills = []

        missing_skills = []

        for skill in required_skills:

            if skill in user_skills:
                matched_skills.append(skill)

            else:
                missing_skills.append(skill)

        # =================================================
        # SCORE
        # =================================================

        match_score = (
            len(matched_skills)
            / len(required_skills)
        ) * 100

        st.subheader("📊 Career Readiness Score")

        st.progress(match_score / 100)

        st.success(
            f"Your readiness for {selected_role}: "
            f"{match_score:.1f}%"
        )

        # =================================================
        # METRICS
        # =================================================

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "✅ Skills Matched",
                len(matched_skills)
            )

        with c2:
            st.metric(
                "❌ Missing Skills",
                len(missing_skills)
            )

        with c3:
            st.metric(
                "🎯 Readiness",
                f"{match_score:.0f}%"
            )

        st.divider()

        # =================================================
        # PIE CHART
        # =================================================

        st.subheader("📌 Skill Match Distribution")

        pie_df = pd.DataFrame({
            'Category': ['Matched', 'Missing'],
            'Count': [
                len(matched_skills),
                len(missing_skills)
            ]
        })

        pie_fig = px.pie(
            pie_df,
            names='Category',
            values='Count',
            title='Matched vs Missing Skills'
        )

        st.plotly_chart(
            pie_fig,
            use_container_width=True
        )

        # =================================================
        # RADAR CHART
        # =================================================

        st.subheader("🕸 Career Skill Coverage")

        radar_df = pd.DataFrame({
            'Skill': required_skills,
            'Value': [
                1 if skill in user_skills else 0
                for skill in required_skills
            ]
        })

        radar_fig = px.line_polar(
            radar_df,
            r='Value',
            theta='Skill',
            line_close=True,
            title='Skill Coverage Radar'
        )

        st.plotly_chart(
            radar_fig,
            use_container_width=True
        )

        st.divider()

        # =================================================
        # MATCHED / MISSING SKILLS
        # =================================================

        colA, colB = st.columns(2)

        with colA:

            st.subheader("✅ Skills You Have")

            if matched_skills:

                for skill in matched_skills:

                    st.markdown(f"""
                    <div class="skill-box"
                    style="background-color:#163020;color:#7CFC00;">
                    {skill.upper()}
                    </div>
                    """, unsafe_allow_html=True)

            else:
                st.warning("No matching skills found.")

        with colB:

            st.subheader("🚀 Skills To Learn")

            for skill in missing_skills:

                st.markdown(f"""
                <div class="skill-box"
                style="background-color:#3B0D11;color:#FF7F7F;">
                {skill.upper()}
                </div>
                """, unsafe_allow_html=True)

        st.divider()

        # =================================================
        # HEATMAP
        # =================================================

        st.subheader("🔥 Market Skill Demand Heatmap")

        heatmap_df = comparison_df.head(15)

        heatmap_fig = px.density_heatmap(
            heatmap_df,
            x='Skill',
            y='Demand Count',
            title='Skill Demand Heatmap'
        )

        st.plotly_chart(
            heatmap_fig,
            use_container_width=True
        )

        # =================================================
        # AI RECOMMENDATIONS
        # =================================================

        st.subheader("🧠 AI Career Recommendations")

        if match_score >= 80:

            st.success(f"""
            Excellent alignment detected for {selected_role} roles.

            You are highly competitive for internships
            and entry-level opportunities.
            """)

        elif match_score >= 50:

            st.warning(f"""
            Moderate alignment detected.

            Learning the recommended skills can significantly
            improve your market competitiveness.
            """)

        else:

            st.error(f"""
            Low market alignment detected.

            Focus first on core technical skills such as:
            Python, SQL, visualization tools,
            and analytics fundamentals.
            """)

        # =================================================
        # GAP TABLE
        # =================================================

        st.subheader("📋 Skill Gap Dataset")

        filtered_df = comparison_df[
            comparison_df['Skill'].str.lower().isin(missing_skills)
        ]

        st.dataframe(filtered_df)

    else:

        st.info("Enter your skills in the sidebar to begin analysis.")

# =====================================================
# TAB 3 - DATASET
# =====================================================

with tab3:

    st.subheader("📋 Market Skills Dataset")

    st.dataframe(skills_df)

    st.subheader("📋 Skill Gap Dataset")

    st.dataframe(comparison_df)
import streamlit as st
from parser import parse_resume
from scorer import analyze_resume

st.set_page_config(page_title="AI Resume Assistant", page_icon="📄", layout="wide")

st.title("📄 AI Resume Assistant")
st.caption("Rubric-based evaluation grounded in Harvard College OCS standards.")

# API Key handling
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    api_key = st.sidebar.text_input("Enter Google Gemini API Key", type="password")

col_left, col_right = st.columns([1, 1], gap="medium")

with col_left:
    st.subheader("1. Upload Resume")
    uploaded_file = st.file_uploader("Upload PDF or DOCX", type=["pdf", "docx"])
    job_desc = st.text_area("2. Target Job Description (Optional)", height=160, placeholder="Paste job description here...")
    analyze_btn = st.button("Analyze Resume", type="primary", use_container_width=True)

if analyze_btn:
    if not uploaded_file:
        st.warning("Please upload a resume file first.")
    elif not api_key:
        st.error("Gemini API key is required to proceed.")
    else:
        with st.spinner("Extracting and evaluating against Harvard OCS rubric..."):
            try:
                raw_text, segmented = parse_resume(uploaded_file.getvalue(), uploaded_file.name)
                result = analyze_resume(api_key, raw_text, job_desc)
                st.session_state["analysis_result"] = result
                st.session_state["resume_text"] = raw_text
            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")

with col_right:
    st.subheader("Analysis & Recommendations")
    if "analysis_result" in st.session_state:
        res = st.session_state["analysis_result"]
        
        # Metric indicators
        metric_col1, metric_col2 = st.columns(2)
        metric_col1.metric("Overall Harvard Score", f"{res.overall_score}/100")
        metric_col2.metric("Quantified Metrics Ratio", res.quantified_impact_ratio)
        
        if res.missing_jd_keywords:
            st.warning(f"**Missing Keywords:** {', '.join(res.missing_jd_keywords)}")

        st.write("---")
        st.write("**Rubric Breakdown**")
        for sub in res.sub_scores:
            with st.expander(f"{sub.criterion_name} — {sub.score}/10"):
                st.write(sub.feedback)

        st.write("---")
        st.write("**Suggested Rewrites**")
        for i, s in enumerate(res.suggestions):
            with st.container(border=True):
                st.caption(f"Section: {s.section.title()}")
                st.markdown(f"**Original:** `{s.original_text}`")
                st.markdown(f"**Suggested:** {s.suggested_text}")
                st.info(f"Why: {s.improvement_reason}")
    else:
        st.info("Upload your resume and click **Analyze Resume** to see your score and recommendations.")

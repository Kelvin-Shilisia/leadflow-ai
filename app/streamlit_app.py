import streamlit as st

from backend.database import init_db


# Initialize database
init_db()


st.set_page_config(
    page_title="LeadFlow AI",
    page_icon="📊",
    layout="wide",
)


st.title("📊 LeadFlow AI")

st.subheader(
    "AI-Powered Lead Management & Sales Intelligence"
)


st.write(
    """
    Welcome to LeadFlow AI.

    This platform helps you capture, manage, follow up with,
    and analyze leads generated from your marketing campaigns.
    """
)


st.divider()


col1, col2, col3 = st.columns(3)


with col1:
    st.info(
        """
        ### 👥 Manage Leads

        Capture customer information and track every lead
        through the sales process.
        """
    )


with col2:
    st.info(
        """
        ### 📞 Follow Up

        Never forget customers who need to be contacted again.
        """
    )


with col3:
    st.info(
        """
        ### 📈 Analyze

        Understand which campaigns and channels generate
        the best customers.
        """
    )


st.success(
    "LeadFlow AI is running successfully."
)
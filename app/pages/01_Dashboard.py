import streamlit as st

from backend.crud import get_all_leads


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Dashboard | LeadFlow AI",
    page_icon="📊",
    layout="wide",
)


# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------

st.title("📊 LeadFlow AI Dashboard")

st.write(
    "Overview of your leads, sales pipeline, and follow-up activity."
)

st.divider()


# ---------------------------------------------------------
# GET LEADS
# ---------------------------------------------------------

try:
    leads = get_all_leads()

except Exception as error:
    st.error("Unable to load leads from the database.")
    st.exception(error)
    st.stop()


# ---------------------------------------------------------
# BASIC METRICS
# ---------------------------------------------------------

total_leads = len(leads)

new_leads = sum(
    1
    for lead in leads
    if lead["status"] == "New"
)

interested_leads = sum(
    1
    for lead in leads
    if lead["status"] == "Interested"
)

sold_leads = sum(
    1
    for lead in leads
    if lead["status"] == "Sold"
)

total_pipeline_value = sum(
    (lead["estimated_value"] or 0)
    for lead in leads
)


# ---------------------------------------------------------
# METRICS
# ---------------------------------------------------------

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Total Leads",
        total_leads,
    )

with col2:
    st.metric(
        "New",
        new_leads,
    )

with col3:
    st.metric(
        "Interested",
        interested_leads,
    )

with col4:
    st.metric(
        "Sold",
        sold_leads,
    )

with col5:
    st.metric(
        "Pipeline Value",
        f"KES {total_pipeline_value:,.0f}",
    )


st.divider()


# ---------------------------------------------------------
# RECENT LEADS
# ---------------------------------------------------------

if not leads:

    st.info(
        "Your dashboard will populate once you start adding leads."
    )

else:

    st.subheader("Recent Leads")

    for lead in leads[:5]:

        with st.container(border=True):

            col1, col2, col3 = st.columns(
                [3, 2, 2]
            )

            with col1:

                st.write(
                    f"**{lead['name']}**"
                )

                st.caption(
                    lead["phone"]
                )

            with col2:

                st.write(
                    f"**Status:** {lead['status']}"
                )

            with col3:

                value = lead["estimated_value"] or 0

                st.write(
                    f"**Value:** KES {value:,.0f}"
                )
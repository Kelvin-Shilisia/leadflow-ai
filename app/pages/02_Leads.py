import streamlit as st
import pandas as pd

from backend.database import init_db
from backend.crud import get_all_leads, delete_lead


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Leads | LeadFlow AI",
    page_icon="👥",
    layout="wide",
)


# ---------------------------------------------------------
# INITIALIZE DATABASE
# ---------------------------------------------------------

init_db()


# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------

st.title("👥 Leads")

st.write(
    "View and manage all leads stored in the LeadFlow AI database."
)

st.divider()


# ---------------------------------------------------------
# GET LEADS
# ---------------------------------------------------------

leads = get_all_leads()


if not leads:

    st.info(
        "No leads have been added yet. "
        "Go to **Add Lead** to create your first lead."
    )

    st.stop()


# ---------------------------------------------------------
# CONVERT TO DATAFRAME
# ---------------------------------------------------------

data = [dict(lead) for lead in leads]

df = pd.DataFrame(data)


# ---------------------------------------------------------
# METRICS
# ---------------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Leads",
        len(df),
    )

with col2:
    interested = len(
        df[df["status"] == "Interested"]
    )

    st.metric(
        "Interested",
        interested,
    )

with col3:
    sold = len(
        df[df["status"] == "Sold"]
    )

    st.metric(
        "Sold",
        sold,
    )

with col4:
    total_value = df["estimated_value"].fillna(0).sum()

    st.metric(
        "Pipeline Value",
        f"KES {total_value:,.0f}",
    )


st.divider()


# ---------------------------------------------------------
# SEARCH
# ---------------------------------------------------------

search = st.text_input(
    "🔎 Search Leads",
    placeholder="Search by name, phone, campaign, product or source...",
)


if search:

    search = search.lower()

    mask = (
        df["name"].fillna("").str.lower().str.contains(search)
        | df["phone"].fillna("").str.lower().str.contains(search)
        | df["campaign"].fillna("").str.lower().str.contains(search)
        | df["product_service"].fillna("").str.lower().str.contains(search)
        | df["source"].fillna("").str.lower().str.contains(search)
    )

    filtered_df = df[mask]

else:

    filtered_df = df


st.write(
    f"Showing **{len(filtered_df)}** lead(s)"
)


# ---------------------------------------------------------
# LEADS TABLE
# ---------------------------------------------------------

display_columns = [
    "id",
    "name",
    "phone",
    "source",
    "campaign",
    "status",
    "product_service",
    "estimated_value",
    "follow_up_date",
    "created_at",
]

available_columns = [
    column
    for column in display_columns
    if column in filtered_df.columns
]


display_df = filtered_df[available_columns].copy()


# Rename columns for the user interface

display_df = display_df.rename(
    columns={
        "id": "ID",
        "name": "Name",
        "phone": "Phone",
        "source": "Source",
        "campaign": "Campaign",
        "status": "Status",
        "product_service": "Product / Service",
        "estimated_value": "Estimated Value",
        "follow_up_date": "Follow-up",
        "created_at": "Created",
    }
)


st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
)


# ---------------------------------------------------------
# DOWNLOAD CSV
# ---------------------------------------------------------

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Leads as CSV",
    data=csv,
    file_name="leadflow_leads.csv",
    mime="text/csv",
)


st.divider()


# ---------------------------------------------------------
# DELETE LEAD
# ---------------------------------------------------------

st.subheader("🗑️ Delete Lead")

st.warning(
    "Deleting a lead is permanent. "
    "Make sure you select the correct lead."
)


lead_options = {
    f"#{row['id']} — {row['name']} — {row['phone']}": row["id"]
    for _, row in df.iterrows()
}


selected_lead_label = st.selectbox(
    "Select a lead to delete",
    options=list(lead_options.keys()),
)


selected_lead_id = lead_options[selected_lead_label]


confirm_delete = st.checkbox(
    "I understand that this lead will be permanently deleted."
)


if st.button(
    "🗑️ Delete Selected Lead",
    type="secondary",
    disabled=not confirm_delete,
):

    try:

        deleted = delete_lead(selected_lead_id)

        if deleted:

            st.success(
                f"Lead #{selected_lead_id} was deleted successfully."
            )

            st.rerun()

        else:

            st.error(
                "The lead could not be found."
            )

    except Exception as error:

        st.error(
            "An error occurred while deleting the lead."
        )

        st.exception(error)
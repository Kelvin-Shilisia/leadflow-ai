import streamlit as st
from datetime import date, time, datetime

from backend.crud import create_lead


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Add Lead | LeadFlow AI",
    page_icon="➕",
    layout="wide",
)


# ---------------------------------------------------------
# PAGE HEADER
# ---------------------------------------------------------

st.title("➕ Add New Lead")

st.markdown(
    """
    Add a new potential customer to your LeadFlow AI database.

    **Important:** Filling in this form does not save anything.
    The lead is only created when you click **Save Lead** at the bottom.
    """
)

st.divider()


# ---------------------------------------------------------
# CUSTOMER INFORMATION
# ---------------------------------------------------------

st.subheader("👤 Customer Information")

col1, col2 = st.columns(2)

with col1:

    name = st.text_input(
        "Customer Name *",
        placeholder="e.g. John Kamau",
    )

    phone = st.text_input(
        "Phone Number *",
        placeholder="e.g. +254712345678",
    )


with col2:

    email = st.text_input(
        "Email Address",
        placeholder="e.g. john@example.com",
    )

    source = st.selectbox(
        "Lead Source *",
        [
            "Facebook",
            "Instagram",
            "TikTok",
            "WhatsApp",
            "Google",
            "Website",
            "Referral",
            "LinkedIn",
            "Other",
        ],
    )


st.divider()


# ---------------------------------------------------------
# MARKETING INFORMATION
# ---------------------------------------------------------

st.subheader("📣 Campaign Information")

col1, col2 = st.columns(2)

with col1:

    campaign = st.text_input(
        "Campaign Name",
        placeholder="e.g. August CRM Campaign",
    )


with col2:

    status = st.selectbox(
        "Lead Status *",
        [
            "New",
            "Interested",
            "Qualified",
            "Call Back Later",
            "Not Interested",
            "Sold",
            "Lost",
        ],
    )


st.divider()


# ---------------------------------------------------------
# PRODUCT / SALES INFORMATION
# ---------------------------------------------------------

st.subheader("💰 Product & Sales Information")

col1, col2 = st.columns(2)

with col1:

    product_service = st.text_input(
        "Product / Service",
        placeholder="e.g. CRM Software",
    )


with col2:

    estimated_value = st.number_input(
        "Estimated Deal Value (KES)",
        min_value=0.0,
        value=0.0,
        step=1000.0,
        help=(
            "The estimated amount you expect to earn if this "
            "lead becomes a successful sale."
        ),
    )


st.divider()


# ---------------------------------------------------------
# FOLLOW-UP
# ---------------------------------------------------------

st.subheader("📅 Follow-Up")

schedule_follow_up = st.checkbox(
    "Schedule a follow-up",
    value=False,
    help="Enable this if you need to contact this customer again.",
)

next_follow_up = None
next_follow_up_datetime = None


if schedule_follow_up:

    st.info(
        "Choose when you want LeadFlow AI to remind you "
        "to contact this customer."
    )

    col1, col2 = st.columns(2)

    with col1:

        follow_up_date = st.date_input(
            "Follow-Up Date *",
            value=date.today(),
            min_value=date.today(),
        )

    with col2:

        follow_up_time = st.time_input(
            "Follow-Up Time *",
            value=time(9, 0),
        )

    # Combine date and time
    next_follow_up_datetime = datetime.combine(
        follow_up_date,
        follow_up_time,
    )

    # Store as a single database value
    next_follow_up = next_follow_up_datetime.strftime(
        "%Y-%m-%d %H:%M:%S"
    )


st.divider()


# ---------------------------------------------------------
# NOTES
# ---------------------------------------------------------

st.subheader("📝 Notes")

notes = st.text_area(
    "Lead Notes",
    placeholder=(
        "Example: Customer is interested in the premium package "
        "and requested a call next week."
    ),
    height=150,
)


st.divider()


# ---------------------------------------------------------
# SAVE LEAD
# ---------------------------------------------------------

st.subheader("💾 Save Lead")


if not name.strip():

    st.caption(
        "⚠️ Customer name is required."
    )


if not phone.strip():

    st.caption(
        "⚠️ Phone number is required."
    )


save_clicked = st.button(
    "💾 Save Lead",
    type="primary",
    use_container_width=True,
)


# ---------------------------------------------------------
# SAVE PROCESS
# ---------------------------------------------------------

if save_clicked:

    # -----------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------

    if not name.strip():

        st.error(
            "Please enter the customer's name before saving."
        )

        st.stop()


    if not phone.strip():

        st.error(
            "Please enter the customer's phone number before saving."
        )

        st.stop()


    # -----------------------------------------------------
    # DATABASE SAVE
    # -----------------------------------------------------

    try:

        lead_id = create_lead(
            name=name.strip(),
            phone=phone.strip(),
            email=email.strip() or None,
            source=source,
            campaign=campaign.strip() or None,
            status=status,
            product_service=product_service.strip() or None,
            estimated_value=estimated_value,
            next_follow_up=next_follow_up,
            notes=notes.strip() or None,
        )


        # -------------------------------------------------
        # SUCCESS MESSAGE
        # -------------------------------------------------

        st.success(
            f"✅ Lead saved successfully! Lead ID: {lead_id}"
        )

        st.balloons()


        # -------------------------------------------------
        # FOLLOW-UP MESSAGE
        # -------------------------------------------------

        if next_follow_up_datetime:

            formatted_follow_up = (
                next_follow_up_datetime.strftime(
                    "%A, %d %B %Y at %I:%M %p"
                )
            )

            st.info(
                f"📅 Follow-up scheduled for "
                f"**{formatted_follow_up}**."
            )

        else:

            st.info(
                "No follow-up has been scheduled for this lead."
            )


    except Exception as error:

        st.error(
            "Something went wrong while saving the lead."
        )

        st.exception(error)
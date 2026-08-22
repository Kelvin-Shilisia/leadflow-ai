from datetime import datetime

from backend.database import get_connection


# ---------------------------------------------------------
# CREATE LEAD
# ---------------------------------------------------------

def create_lead(
    name,
    phone,
    email,
    source,
    campaign,
    status,
    product_service,
    estimated_value,
    next_follow_up=None,
    notes=None,
):
    """
    Create a new lead in the database.

    created_at and updated_at are explicitly supplied rather
    than relying on SQLite table defaults.

    This is important because existing databases may have
    created_at defined as NOT NULL without a usable default.
    """

    connection = get_connection()
    cursor = connection.cursor()

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        cursor.execute(
            """
            INSERT INTO leads (
                name,
                phone,
                email,
                source,
                campaign,
                status,
                product_service,
                estimated_value,
                next_follow_up,
                notes,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                name,
                phone,
                email,
                source,
                campaign,
                status,
                product_service,
                estimated_value,
                next_follow_up,
                notes,
                now,
                now,
            ),
        )

        lead_id = cursor.lastrowid

        connection.commit()

        return lead_id

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


# ---------------------------------------------------------
# GET ALL LEADS
# ---------------------------------------------------------

def get_all_leads():
    """
    Return all leads ordered by newest first.
    """

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT *
            FROM leads
            ORDER BY id DESC
            """
        )

        leads = cursor.fetchall()

        return leads

    finally:
        connection.close()


# ---------------------------------------------------------
# GET SINGLE LEAD
# ---------------------------------------------------------

def get_lead_by_id(lead_id):
    """
    Get one lead by ID.
    """

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT *
            FROM leads
            WHERE id = ?
            """,
            (lead_id,),
        )

        lead = cursor.fetchone()

        return lead

    finally:
        connection.close()


# ---------------------------------------------------------
# UPDATE LEAD
# ---------------------------------------------------------

def update_lead(
    lead_id,
    name,
    phone,
    email,
    source,
    campaign,
    status,
    product_service,
    estimated_value,
    next_follow_up=None,
    notes=None,
):
    """
    Update an existing lead.
    """

    connection = get_connection()
    cursor = connection.cursor()

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        cursor.execute(
            """
            UPDATE leads
            SET
                name = ?,
                phone = ?,
                email = ?,
                source = ?,
                campaign = ?,
                status = ?,
                product_service = ?,
                estimated_value = ?,
                next_follow_up = ?,
                notes = ?,
                updated_at = ?
            WHERE id = ?
            """,
            (
                name,
                phone,
                email,
                source,
                campaign,
                status,
                product_service,
                estimated_value,
                next_follow_up,
                notes,
                now,
                lead_id,
            ),
        )

        connection.commit()

        return cursor.rowcount > 0

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


# ---------------------------------------------------------
# DELETE LEAD
# ---------------------------------------------------------

def delete_lead(lead_id):
    """
    Permanently delete a lead.

    Returns:
        True  -> lead was deleted
        False -> lead did not exist
    """

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            DELETE FROM leads
            WHERE id = ?
            """,
            (lead_id,),
        )

        deleted = cursor.rowcount > 0

        connection.commit()

        return deleted

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()
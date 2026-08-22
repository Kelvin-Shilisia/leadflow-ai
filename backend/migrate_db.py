from backend.database import get_connection, init_db


def migrate_database():
    """
    Safely update the existing LeadFlow AI database.

    Existing lead data is preserved.
    Missing columns are added automatically.
    """

    # Make sure the database/table exists
    init_db()

    connection = get_connection()
    cursor = connection.cursor()

    # Get existing columns
    cursor.execute("PRAGMA table_info(leads)")
    existing_columns = {
        row["name"]
        for row in cursor.fetchall()
    }

    # Columns required by the current version of LeadFlow AI
    required_columns = {
        "email": "TEXT",
        "follow_up_date": "TEXT",
        "follow_up_time": "TEXT",
        "notes": "TEXT",
        "updated_at": "TEXT",
    }

    added_columns = []

    for column_name, column_type in required_columns.items():

        if column_name not in existing_columns:

            cursor.execute(
                f"""
                ALTER TABLE leads
                ADD COLUMN {column_name} {column_type}
                """
            )

            added_columns.append(column_name)

    # Existing records may have NULL updated_at values.
    cursor.execute(
        """
        UPDATE leads
        SET updated_at = COALESCE(
            updated_at,
            created_at,
            CURRENT_TIMESTAMP
        )
        """
    )

    connection.commit()
    connection.close()

    print("========================================")
    print("LeadFlow AI Database Migration")
    print("========================================")

    if added_columns:

        print("Added columns:")

        for column in added_columns:
            print(f"  ✓ {column}")

    else:

        print("✓ Database already has all required columns.")

    print()
    print("✓ Existing lead data has been preserved.")
    print("✓ Database migration completed successfully.")


if __name__ == "__main__":
    migrate_database()
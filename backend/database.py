from pathlib import Path
import sqlite3


# =========================================================
# PROJECT PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

DATA_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

DATABASE_PATH = DATA_DIR / "leadflow.db"


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():
    """
    Create and return a SQLite database connection.

    sqlite3.Row allows us to access database values using
    column names:

        lead["name"]
        lead["status"]

    instead of numeric indexes.
    """

    connection = sqlite3.connect(
        DATABASE_PATH,
        timeout=30,
    )

    connection.row_factory = sqlite3.Row

    # Enable foreign keys for future relational tables.
    connection.execute(
        "PRAGMA foreign_keys = ON"
    )

    return connection


# =========================================================
# DATABASE INITIALIZATION
# =========================================================

def init_db():
    """
    Initialize the LeadFlow AI database.

    This function is intentionally safe for an existing
    database.

    It creates missing tables but does NOT delete existing
    leads.
    """

    connection = get_connection()

    try:

        cursor = connection.cursor()

        # -------------------------------------------------
        # LEADS TABLE
        # -------------------------------------------------

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS leads (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                name TEXT NOT NULL,

                phone TEXT NOT NULL,

                email TEXT,

                source TEXT NOT NULL,

                campaign TEXT,

                status TEXT NOT NULL DEFAULT 'New',

                product_service TEXT,

                estimated_value REAL DEFAULT 0,

                next_follow_up TEXT,

                notes TEXT,

                created_at TEXT NOT NULL
                    DEFAULT CURRENT_TIMESTAMP,

                updated_at TEXT NOT NULL
                    DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        # -------------------------------------------------
        # ACTIVITIES TABLE
        # -------------------------------------------------

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS activities (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                lead_id INTEGER NOT NULL,

                activity_type TEXT NOT NULL,

                notes TEXT,

                created_at TEXT NOT NULL
                    DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (lead_id)
                    REFERENCES leads(id)
                    ON DELETE CASCADE
            )
            """
        )

        connection.commit()

    finally:

        connection.close()


# =========================================================
# DIRECT EXECUTION
# =========================================================

if __name__ == "__main__":

    init_db()

    print("========================================")
    print("LeadFlow AI Database")
    print("========================================")
    print()
    print("Database initialized successfully.")
    print()
    print(f"Database location:")
    print(DATABASE_PATH)
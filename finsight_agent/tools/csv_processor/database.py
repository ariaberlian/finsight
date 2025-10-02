"""Database connection and initialization utilities."""

from typing import Optional, Dict, Any
import psycopg2
from psycopg2.extensions import connection as Connection

from settings import get_settings


def get_db_connection(connection_string: str = None) -> Connection:
    """
    Establish a connection to PostgreSQL database.

    Args:
        connection_string: PostgreSQL connection string in the format:
                          "postgresql://user:password@host:port/database"
                          If not provided, reads from settings configuration.

    Returns:
        psycopg2 connection object

    Raises:
        psycopg2.Error: If database connection fails
    """
    if connection_string is None:
        settings = get_settings()
        connection_string = settings.DATABASE_URL

    return psycopg2.connect(connection_string)


def initialize_expenses_table(connection_string: str = None) -> Dict[str, Any]:
    """
    Create the expenses table in PostgreSQL if it doesn't exist.

    This function creates the necessary table schema with appropriate
    column types and constraints. The embedding column uses PostgreSQL array
    type to store vector embeddings. Also creates indexes for optimized queries.

    Args:
        connection_string: PostgreSQL connection string. If not provided,
                          reads from settings configuration.

    Returns:
        Dict containing:
            - success (bool): Whether table creation succeeded
            - message (str): Status message
            - errors (List[str], optional): List of errors if any occurred

    Example:
        >>> result = initialize_expenses_table()
        >>> print(result)
        {'success': True, 'message': 'Expenses table created successfully'}
    """
    conn = None
    cursor = None

    try:
        conn = get_db_connection(connection_string)
        cursor = conn.cursor()

        # Enable pgvector extension
        cursor.execute("CREATE EXTENSION IF NOT EXISTS vector")

        # Create expenses table
        create_table_query = """
            CREATE TABLE IF NOT EXISTS expenses (
                id SERIAL PRIMARY KEY,
                date TIMESTAMP NOT NULL,
                category VARCHAR(100) NOT NULL,
                description TEXT NOT NULL,
                amount NUMERIC(12, 2) NOT NULL CHECK (amount > 0),
                payment_method VARCHAR(50) NOT NULL,
                vendor VARCHAR(200) NOT NULL,
                embedding vector(768),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        cursor.execute(create_table_query)

        # Create index on date for faster queries
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_expenses_date
            ON expenses(date DESC)
        """)

        # Create index on category
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_expenses_category
            ON expenses(category)
        """)

        # Create vector index for similarity search (HNSW algorithm)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_expenses_embedding
            ON expenses USING hnsw (embedding vector_cosine_ops)
        """)

        conn.commit()

        return {
            "success": True,
            "message": "Expenses table created successfully"
        }

    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        return {
            "success": False,
            "message": "Failed to create expenses table",
            "errors": [f"Database error: {str(e)}"]
        }

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

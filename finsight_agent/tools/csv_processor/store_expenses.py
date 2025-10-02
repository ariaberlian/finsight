"""Tool for storing expense data to PostgreSQL database."""

from typing import List, Dict, Any
import psycopg2
from psycopg2.extras import execute_batch

from schema import Expense
from .database import get_db_connection


def store_expenses_to_db(
    expenses: List[Expense],
    connection_string: str = None
) -> Dict[str, Any]:
    """
    Store expense records to PostgreSQL database.

    This function inserts expense records into the expenses table in PostgreSQL.
    It supports both single and bulk insert operations for efficient data storage.
    The function uses batch insertion for optimal performance with large datasets.

    Args:
        expenses: List of Expense objects to store in the database. Each expense
                 must contain: date, category, description, amount, payment_method,
                 vendor, and optionally an embedding vector.
        connection_string: PostgreSQL connection string in the format:
                          "postgresql://user:password@host:port/database"
                          If not provided, reads from DATABASE_URL environment variable.

    Returns:
        Dict containing:
            - success (bool): Whether the operation succeeded
            - rows_inserted (int): Number of rows successfully inserted
            - message (str): Status message
            - errors (List[str], optional): List of errors if any occurred

    Raises:
        ValueError: If expenses list is empty
        psycopg2.Error: If database connection or insertion fails

    Example:
        >>> from schema import Expense
        >>> from datetime import datetime
        >>>
        >>> expenses = [
        ...     Expense(
        ...         date=datetime(2025, 10, 2, 10, 30),
        ...         category="food",
        ...         description="Lunch",
        ...         amount=25.50,
        ...         payment_method="credit card",
        ...         vendor="Restaurant ABC"
        ...     )
        ... ]
        >>> result = store_expenses_to_db(expenses)
        >>> print(result)
        {'success': True, 'rows_inserted': 1, 'message': 'Successfully inserted 1 expense(s)'}
    """
    # Validation
    if not expenses:
        raise ValueError("Expenses list cannot be empty")

    conn = None
    cursor = None
    errors = []

    try:
        # Connect to PostgreSQL
        conn = get_db_connection(connection_string)
        cursor = conn.cursor()

        # Prepare insert query
        insert_query = """
            INSERT INTO expenses (
                date, category, description, amount,
                payment_method, vendor, embedding
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s
            )
        """

        # Prepare data for batch insertion
        expense_data = [
            (
                expense.date,
                expense.category,
                expense.description,
                expense.amount,
                expense.payment_method,
                expense.vendor,
                expense.embedding
            )
            for expense in expenses
        ]

        # Execute batch insert
        execute_batch(cursor, insert_query, expense_data)

        # Commit transaction
        conn.commit()

        rows_inserted = len(expense_data)

        return {
            "success": True,
            "rows_inserted": rows_inserted,
            "message": f"Successfully inserted {rows_inserted} expense(s)"
        }

    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        error_msg = f"Database error: {str(e)}"
        errors.append(error_msg)

        return {
            "success": False,
            "rows_inserted": 0,
            "message": "Failed to insert expenses",
            "errors": errors
        }

    except Exception as e:
        if conn:
            conn.rollback()
        error_msg = f"Unexpected error: {str(e)}"
        errors.append(error_msg)

        return {
            "success": False,
            "rows_inserted": 0,
            "message": "Failed to insert expenses",
            "errors": errors
        }

    finally:
        # Clean up resources
        if cursor:
            cursor.close()
        if conn:
            conn.close()



# notebook_error_logger/logger.py
import sqlite3
import traceback
from datetime import datetime

try:
    from IPython.core.interactiveshell import InteractiveShell
except ImportError:
    InteractiveShell = None


class ErrorLogger:
    def __init__(self, project_name: str, db_path: str = "error_logs.db"):
        """
        Initialize the error logger.

        Args:
            project_name (str): Name of the session (manual).
            db_path (str): SQLite database file path.
        """
        self.project_name = project_name
        self.db_path = db_path
        self._setup_db()
        self._install_hook()

    def _setup_db(self):
        """Create the errors table if it doesn’t exist, and drop previous table if it does exist."""
        self.conn = sqlite3.connect(self.db_path)
        c = self.conn.cursor()

        # Drop the table if it already exists
        c.execute("DROP TABLE IF EXISTS errors")

        # Create a new table with the desired schema
        c.execute('''
            CREATE TABLE IF NOT EXISTS errors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_type TEXT,
                project_name TEXT,
                error_type TEXT,
                date TEXT
            )
        ''')
        self.conn.commit()

    def _install_hook(self):
        """Attach a custom IPython exception handler."""
        if InteractiveShell is not None:
            shell = InteractiveShell.instance()

            def custom_exc(shell, exc_type, exc_value, exc_tb, tb_offset=None):
                tb_str = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
                self.log_error(exc_type.__name__, tb_str)
                # Display error normally in notebook
                shell.showtraceback((exc_type, exc_value, exc_tb), tb_offset=tb_offset)

            shell.set_custom_exc((Exception,), custom_exc)

    def log_error(self, error_type: str, tb: str):
        """Insert a new error record into the database where project_type will default to "data science notebook"."""
        c = self.conn.cursor()
        c.execute('''
            INSERT INTO errors (project_type, project_name, error_type, date)
            VALUES (?, ?, ?, ?)
        ''', ("data science notebook", self.project_name, error_type, datetime.utcnow().date().isoformat()))
        self.conn.commit()


def start_logger(project_name: str, db_path: str = "error_logs.db"):
    """
    Start error logging for the current session.
    """
    return ErrorLogger(project_name, db_path)

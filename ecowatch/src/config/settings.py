# src/config/settings.py
from pathlib import Path
import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

class Settings:
    """
    Configuration settings for Ecowatch application, loaded from environment variables.
    """
    # Project root directory
    PROJECT_ROOT = Path(__file__).resolve().parents[2]

    # Path to the CSV log file (can be overridden in .env)
    LOG_CSV_PATH = Path(
        os.getenv(
            'LOG_CSV_PATH',
            str(PROJECT_ROOT / 'data' / 'logs_ambientales_ecowatch.csv')
        )
    )

    # Delay between records in seconds (None or 0 for no delay)
    _stream_delay = os.getenv('STREAM_DELAY_SEC', '')
    STREAM_DELAY_SEC = None if _stream_delay in ('', 'None') else float(_stream_delay)

    # Default reference time for interactive menu (ISO format)
    DEFAULT_REF_TIME = os.getenv('DEFAULT_REF_TIME', '2025-05-01T08:05:00')

    # Default time window in minutes
    DEFAULT_WINDOW_MIN = int(os.getenv('DEFAULT_WINDOW_MIN', '5'))

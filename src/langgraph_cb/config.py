from dotenv import load_dotenv


def load_env() -> None:
    """Load environment variables from a .env file if present."""
    load_dotenv()

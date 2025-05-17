from datetime import datetime

def get_current_date():
    """
    get current date

    Returns:
        str: current date
    """
    return datetime.now().strftime("%Y-%m-%d")
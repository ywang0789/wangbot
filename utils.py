import random
import time

from datetime import datetime

def get_unique_str() -> str:
    """Returns a unique string from current datetime."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    return f"{timestamp}"

if __name__ == "__main__":
    print(str(int(time.time())))
    print(get_unique_str())

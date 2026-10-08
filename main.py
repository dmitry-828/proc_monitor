from db import init_db
from monitor import monitor_loop


if __name__ == "__main__":
    init_db()
    monitor_loop()

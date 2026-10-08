DB_NAME = "antivirus.db"
LOG_NAME = "events.log"

ALERT_THRESHOLD = 30
BLOCK_THRESHOLD = 60

WEIGHT_BAD_PATH = 30
WEIGHTS = {
    "bad_path": WEIGHT_BAD_PATH
}

BAD_DIRS = (
    "\\temp\\",
    "\\appdata\\roaming\\",
    "\\windows\\temp\\",
)

MODE = "notify"

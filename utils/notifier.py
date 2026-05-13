import os
import json
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")


# =========================
# CORE NOTIFIER
# =========================
def send_slack_notification(message: str) -> bool:
    """
    Send a Slack message safely.
    Returns True if successful, False otherwise.
    """

    if not SLACK_WEBHOOK_URL:
        print("❌ Slack webhook not configured")
        return False

    payload = {
        "username": "ETL Bot",
        "icon_emoji": ":rocket:",
        "text": message
    }

    try:
        response = requests.post(
            SLACK_WEBHOOK_URL,
            data=json.dumps(payload),
            headers={"Content-Type": "application/json"},
            timeout=5
        )

        response.raise_for_status()
        print("✅ Slack notification sent")
        return True

    except requests.exceptions.Timeout:
        print("❌ Slack timeout error")
        return False

    except requests.exceptions.RequestException as e:
        print(f"❌ Slack request error: {e}")
        return False

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


# =========================
# SUCCESS NOTIFICATION
# =========================
def send_etl_success(job_id: str, file_path: str, data: int):
    message = f"""
🚀 ETL SUCCESS

🆔 Job ID: {job_id}
📁 File: {file_path}
✅  Data to  load :{data}  
⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    return send_slack_notification(message)


# =========================
# FAILURE NOTIFICATION
# =========================
def send_etl_failure(job_id: str, error: str):
    message = f"""
🚨 ETL FAILED

🆔 Job ID: {job_id}
❌ Error: {error}
⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    return send_slack_notification(message)


# =========================
# TEST RUN
# =========================
if __name__ == "__main__":
    send_slack_notification("🚀 ETL system is running")

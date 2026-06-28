import requests
from datetime import datetime
from config import SLACK_WEBHOOK_URL

def send_slack_message(message: str, color: str = "good"):
    """Send a message to Slack."""
    payload = {
        "attachments": [
            {
                "color": color,
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": message
                        }
                    },
                    {
                        "type": "context",
                        "elements": [
                            {
                                "type": "mrkdwn",
                                "text": f"🕐 {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC | Energy Timeseries Platform"
                            }
                        ]
                    }
                ]
            }
        ]
    }
    response = requests.post(SLACK_WEBHOOK_URL, json=payload)
    return response.status_code == 200

def alert_pipeline_start(filters_count: int, start_date: str):
    send_slack_message(
        f"🚀 *Energy Pipeline Started*\n"
        f"• Filters: {filters_count}\n"
        f"• From: {start_date}",
        color="#36a64f"
    )

def alert_pipeline_success(rows: int, duration_seconds: float):
    send_slack_message(
        f"✅ *Energy Pipeline Completed Successfully*\n"
        f"• Rows loaded: {rows:,}\n"
        f"• Duration: {duration_seconds:.1f}s",
        color="#36a64f"
    )

def alert_pipeline_failure(error: str, filter_name: str = None):
    location = f" at filter: {filter_name}" if filter_name else ""
    send_slack_message(
        f"🔴 *Energy Pipeline Failed{location}*\n"
        f"• Error: {error[:200]}",
        color="danger"
    )

def alert_quality_warning(filter_name: str, issue: str, rows: int):
    send_slack_message(
        f"⚠️ *Data Quality Warning*\n"
        f"• Filter: {filter_name}\n"
        f"• Issue: {issue}\n"
        f"• Affected rows: {rows:,}",
        color="warning"
    )

import requests
import json
import os


def create_message(event):
    login_data = json.loads(event["Records"][0]["Sns"]["Message"])

    event_time = login_data["time"]
    event_name = login_data["detail"]["eventName"]
    event_source = login_data["detail"]["eventSource"]
    login_region = login_data["detail"]["awsRegion"]
    login_name = login_data["detail"]["userIdentity"]["userName"]
    login_source_ip = login_data["detail"]["sourceIPAddress"]
    login_response = login_data["detail"]["responseElements"]

    payload = {
        "username": "AWS Console Login Notify",
        "icon_emoji": ":paw_prints:",
        "text": "AWSへのログインを検知しました",
        "attachments": [
            {
                "fallback": "Detailed information on CloudTrail.",
                "color": "warning",
                "title": "イベント({})を検知しました".format(event_name),
                "text": "イベントの情報は以下の通りです。予期しないものであれば至急対応してください",
                "fields": [
                    {"title": "アカウント", "value": login_name, "short": True},
                    {"title": "リージョン", "value": login_region, "short": True},
                    {"title": "アクセス元", "value": login_source_ip, "short": False},
                    {"title": "イベント発生時刻", "value": event_time, "short": False},
                    {"title": "イベント発生元", "value": event_source, "short": False},
                    {
                        "title": "イベント結果",
                        "value": "{}".format(login_response),
                        "short": False,
                    },
                ],
            }
        ],
    }

    return payload


def lambda_handler(event, context):
    requests.post(
        url=os.getenv("SLACK_WEBHOOK_URL", None),
        data=json.dumps(create_message(event))
    )

    return {"statusCode": 200, "body": json.dumps("Successfly ended.")}

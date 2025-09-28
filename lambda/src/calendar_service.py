import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List

from google.oauth2 import service_account
from googleapiclient.discovery import build
from src.config.calendar_mapping import get_calendar_config


class CalendarService:
    """
    年別のGoogleマイカレンダーとの連携を管理するクラス
    """

    def __init__(self):
        self._service = self._create_calendar_service()

    def _create_calendar_service(self):
        """
        Google Calendar APIサービスを作成
        """
        try:
            # 環境変数から認証情報を取得
            credentials = service_account.Credentials.from_service_account_info(
                {
                    "type": "service_account",
                    "project_id": os.environ.get("GOOGLE_PROJECT_ID"),
                    "private_key_id": os.environ.get("GOOGLE_PRIVATE_KEY_ID"),
                    "private_key": os.environ.get("GOOGLE_PRIVATE_KEY").replace("\\n", "\n"),
                    "client_email": os.environ.get("GOOGLE_SERVICE_ACCOUNT_EMAIL"),
                    "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "client_x509_cert_url": os.environ.get("GOOGLE_CLIENT_CERT_URL"),
                },
                scopes=["https://www.googleapis.com/auth/calendar.readonly"],
            )

            return build("calendar", "v3", credentials=credentials)

        except Exception as e:
            print(f"Failed to create calendar service: {str(e)}")
            raise

    def get_races_by_date(self, year: int, month: int, day: int) -> List[Dict[str, Any]]:
        """
        指定日の重量レースを取得

        Args:
            year: 年
            month: 月
            day: 日

        Returns:
            重賞レースのリスト
        """
        try:
            # 年別カレンダー設定を取得
            config = get_calendar_config(year)
            if not config:
                raise ValueError(f"Calendar config not found for year {year}")

            calendar_id = config["calendar_id"]

            # JST タイムゾーンを定義（UTC+9）
            jst = timezone(timedelta(hours=9))

            # 指定日の開始と終了（JST）
            start_date = datetime(year, month, day, 0, 0, 0, tzinfo=jst).isoformat()
            end_date = datetime(year, month, day, 23, 59, 59, tzinfo=jst).isoformat()

            response = (
                self._service.events()
                .list(
                    calendarId=calendar_id,
                    timeMin=start_date,
                    timeMax=end_date,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )

            races = response.get("items", [])

            # イベントデータを整形
            formatted_events = list(
                map(
                    lambda event: {
                        "id": event["id"],
                        "summary": event.get("summary", "No Title"),
                        "description": event.get("description", ""),
                        "start": event["start"].get("dateTime", event["start"].get("date")),
                        "end": event["end"].get("dateTime", event["end"].get("date")),
                        "location": event.get("location", ""),
                        "year": year,
                        "month": month,
                        "day": day,
                        "calendar_id": calendar_id,
                    },
                    races,
                )
            )

            return formatted_events

        except Exception as e:
            print(f"Failed to get races for date {year}-{month:02d}-{day:02d}: {str(e)}")
            raise

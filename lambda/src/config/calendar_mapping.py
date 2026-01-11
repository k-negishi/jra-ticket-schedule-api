"""
カレンダーID設定（環境変数から取得）
"""

import os


def get_calendar_id() -> str:
    """
    カレンダーIDを環境変数から取得

    Returns:
        カレンダーID

    Raises:
        ValueError: CALENDAR_IDが設定されていない場合
    """
    calendar_id = os.environ.get("CALENDAR_ID")
    if not calendar_id:
        raise ValueError("CALENDAR_ID environment variable is not set")
    return calendar_id

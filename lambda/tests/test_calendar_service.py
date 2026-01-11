import os

import pytest
from dotenv import load_dotenv
from src.calendar_service import CalendarService
from src.config.calendar_mapping import get_calendar_id

load_dotenv()


class TestCalendarService:
    def test_calendar_service_initialization(self):
        """カレンダーサービスの初期化テスト"""
        # Google API認証情報が設定されている場合のみテスト
        if os.environ.get("GOOGLE_PRIVATE_KEY"):
            service = CalendarService()
            assert service is not None
            assert service._service is not None
        else:
            pytest.skip("Google API認証情報が設定されていません")

    def test_get_events_by_date(self):
        """指定日のイベント取得テスト"""
        # Google API認証情報が設定されている場合のみテスト
        if os.environ.get("GOOGLE_PRIVATE_KEY"):
            service = CalendarService()

            # テスト用の日付（実際のカレンダーにイベントがある日付を指定）
            year = 2025
            month = 6
            day = 1

            events = service.get_races_by_date(year, month, day)
            print(events)

            # イベントがリスト形式で返されることを確認
            assert isinstance(events, list)

            # イベントがある場合のテスト
            if events:
                event = events[0]
                assert "id" in event
                assert "summary" in event
                assert "start" in event
                assert "end" in event
                assert event["year"] == year
                assert event["month"] == month
                assert event["day"] == day
        else:
            pytest.skip("Google API認証情報が設定されていません")

    def test_get_events_by_date_no_events(self):
        """イベントが存在しない日のテスト"""
        # Google API認証情報が設定されている場合のみテスト
        if os.environ.get("GOOGLE_PRIVATE_KEY"):
            service = CalendarService()

            # イベントが存在しない可能性が高い日付
            year = 2025
            month = 1
            day = 1

            events = service.get_races_by_date(year, month, day)

            # 空のリストが返されることを確認
            assert isinstance(events, list)
            assert len(events) == 0
        else:
            pytest.skip("Google API認証情報が設定されていません")


class TestCalendarMapping:
    def test_get_calendar_id(self):
        """カレンダーID取得テスト"""
        # 環境変数から設定を取得
        calendar_id = get_calendar_id()

        # カレンダーIDが文字列で返されることを確認
        assert isinstance(calendar_id, str)
        assert len(calendar_id) > 0
        # Google Calendar形式のカレンダーIDを確認
        assert "@group.calendar.google.com" in calendar_id

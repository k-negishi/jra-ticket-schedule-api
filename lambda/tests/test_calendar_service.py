import os

import pytest
from dotenv import load_dotenv
from src.calendar_service import CalendarService
from src.config.calendar_mapping import get_available_years, get_calendar_config

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
    def test_get_calendar_config(self):
        """カレンダー設定取得テスト"""
        # 環境変数から設定を取得
        config = get_calendar_config(2024)

        if config:
            assert "calendar_id" in config
            assert "url" in config
            assert isinstance(config["calendar_id"], str)
            assert isinstance(config["url"], str)
        else:
            # 設定が存在しない場合はNoneが返されることを確認
            assert config is None

    def test_get_available_years(self):
        """利用可能な年のリスト取得テスト"""
        years = get_available_years()

        # リスト形式で返されることを確認
        assert isinstance(years, list)

        # 年が整数で返されることを確認
        for year in years:
            assert isinstance(year, int)
            assert year > 2000  # 妥当な年範囲

    def test_get_calendar_config_invalid_year(self):
        """存在しない年のカレンダー設定取得テスト"""
        config = get_calendar_config(1900)  # 存在しない年
        assert config is None

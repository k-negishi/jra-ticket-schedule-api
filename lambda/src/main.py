import json
import re
from datetime import datetime
from src.calendar_service import CalendarService
from src.utils.response import create_response, create_error_response

def lambda_handler(event, context):
    """
    AWS Lambda関数のメインハンドラー（Function URL用）
    """
    try:
        # Function URLのイベント構造を解析
        http_method = event.get('requestContext', {}).get('http', {}).get('method', 'GET')
        path = event.get('rawPath', '/')
        query_string = event.get('rawQueryString', '')

        # クエリパラメータを解析
        query_params = {}
        if query_string:
            for param in query_string.split('&'):
                if '=' in param:
                    key, value = param.split('=', 1)
                    query_params[key] = value

        calendar_service = CalendarService()

        # 指定日のイベント取得
        if path == '/jra-calendar/events' and http_method == 'GET':
            # 必須パラメータの検証
            year = query_params.get('year')
            month = query_params.get('month')
            day = query_params.get('day')

            if not year or not month or not day:
                return create_error_response(400, 'year, month, and day are required parameters')

            try:
                year = int(year)
                month = int(month)
                day = int(day)
            except ValueError:
                return create_error_response(400, 'year, month, and day must be valid integers')

            # 日付の妥当性チェック
            try:
                datetime(year, month, day)
            except ValueError:
                return create_error_response(400, 'Invalid date')

            #
            races = calendar_service.get_races_by_date(year, month, day)

            # イベントをグレード順に並べ替えて整形
            formatted_races = _format_and_sort_races(races)

            return create_response(200, {
                'events': formatted_races,
                'date': f"{year:04d}-{month:02d}-{day:02d}",
                'count': len(races)
            })

        else:
            return create_error_response(404, 'Endpoint not found')

    except Exception as e:
        print(f"Error: {str(e)}")
        return create_error_response(500, f"Internal server error: {str(e)}")


def _format_and_sort_races(races):
    """
    レースをグレード順に並べ替えて、summaryとlocationのみの形式に整形する
    """
    # グレードに基づいて並べ替える関数
    def _get_grade_key(event):
        summary = event.get('summary', '')
        # グレードを抽出
        grade_match = re.search(r'\(G([I]+)\)', summary)
        if grade_match:
            grade = grade_match.group(1)
            # 'I'の数に基づいて並べ替え (少ないほど上位)
            return len(grade)
        # グレードなしは最後
        return 999

    # グレード順にソート
    sorted_events = sorted(races, key=_get_grade_key)

    # race_nameとlocationのみの形式に整形
    return [
        {
            'race_name': event.get('summary', ''),
            'location': event.get('location', '')
        }
        for event in sorted_events
    ]
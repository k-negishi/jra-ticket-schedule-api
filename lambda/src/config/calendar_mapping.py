"""
年別マイカレンダーURLの設定（環境変数から取得）
"""

import os
import json
from typing import Dict, Any, Optional

def get_calendar_config(year: int) -> Optional[Dict[str, Any]]:
    """
    指定年のカレンダー設定を環境変数から取得
    
    Args:
        year: 対象年
        
    Returns:
        カレンダー設定辞書、存在しない場合はNone
    """
    try:
        # 環境変数からカレンダー設定を取得
        calendar_configs_json = os.environ.get('CALENDAR_CONFIGS', '{}')
        calendar_configs = json.loads(calendar_configs_json)
        
        # 指定年の設定を取得
        year_str = str(year)
        if year_str in calendar_configs:
            return calendar_configs[year_str]
        
        return None
        
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Failed to parse calendar config for year {year}: {str(e)}")
        return None

def get_available_years() -> list:
    """
    利用可能な年一覧を取得
    
    Returns:
        年のリスト（降順）
    """
    try:
        calendar_configs_json = os.environ.get('CALENDAR_CONFIGS', '{}')
        calendar_configs = json.loads(calendar_configs_json)
        
        years = [int(year) for year in calendar_configs.keys()]
        return sorted(years, reverse=True)
        
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Failed to get available years: {str(e)}")
        return [] 
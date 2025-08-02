import json
from typing import Dict, Any

def create_response(status_code: int, body: Dict[str, Any]) -> Dict[str, Any]:
    """
    Lambda Function URL用のレスポンスを作成
    """
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'GET, OPTIONS'
        },
        'body': json.dumps(body, ensure_ascii=False, default=str)
    }

def create_error_response(status_code: int, message: str) -> Dict[str, Any]:
    """
    エラーレスポンスを作成
    """
    return create_response(status_code, {
        'error': message,
        'status': 'error'
    })

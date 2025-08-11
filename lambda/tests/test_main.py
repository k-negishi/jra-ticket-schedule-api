import pytest
import json

from dotenv import load_dotenv

from src.main import lambda_handler

load_dotenv()

class TestLambdaHandler:
    def test_lambda_handler_success(self):
        """正常なリクエストのテスト"""
        event = {
            'requestContext': {
                'http': {
                    'method': 'GET'
                }
            },
            'rawPath': '/jra-calendar/events',
            'rawQueryString': 'year=2025&month=6&day=1'
        }
        
        response = lambda_handler(event, None)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        expected_events = [
            {'race_name': '日本ダービー(GI)', 'location': '東京競馬場'},
            {'race_name': '目黒記念(GII)', 'location': '東京競馬場'},
        ]
        assert body['events'] == expected_events
        print(body)

    def test_lambda_handler_missing_parameters(self):
        """パラメータ不足のテスト"""
        event = {
            'requestContext': {
                'http': {
                    'method': 'GET'
                }
            },
            'rawPath': '/jra-calendar/events',
            'rawQueryString': 'year=2025&month=1'  # dayが不足
        }
        
        response = lambda_handler(event, None)
        
        assert response['statusCode'] == 400
        body = json.loads(response['body'])
        assert 'error' in body
        assert 'year, month, and day are required parameters' in body['error']

    def test_lambda_handler_invalid_parameters(self):
        """無効なパラメータのテスト"""
        event = {
            'requestContext': {
                'http': {
                    'method': 'GET'
                }
            },
            'rawPath': '/jra-calendar/events',
            'rawQueryString': 'year=invalid&month=1&day=15'  # yearが無効
        }
        
        response = lambda_handler(event, None)
        
        assert response['statusCode'] == 400
        body = json.loads(response['body'])
        assert 'error' in body
        assert 'must be valid integers' in body['error']

    def test_lambda_handler_invalid_date(self):
        """無効な日付のテスト"""
        event = {
            'requestContext': {
                'http': {
                    'method': 'GET'
                }
            },
            'rawPath': '/jra-calendar/events',
            'rawQueryString': 'year=2025&month=13&day=1'  # 無効な月
        }
        
        response = lambda_handler(event, None)
        
        assert response['statusCode'] == 400
        body = json.loads(response['body'])
        assert 'error' in body
        assert 'Invalid date' in body['error']

    def test_lambda_handler_no_events_found(self):
        """イベントが見つからない場合のテスト"""
        event = {
            'requestContext': {
                'http': {
                    'method': 'GET'
                }
            },
            'rawPath': '/jra-calendar/events',
            'rawQueryString': 'year=2025&month=1&day=1'  # 非重賞開催日
        }
        
        response = lambda_handler(event, None)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert isinstance(body['events'], list)
        assert body['count'] == 0

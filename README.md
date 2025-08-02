# JRAカレンダーAPI

GoogleカレンダーAPIをリクエストするAWS Lambda関数です。
Lambda Function URL で直接アクセス可能で、指定した年・月・日のイベントを取得します。

## Tech Stack
- AWS Lambda
- Python 3.12対応
- Node.js 18以上
- Google Calendar API
- Serverless Framework


### 1. 開発環境セットアップ
```bash
cd lambda
npm run setup:dev
```

### 2. 環境変数設定
```bash
cp env.example .env
# .envファイルを編集してGoogle認証情報とカレンダー設定を設定
```

### 3. デプロイ
```bash
npm run deploy
```

## API仕様

```
GET https://[function-url-id].lambda-url.[region].on.aws/
/jra-calendar/events?year=2025&month=5&day=31


Response:
{
	"events": [
		{
			"race_name": "日本ダービー(GI)",
			"location": "東京競馬場"
		},
		{
			"race_name": "目黒記念(GII)",
			"location": "東京競馬場"
		},
		{
			"race_name": "葵ステークス(GIII)",
			"location": "京都競馬場"
		}
	],
	"date": "2025-05-31",
	"count": 3
}
```

## 詳細セットアップ

### 環境変数の設定
```bash
cd lambda
cp env.example .env
# .envファイルを編集してGoogle認証情報とカレンダー設定を設定
```

### 依存関係のインストール
```bash
cd lambda
npm install
```

### 開発環境の有効化
```bash
cd lambda
npm run activate:dev
```

### テスト実行
```bash
cd lambda
npm run test
```

### ローカルテスト
```bash
cd lambda
serverless invoke local --function getCalendarEvents --data '{"queryStringParameters": {"year": "2025", "month": "5", "day": "31"}}'
```

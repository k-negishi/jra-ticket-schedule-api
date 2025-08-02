# JRAカレンダーAPI

JRAカレンダーAPIは、Google Calendar APIを使用して日本中央競馬会(JRA)の重賞レース情報を取得するAPIです。  
AWS Lambda関数(Lambda Function URL)によって実装されており、指定した日付の競馬イベントを取得できます。  

カレンダーの元ネタは、JRAの公式のレーシングカレンダーを使用しています。
https://www.jra.go.jp/keiba/common/calendar/ics2025.html

## 技術スタック
- AWS Lambda
- Python 3.12
- Google Calendar API
- Serverless Framework

## API仕様
### リクエスト
```
GET https://[function-url-id].lambda-url.[region].on.aws/jra-calendar/events
```

#### クエリパラメータ
| パラメータ | 説明 | 例 |
| --- | --- | --- |
| year | 取得したい年 (必須) | 2025 |
| month | 取得したい月 (必須) | 5 |
| day | 取得したい日 (必須) | 31 |


### レスポンス例
```json
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

### 開発環境セットアップ
```bash
cd lambda
npm run setup:dev
```

### 環境変数設定
```bash
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

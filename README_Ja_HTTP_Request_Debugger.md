# HTTP Debugger Server

軽量で高機能な HTTP デバッグサーバです。  
`GET / POST / PUT / DELETE / PATCH` のすべての HTTP メソッドに対応し、  
受信したリクエストの内容を **Web UI でわかりやすく可視化**します。

フォーム送信、API テスト、multipart の解析、JSON/XML の整形など、  
HTTP リクエストの中身を確認したいときに最適です。

---

## ✨ 主な機能

### ✔ すべての HTTP メソッドに対応
- GET  
- POST  
- PUT  
- DELETE  
- PATCH  

### ✔ リクエスト内容を Web UI で表示
Bootstrap による見やすい UI。

### ✔ multipart/form-data の解析
- 各パートのヘッダ  
- name / filename  
- バイナリ内容（先頭 1024 bytes）  

### ✔ JSON / XML の整形表示
- `application/json` → インデント付きで整形  
- `application/xml` / `text/xml` → pretty print  

### ✔ 生のボディをそのまま表示
- `repr(raw_body)` を折り返して表示  
- 改行コードやバイナリも確認可能  

### ✔ hexdump 表示
バイナリデータの内容を 16 バイト幅で可視化。

---

## 🚀 使い方

### 1. サーバを起動

```bash
python debug_server.py
```

起動すると以下で待ち受けます：

```
http://localhost:8080/
```

### 2. 任意の HTTP クライアントからリクエストを送信

例：

```bash
curl -X POST http://localhost:8080/ -d "hello=world"
```

または multipart：

```bash
curl -X POST http://localhost:8080/ \
  -F "text=hello" \
  -F "file=@sample.png"
```

コマンドラインで実行すると標準出力に表示されるので、.htmlファイルにリダイレクト出力してブラウザで開くと読みやすくなります。


### 3. ブラウザで結果を確認

送信されたリクエスト内容が Web UI に表示されます。

#### サンプルコマンドと結果

- コマンド（Windows）
```DOS
curl -XPOST http://localhost:8080/ -H 'Content-Type:application/x-www-form-urlencoded' -H "Authorization: Bearer xxxxxxxxxxxxxxxxx" -F "file=@test.csv;type=multipart/form-data" -F "processinfo={\"type\":\"replace\",\"linkName\":\"Sample\",\"userKeyNames\":[{\"user\":\"UserAccountName1\",\"userAccount\": \"UserAccount1\"}],\"processingName\":\"SampleProcess\"};type=text/json" > result_sample.html
```

- 結果

[result_sample.html](result_sample.html)


---

## 📂 表示される情報

### GET
- Path  
- Query Parameters  
- Headers  

### POST / PUT / DELETE / PATCH
- Headers  
- Raw Body  
- Pretty JSON  
- Pretty XML  
- Hexdump  
- Multipart Parts  

---

## 🛠 技術的ポイント

- multipart の解析に `email.parser.BytesParser` を使用  
  → `cgi.FieldStorage` より安定して動作  
- Bootstrap による UI  
- Python 標準ライブラリのみで動作  
- ストリームを確実に読み切るため `Content-Length` を使用  

---

## 📜 ライセンス

自由に改変・利用できます。

---

## 🤝 作者へ

このツールは、HTTP リクエストの中身を深く理解したい開発者のために作られています。  
改善案や追加したい機能があれば、気軽に相談してください。



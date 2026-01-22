# HTTP Debugger Server

A lightweight yet powerful HTTP debugging server.  
It supports **GET / POST / PUT / DELETE / PATCH** and visualizes incoming HTTP requests in a clean, Bootstrap‑powered web interface.

This tool is ideal for inspecting HTTP requests during API development, form submission testing, multipart debugging, or analyzing raw request bodies.

---

## ✨ Features

### ✔ Supports all major HTTP methods
- GET  
- POST  
- PUT  
- DELETE  
- PATCH  

### ✔ Clean and readable Web UI
Built with Bootstrap for clarity and ease of use.

### ✔ Multipart/form-data parsing
Displays:
- Part headers  
- `name` and `filename`  
- Binary payload (first 1024 bytes)  

### ✔ Pretty‑printed JSON and XML
- `application/json` → formatted with indentation  
- `application/xml` / `text/xml` → pretty‑printed  

### ✔ Raw body inspection
Shows the raw request body using `repr()`, wrapped for readability.

### ✔ Hexdump view
Displays binary data in a 16‑byte hexdump format.

---

## 🚀 Usage

### 1. Start the server

```bash
python debug_server.py
```

The server listens on:

```
http://localhost:8080/
```

### 2. Send any HTTP request

Example (POST):

```bash
curl -X POST http://localhost:8080/ -d "hello=world"
```

Multipart example:

```bash
curl -X POST http://localhost:8080/ \
  -F "text=hello" \
  -F "file=@sample.png"
```

### 3. View results in your browser

The server displays all request details in a structured, readable format.

#### Sample Command and Result

- Command line(Windows)
```DOS
curl -XPOST http://localhost:8080/ -H 'Content-Type:application/x-www-form-urlencoded' -H "Authorization: Bearer xxxxxxxxxxxxxxxxx" -F "file=@test.csv;type=multipart/form-data" -F "processinfo={\"type\":\"replace\",\"linkName\":\"Sample\",\"userKeyNames\":[{\"user\":\"UserAccountName1\",\"userAccount\": \"UserAccount1\"}],\"processingName\":\"SampleProcess\"};type=text/json" > result_sample.html
```

- Result

[result_sample.html](result_sample.html)

---

## 📂 What gets displayed

### GET requests
- Path  
- Query parameters  
- Headers  

### POST / PUT / DELETE / PATCH requests
- Headers  
- Raw body  
- Pretty JSON  
- Pretty XML  
- Hexdump  
- Multipart parts  

---

## 🛠 Technical Notes

- Uses `email.parser.BytesParser` for robust multipart parsing  
  (more reliable than `cgi.FieldStorage`)
- Uses only Python standard libraries  
- Bootstrap UI for readability  
- Reads request bodies using `Content-Length` for accuracy  

---

## 📜 License

Free to modify and use.

---

## 🤝 About this project

This tool is designed for developers who want full visibility into HTTP requests.  
If you have ideas for improvements or new features, feel free to contribute or reach out.

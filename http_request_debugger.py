from http.server import BaseHTTPRequestHandler, HTTPServer
# emailはmultipart/form-data を解析するために使っている。
# cgi.FieldStorage が不安定で固まりやすい
# emailモジュールは本来メールのMIMEを扱うためのものだが、HTTPのmultipartもMIME形式なので非常に相性がいい。
import email 
from email.parser import BytesParser
from email.policy import default
import html
import textwrap
from urllib.parse import urlparse, parse_qs
import json
import xml.dom.minidom

# --- hexdump 関数 ---
def hexdump(data, width=16):
    lines = []
    for i in range(0, len(data), width):
        chunk = data[i:i+width]
        hex_part = " ".join(f"{b:02x}" for b in chunk)
        ascii_part = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
        lines.append(f"{i:08x}  {hex_part:<{width*3}}  {ascii_part}")
    return "\n".join(lines)


class DebugServer(BaseHTTPRequestHandler):

    # BootStrap
    head_html = """
    <head>
        <meta charset="utf-8">
        <title>HTTP Debugger</title>
        <link 
            href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" 
            rel="stylesheet"
        >
        <style>
            body { padding: 20px; font-size: 1.1rem; }
            pre { background: #f8f9fa; padding: 10px; border-radius: 5px; }
            h1, h2, h3 { margin-top: 1.5rem; }
        </style>
    </head>
    """


    # ============================
    #        GET リクエスト
    # ============================
    def do_GET(self):
        html_parts = []
        html_parts.append("<h1>GET Request Debugger</h1>")

        # --- パスとクエリ ---
        parsed = urlparse(self.path)
        html_parts.append(f"<h2>Path</h2><pre>{html.escape(parsed.path)}</pre>")

        # --- クエリパラメータ ---
        query = parse_qs(parsed.query)
        html_parts.append("<h2>Query Parameters</h2>")
        if query:
            qp_html = "<br>".join(f"{html.escape(k)} = {html.escape(str(v))}" for k, v in query.items())
            html_parts.append(f"<pre>{qp_html}</pre>")
        else:
            html_parts.append("<pre>(none)</pre>")

        # --- ヘッダ表示 ---
        html_parts.append("<h2>Request Headers</h2>")
        headers_html = "<br>".join(
            f"{html.escape(k)}: {html.escape(v)}" for k, v in self.headers.items()
        )
        html_parts.append(f"<pre>{headers_html}</pre>")

        # --- HTML を返す ---
        body = f"""
        <html>
        {self.head_html}
        <body class="container">
        {''.join(html_parts)}
        </body>
        </html>
        """
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))

    # =====================================
    # POST/PUT/DELETE/PATCH
    # =====================================
    def do_POST(self):
        self.handle_body_request("POST Request Debugger")
    def do_PUT(self):
        self.handle_body_request("PUT Request Debugger")
    def do_DELETE(self):
        self.handle_body_request("DELETE Request Debugger")
    def do_PATCH(self):
        self.handle_body_request("PATCH Request Debugger")

    # =====================================
    # POST/PUT/DELETE/PATCH 共通処理まとめ
    # =====================================
    def handle_body_request(self, title):
        content_length = int(self.headers.get('Content-Length', 0))
        raw_body = self.rfile.read(content_length)
        content_type = self.headers.get("Content-Type")

        html_parts = []
        html_parts.append(f"<h1>{title}</h1>")

        # --- ヘッダ表示 ---
        html_parts.append("<h2>Request Headers</h2>")
        headers_html = "<br>".join(
            f"{html.escape(k)}: {html.escape(v)}" for k, v in self.headers.items()
        )
        html_parts.append(f"<pre>{headers_html}</pre>")

        # --- Raw Body (repr) を折り返して表示 ---
        wrapped_repr = textwrap.fill(repr(raw_body), width=120)
        html_parts.append("<h2>Raw Body (repr)</h2>")
        html_parts.append(f"<pre>{html.escape(wrapped_repr)}</pre>")


        # --- JSON / XML 整形表示 ---
        if content_type:
            # JSON 整形
            if "application/json" in content_type:
                try:
                    parsed_json = json.loads(raw_body.decode("utf-8"))
                    pretty_json = json.dumps(parsed_json, indent=4, ensure_ascii=False)
                    html_parts.append("<h2>Pretty JSON</h2>")
                    html_parts.append(f"<pre>{html.escape(pretty_json)}</pre>")
                except Exception as e:
                    html_parts.append(f"<h2>Pretty JSON</h2><pre>JSON parse error: {html.escape(str(e))}</pre>")

            # XML 整形
            if "xml" in content_type:
                try:
                    dom = xml.dom.minidom.parseString(raw_body)
                    pretty_xml = dom.toprettyxml(indent="  ")
                    html_parts.append("<h2>Pretty XML</h2>")
                    html_parts.append(f"<pre>{html.escape(pretty_xml)}</pre>")
                except Exception as e:
                    html_parts.append(f"<h2>Pretty XML</h2><pre>XML parse error: {html.escape(str(e))}</pre>")


        # --- hexdump 表示 ---
        html_parts.append("<h2>Hexdump</h2>")
        html_parts.append(f"<pre>{html.escape(hexdump(raw_body))}</pre>")

        # --- multipart パース ---
        if content_type and content_type.startswith("multipart/"):
            msg = BytesParser(policy=default).parsebytes(
                b"Content-Type: " + content_type.encode() + b"\r\n\r\n" + raw_body
            )

            html_parts.append("<h2>Multipart Parts</h2>")

            for idx, part in enumerate(msg.iter_parts()):
                html_parts.append(f"<h3>Part {idx+1}</h3>")

                # ヘッダ
                part_headers = "<br>".join(
                    f"{html.escape(k)}: {html.escape(v)}" for k, v in part.items()
                )
                html_parts.append(f"<p><b>Headers:</b><br>{part_headers}</p>")

                # name / filename
                html_parts.append(f"<p><b>Name:</b> {html.escape(str(part.get_param('name', header='Content-Disposition')))}</p>")
                html_parts.append(f"<p><b>Filename:</b> {html.escape(str(part.get_filename()))}</p>")

                # 内容
                payload = part.get_payload(decode=True)
                if payload is not None:
                    html_parts.append("<b>Value (bytes, first 1024 bytes):</b>")
                    wrapped_payload = textwrap.fill(repr(payload[:1024]), width=120)
                    html_parts.append(f"<pre>{html.escape(wrapped_payload)}</pre>")
                else:
                    html_parts.append("<p>(No payload)</p>")
        else:
            html_parts.append("<h2>Not multipart/form-data</h2>")

        # --- HTML を返す ---
        body = f"""
        <html>
        {self.head_html}
        <body class="container">
        {''.join(html_parts)}
        </body>
        </html>
        """

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))


def run():
    server = HTTPServer(("", 8080), DebugServer)
    print("Debug server running at http://localhost:8080/")
    server.serve_forever()

if __name__ == "__main__":
    run()

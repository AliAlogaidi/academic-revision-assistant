import asyncio
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote

from app.rewriter import ACADEMIC_INTEGRITY_NOTE, AcademicRewriter


ROOT = Path(__file__).parent
STATIC = ROOT / "app" / "static"
INDEX = ROOT / "app" / "templates" / "index.html"


def load_local_env() -> None:
    env_path = ROOT / ".env"
    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"'))


load_local_env()
rewriter = AcademicRewriter()


class AcademicRevisionHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path in {"/", "/index.html"}:
            self._send_file(INDEX, "text/html; charset=utf-8")
            return

        if self.path.startswith("/static/"):
            requested = unquote(self.path.removeprefix("/static/"))
            file_path = (STATIC / requested).resolve()
            if STATIC.resolve() in file_path.parents and file_path.exists():
                self._send_file(file_path, self._content_type(file_path))
                return

        self._send_json({"detail": "Not found"}, status=404)

    def do_POST(self) -> None:
        if self.path != "/api/rewrite":
            self._send_json({"detail": "Not found"}, status=404)
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            text = str(payload.get("text", "")).strip()
            if len(text) < 20:
                self._send_json({"detail": "Text must contain at least 20 characters."}, status=422)
                return

            result = asyncio.run(
                rewriter.rewrite(
                    text=text,
                    tone=payload.get("tone", "formal"),
                    depth=payload.get("depth", "balanced"),
                    include_citation_notes=bool(payload.get("include_citation_notes", True)),
                )
            )
            self._send_json(
                {
                    "original": text,
                    "revised": result.revised,
                    "provider": result.provider,
                    "quality_notes": [note.__dict__ for note in result.quality_notes],
                    "academic_integrity_note": ACADEMIC_INTEGRITY_NOTE,
                }
            )
        except json.JSONDecodeError:
            self._send_json({"detail": "Invalid JSON."}, status=400)

    def log_message(self, format: str, *args: object) -> None:
        return

    def _send_file(self, file_path: Path, content_type: str) -> None:
        body = file_path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, data: dict, status: int = 200) -> None:
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _content_type(self, file_path: Path) -> str:
        if file_path.suffix == ".css":
            return "text/css; charset=utf-8"
        if file_path.suffix == ".js":
            return "application/javascript; charset=utf-8"
        return "application/octet-stream"


def main() -> None:
    host = "127.0.0.1"
    port = 8000
    server = ThreadingHTTPServer((host, port), AcademicRevisionHandler)
    print(f"Academic Revision Assistant running at http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    main()

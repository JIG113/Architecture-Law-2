import subprocess
import sys
import threading
import time
import tkinter as tk
from tkinter import messagebox
import webbrowser
from urllib.request import urlopen
from urllib.error import URLError


class DesktopLauncher:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Architecture Notice Launcher")
        self.root.geometry("500x220")
        self.server_process: subprocess.Popen[str] | None = None

        self.status_var = tk.StringVar(value="서버 중지")
        self.url_var = tk.StringVar(value="http://127.0.0.1:8000/docs")

        tk.Label(root, text="건축 공고/고시/지침 분석 시스템", font=("Arial", 14, "bold")).pack(pady=12)
        tk.Label(root, textvariable=self.status_var, fg="blue").pack(pady=4)

        tk.Button(root, text="서버 시작", command=self.start_server, width=20).pack(pady=4)
        tk.Button(root, text="Swagger 열기", command=self.open_docs, width=20).pack(pady=4)
        tk.Button(root, text="서버 중지", command=self.stop_server, width=20).pack(pady=4)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def start_server(self) -> None:
        if self.server_process and self.server_process.poll() is None:
            messagebox.showinfo("안내", "이미 서버가 실행 중입니다.")
            return

        cmd = [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"]
        self.server_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        self.status_var.set("서버 시작 중...")
        threading.Thread(target=self._wait_until_ready, daemon=True).start()

    def _wait_until_ready(self) -> None:
        for _ in range(40):
            if self._is_server_up():
                self.status_var.set("서버 실행 중 (http://127.0.0.1:8000)")
                return
            time.sleep(0.5)
        self.status_var.set("서버 시작 실패")

    def _is_server_up(self) -> bool:
        try:
            with urlopen("http://127.0.0.1:8000/health", timeout=1) as res:
                return res.status == 200
        except URLError:
            return False

    def open_docs(self) -> None:
        webbrowser.open(self.url_var.get())

    def stop_server(self) -> None:
        if self.server_process and self.server_process.poll() is None:
            self.server_process.terminate()
            self.server_process.wait(timeout=3)
            self.status_var.set("서버 중지")
        else:
            self.status_var.set("실행 중인 서버 없음")

    def on_close(self) -> None:
        try:
            self.stop_server()
        except Exception:
            pass
        self.root.destroy()


if __name__ == "__main__":
    app = tk.Tk()
    DesktopLauncher(app)
    app.mainloop()

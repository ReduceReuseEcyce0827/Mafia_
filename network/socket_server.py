import socket
import threading
from typing import Callable, List


class SocketServer:
    """간단한 TCP 소켓 서버. 메시지 수신 시 등록된 콜백을 호출합니다."""
    def __init__(self, host: str = '0.0.0.0', port: int = 16131):
        self.host = host
        self.port = port
        self.server_socket = None
        self._clients: List[socket.socket] = []
        self._accept_thread = None
        self._running = False
        self.on_message: Callable[[socket.socket, bytes], None] | None = None

    def start(self):
        if self._running:
            return
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
        except Exception:
            self.server_socket.close()
            raise
        self._running = True
        self._accept_thread = threading.Thread(target=self._accept_loop, daemon=True)
        self._accept_thread.start()

    def stop(self):
        self._running = False
        try:
            if self.server_socket:
                self.server_socket.close()
        finally:
            for c in list(self._clients):
                try:
                    c.close()
                except Exception:
                    pass
            self._clients.clear()

    def _accept_loop(self):
        while self._running:
            try:
                client, addr = self.server_socket.accept()
                self._clients.append(client)
                t = threading.Thread(target=self._client_loop, args=(client,), daemon=True)
                t.start()
            except OSError:
                break
            except Exception:
                continue

    def _client_loop(self, client: socket.socket):
        try:
            while self._running:
                data = client.recv(4096)
                if not data:
                    break
                if self.on_message:
                    try:
                        self.on_message(client, data)
                    except Exception:
                        pass
        finally:
            try:
                client.close()
            except Exception:
                pass
            if client in self._clients:
                self._clients.remove(client)

    def send(self, client: socket.socket, data: bytes):
        try:
            client.sendall(data)
        except Exception:
            try:
                client.close()
            except Exception:
                pass
            if client in self._clients:
                self._clients.remove(client)

    def broadcast(self, data: bytes):
        for c in list(self._clients):
            self.send(c, data)

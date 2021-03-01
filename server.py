from sendrecv import SendRecv
import socket
import pickle
import time


class Server:
    def __init__(self, ip="0.0.0.0", port=8888):
        self.host = ip
        self.port = port
        self.all_connections = {}
        self.cur_con = None

        self.sock = self.create_socket(self.port)

    def create_socket(self, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((self.host, self.port))
            sock.listen(20)
        except socket.error as msg:
            print("소켓 생성 에러... %s" % str(msg))
            time.sleep(3)
            print("다시 시도 합니다....")
            self.create_socket()
        return sock

    def connect_socket(self, progress_callback):
        try:
            conn, address = self.sock.accept()
            self.sock.setblocking(1)
            controller = SendRecv(conn)
            print(f"[!]새로운 클라이언트가 연결되었습니다 => [{address[0]}:{str(address[1])}]")
            address = f"{address[0]}:{str(address[1])}"
            self.all_connections[address] = controller
            print(f"{address} 연결 성공")
            return self.refresh(progress_callback)
        except:
            print(f"{address} 연결 실패")
            return []

    def refresh(self, progress_callback=None):
        """ 연결된 클라이언트가 연결되어 있는지 확인& 갱신"""
        for key in list(self.all_connections.keys()):
            try:
                controller = self.all_connections[key]
                controller.send(b":check")
                data = controller.recv()
                if data == b":Done":
                    continue
            except:
                del self.all_connections[key] # 연결이 끊긴 ip 삭제
                continue

        if progress_callback is None:
            # listview update
            return None
        else:
            return list(self.all_connections.keys())

    def get_log(self):
        """ 쓰레드"""
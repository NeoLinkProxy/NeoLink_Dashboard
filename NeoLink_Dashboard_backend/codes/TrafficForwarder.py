# from collections.abc import Callable
# import socket
# import threading
# import logging
# from typing import Literal

# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# # class TargetSocket:
# #     def __init__(self, host='127.0.0.1', port=9000):
# #         # 我要转发的目标socket
# #         self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# #         self.sock.connect((host, port))
# #         logging.info(f"TargetSocket connected to {host}:{port}")

# #     def send(self, data):
# #         # 在这里你可以做自己要处理的东西
# #         self.sock.sendall(data)

# class TargetSocket:
#     def __init__(self, host: str = '127.0.0.1', port: int = 9000, TCPOrUDP: Literal['TCP', 'UDP'] = 'TCP'):
#         self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         if TCPOrUDP == 'TCP':
#             self.sock.connect((host, port))
#         elif TCPOrUDP == 'UDP':
#             self.target_addr = (host, port)
#         else:
#             raise ValueError(f"TCPOrUDP must be 'TCP' or 'UDP', not {TCPOrUDP}")
#         logging.info(f"TargetSocket configured for {TCPOrUDP} to {host}:{port}")

#     def send(self, data: bytes):
#         self.sock.sendto(data, self.target_addr)


# # TCP转发器
# def tcp_forwarder(host: str = '127.0.0.1', port: int = 9000, bindport: int = 8080, func: Callable[[bytes], None] = lambda x: None) -> None:
#     target_socket = TargetSocket(host, port, TCPOrUDP='TCP')
#     tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     tcp_sock.bind(('0.0.0.0', bindport))
#     tcp_sock.listen(5)
#     logging.info(f"TCP forwarder listening on 0.0.0.0:{bindport}")

#     def handle_client(client_sock: socket.socket, addr: tuple[str, int]):
#         try:
#             while True:
#                 data = client_sock.recv(65535)
#                 if not data:
#                     break
#                 logging.debug(f"[TCP] Received {len(data)} bytes from {addr}")
#                 target_socket.send(data) # pyright: ignore[reportUnknownMemberType]
#         except Exception as e:
#             logging.error(f"[TCP] Error handling client {addr}: {e}")
#         finally:
#             client_sock.close()

#     try:
#         while True:
#             client_sock, addr = tcp_sock.accept()
#             logging.info(f"[TCP] New connection from {addr}")
#             thread = threading.Thread(target=handle_client, args=(client_sock, addr), daemon=True)
#             thread.start()
#     except KeyboardInterrupt:
#         logging.info("TCP forwarder shutting down...")
#     finally:
#         tcp_sock.close()

# # UDP转发器
# def udp_forwarder(host: str = '127.0.0.1', port: int = 9000, bindport: int = 8080, func: Callable[[bytes], None] = lambda x: None):
#     target_socket = TargetSocket(host, port, TCPOrUDP='UDP')
#     udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     udp_sock.bind(('0.0.0.0', bindport))
#     logging.info(f"UDP forwarder listening on 0.0.0.0:{bindport}")

#     try:
#         while True:
#             data, addr = udp_sock.recvfrom(65535)
#             logging.debug(f"[UDP] Received {len(data)} bytes from {addr}")
#             target_socket.send(data) # pyright: ignore[reportUnknownMemberType]
#     except KeyboardInterrupt:
#         logging.info("UDP forwarder shutting down...")
#     finally:
#         udp_sock.close()

# def create_TrafficFowarder(host: str = '127.0.0.1', port: int = 9000, bindport: int = 8080, TCPOrUDP: Literal['TCP', 'UDP'] = 'TCP', func: Callable[[bytes], None] = lambda x: None):
#     # thread
#     if type(host) != str:
#         raise ValueError(f"host must be str, not {type(host)}")
#     if len(host.split('.')) != 4:
#         raise ValueError(f"host must be IPv4 address, not {host}")
#     if type(port) != int:
#         raise ValueError(f"port must be int, not {type(port)}")
#     if type(TCPOrUDP) != str:
#         raise ValueError(f"TCPOrUDP must be str, not {type(TCPOrUDP)}")
#     if TCPOrUDP not in ('TCP', 'UDP'):
#         raise ValueError(f"TCPOrUDP must be 'TCP' or 'UDP', not {TCPOrUDP}")
#     if type(bindport) != int:
#         raise ValueError(f"bindport must be int, not {type(bindport)}")
#     if type(func) != Callable:
#         raise ValueError(f"func must be Callable, not {type(func)}")
    
#     if TCPOrUDP == 'TCP':
#         thread = threading.Thread(target=tcp_forwarder, daemon=True, args=(host, port, bindport, func))
#     elif TCPOrUDP == 'UDP':
#         thread = threading.Thread(target=udp_forwarder, daemon=True, args=(host, port, bindport, func))
#     else:
#         raise ValueError(f"TCPOrUDP must be 'TCP' or 'UDP', not {TCPOrUDP}")
    
#     # start thread
#     thread.start()

    
#     logging.info(f"流量转发器已启动在{bindport}端口上，{TCPOrUDP}模式")
    
#     # try:
#     #     # tcp_thread.join()
#     #     thread.join()
#     # except KeyboardInterrupt:
#     #     logging.info("转发结束")


# if __name__ == '__main__':
#     # tcp_thread = threading.Thread(target=tcp_forwarder, daemon=True, args=('127.0.0.1', 9000, 8080))
#     udp_thread = threading.Thread(target=udp_forwarder, daemon=True, args=('127.0.0.1', 9000, 8080))

#     # tcp_thread.start()
#     udp_thread.start()

#     logging.info(f"流量转发器已启动在8080端口上，UDP模式")

#     try:
#         # tcp_thread.join()
#         udp_thread.join()
#     except KeyboardInterrupt:
#         logging.info("转发结束")
from collections.abc import Callable
import socket
import threading
import logging
import types
from typing import Literal

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TrafficStats:
    def __init__(self, port: int, protocol: str):
        self.port = port
        self.protocol = protocol.upper()
        self.inbound_bytes = 0
        self.outbound_bytes = 0
        self.total_packets = 0
        self.lock = threading.Lock()
        
    def update_stats(self, data: bytes, direction: str = 'inbound'):
        with self.lock:
            self.total_packets += 1
            if direction == 'inbound':
                self.inbound_bytes += len(data)
            elif direction == 'outbound':
                self.outbound_bytes += len(data)
    
    def get_stats(self):
        with self.lock:
            return {
                'port': self.port,
                'protocol': self.protocol,
                'inbound_bytes': self.inbound_bytes,
                'outbound_bytes': self.outbound_bytes,
                'total_packets': self.total_packets
            }
    
    def print_stats(self):
        stats = self.get_stats()
        print(f"\n{stats['protocol']} 端口 {stats['port']} 流量统计:")
        print(f"  入站字节: {stats['inbound_bytes']}")
        print(f"  出站字节: {stats['outbound_bytes']}")
        print(f"  总包数: {stats['total_packets']}")

class TargetSocket:
    def __init__(self, host: str = '127.0.0.1', port: int = 9000, TCPOrUDP: Literal['TCP', 'UDP'] = 'TCP'):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if TCPOrUDP == 'TCP':
            self.sock.connect((host, port))
        elif TCPOrUDP == 'UDP':
            self.target_addr = (host, port)
        else:
            raise ValueError(f"TCPOrUDP must be 'TCP' or 'UDP', not {TCPOrUDP}")
        logging.info(f"TargetSocket configured for {TCPOrUDP} to {host}:{port}")

    def send(self, data: bytes):
        self.sock.sendto(data, self.target_addr)


# TCP转发器
def tcp_forwarder(host: str = '127.0.0.1', port: int = 9000, bindport: int = 8080, func: Callable[[bytes], None] = lambda x: None) -> None:
    target_socket = TargetSocket(host, port, TCPOrUDP='TCP')
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_sock.bind(('0.0.0.0', bindport))
    tcp_sock.listen(5)
    logging.info(f"TCP forwarder listening on 0.0.0.0:{bindport}")
    
    # 创建流量统计对象
    traffic_stats = TrafficStats(bindport, 'TCP')

    def handle_client(client_sock: socket.socket, addr: tuple[str, int]):
        try:
            while True:
                data = client_sock.recv(65535)
                if not data:
                    break
                logging.debug(f"[TCP] Received {len(data)} bytes from {addr}")
                # 更新入站统计
                traffic_stats.update_stats(data, 'inbound')
                # 执行自定义处理函数
                func(data)
                # 更新出站统计
                traffic_stats.update_stats(data, 'outbound')
                target_socket.send(data)  # pyright: ignore[reportUnknownMemberType]
        except Exception as e:
            logging.error(f"[TCP] Error handling client {addr}: {e}")
        finally:
            client_sock.close()

    try:
        while True:
            client_sock, addr = tcp_sock.accept()
            logging.info(f"[TCP] New connection from {addr}")
            thread = threading.Thread(target=handle_client, args=(client_sock, addr), daemon=True)
            thread.start()
    except KeyboardInterrupt:
        logging.info("TCP forwarder shutting down...")
        traffic_stats.print_stats()  # 打印最终统计
    finally:
        tcp_sock.close()

# UDP转发器
def udp_forwarder(host: str = '127.0.0.1', port: int = 9000, bindport: int = 8080, func: Callable[[bytes], None] = lambda x: None):
    target_socket = TargetSocket(host, port, TCPOrUDP='UDP')
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.bind(('0.0.0.0', bindport))
    logging.info(f"UDP forwarder listening on 0.0.0.0:{bindport}")
    
    # 创建流量统计对象
    traffic_stats = TrafficStats(bindport, 'UDP')

    try:
        while True:
            data, addr = udp_sock.recvfrom(65535)
            logging.debug(f"[UDP] Received {len(data)} bytes from {addr}")
            # 更新入站统计
            traffic_stats.update_stats(data, 'inbound')
            # 执行自定义处理函数
            func(data)
            # 更新出站统计
            traffic_stats.update_stats(data, 'outbound')
            target_socket.send(data)  # pyright: ignore[reportUnknownMemberType]
    except KeyboardInterrupt:
        logging.info("UDP forwarder shutting down...")
        traffic_stats.print_stats()  # 打印最终统计
    finally:
        udp_sock.close()

def create_TrafficFowarder(host: str = '127.0.0.1', port: int = 9000, bindport: int = 8080, TCPOrUDP: Literal['TCP', 'UDP'] = 'TCP', func: Callable[[bytes], None] = lambda x: None):
    # 参数验证
    if type(host) != str:
        raise ValueError(f"host must be str, not {type(host)}")
    if len(host.split('.')) != 4:
        raise ValueError(f"host must be IPv4 address, not {host}")
    if type(port) != int:
        raise ValueError(f"port must be int, not {type(port)}")
    if type(TCPOrUDP) != str:
        raise ValueError(f"TCPOrUDP must be str, not {type(TCPOrUDP)}")
    if TCPOrUDP not in ('TCP', 'UDP'):
        raise ValueError(f"TCPOrUDP must be 'TCP' or 'UDP', not {TCPOrUDP}")
    if type(bindport) != int:
        raise ValueError(f"bindport must be int, not {type(bindport)}")
    if not callable(func):
        raise ValueError("func must be callable")
    
    if TCPOrUDP == 'TCP':
        thread = threading.Thread(target=tcp_forwarder, daemon=True, args=(host, port, bindport, func))
    elif TCPOrUDP == 'UDP':
        thread = threading.Thread(target=udp_forwarder, daemon=True, args=(host, port, bindport, func))
    else:
        raise ValueError(f"TCPOrUDP must be 'TCP' or 'UDP', not {TCPOrUDP}")
    
    # 启动线程
    thread.start()
    
    logging.info(f"流量转发器已启动在{bindport}端口上，{TCPOrUDP}模式")

# 使用示例
if __name__ == '__main__':
    # 创建一个简单的处理函数，用于打印数据包大小
    def packet_handler(data: bytes):
        print(f"[+] 转发了 {len(data)} 字节的数据")
    
    # 创建TCP转发器并传入处理函数
    create_TrafficFowarder('127.0.0.1', 9000, 8080, 'TCP', packet_handler)
    
    # 如果需要创建UDP转发器
    # create_TrafficFowarder('127.0.0.1', 9000, 8080, 'UDP', packet_handler)
    
    try:
        # 保持主线程运行
        while True:
            pass
    except KeyboardInterrupt:
        logging.info("转发结束")

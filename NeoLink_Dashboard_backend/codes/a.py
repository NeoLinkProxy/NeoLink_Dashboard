# from scapy.all import sniff, TCP, UDP, IP
# import threading
# import time

# class PassivePortMonitor:
#     def __init__(self, port, protocol='tcp'):
#         self.port = port
#         self.protocol = protocol.lower()
#         if self.protocol not in ('tcp', 'udp'):
#             raise ValueError("协议必须是 'tcp' 或 'udp'")
#         self.inbound_bytes = 0
#         self.outbound_bytes = 0
#         self.total_packets = 0
#         self.is_monitoring = False
#         self.lock = threading.Lock()
        
#     def _packet_handler(self, packet):
#         """处理每个捕获的数据包"""
#         if not self.is_monitoring:
#             return
            
#         try:
#             if IP not in packet:
#                 return

#             # 根据协议处理
#             if self.protocol == 'tcp' and TCP in packet:
#                 layer = packet[TCP]
#             elif self.protocol == 'udp' and UDP in packet:
#                 layer = packet[UDP]
#             else:
#                 print(f"[!] 警告: 未处理的 {self.protocol.upper()} 数据包")
#                 return

#             if layer.dport == self.port or layer.sport == self.port:
#                 payload_len = len(layer.payload)
                
#                 with self.lock:
#                     self.total_packets += 1
#                     if layer.dport == self.port:
#                         self.inbound_bytes += payload_len
#                     elif layer.sport == self.port:
#                         self.outbound_bytes += payload_len

#         except Exception as e:
#             print(f"[!] WARNING: 处理数据包时出错: {e}")
    
#     def start_monitoring(self):
#         if self.is_monitoring:
#             print(f"[!] WARNING: 端口 {self.port} ({self.protocol.upper()}) 已在监控中")
#             return
            
#         self.is_monitoring = True
#         print(f"[-] 开始被动监控 {self.protocol.upper()} 端口 {self.port} 的流量（需要 root 权限）")
        
#         # 构建 BPF 过滤器
#         bpf_filter = f"{self.protocol} port {self.port}"
        
#         def sniff_thread():
#             try:
#                 sniff(
#                     iface="lo", # 只抓本地回环
#                     filter=bpf_filter,
#                     prn=self._packet_handler,
#                     store=False,
#                     stop_filter=lambda x: not self.is_monitoring
#                 )
#             except Exception as e:
#                 print(f"[!] 抓包失败: {e}")
#                 self.is_monitoring = False
        
#         self.sniff_thread = threading.Thread(target=sniff_thread)
#         self.sniff_thread.daemon = True
#         self.sniff_thread.start()
    
#     def stop_monitoring(self):
#         self.is_monitoring = False
#         print(f"[-] 停止监控 {self.protocol.upper()} 端口 {self.port}")
    
#     def get_stats(self):
#         with self.lock:
#             return {
#                 'port': self.port,
#                 'protocol': self.protocol.upper(),
#                 'inbound_bytes': self.inbound_bytes,
#                 'outbound_bytes': self.outbound_bytes,
#                 'total_packets': self.total_packets
#             }
    
#     def print_stats(self):
#         stats = self.get_stats()
#         print(f"\n{stats['protocol']} 端口 {stats['port']} 被动流量统计:")
#         print(f"  入站字节: {stats['inbound_bytes']}")
#         print(f"  出站字节: {stats['outbound_bytes']}")
#         print(f"  总包数: {stats['total_packets']}")

# if __name__ == "__main__":
#     import sys
#     if len(sys.argv) < 2:
#         print("用法: sudo python monitor.py <端口号> [tcp|udp]")
#         sys.exit(1)
        
#     port = int(sys.argv[1])
#     protocol = sys.argv[2].lower() if len(sys.argv) > 2 else 'tcp'
    
#     try:
#         monitor = PassivePortMonitor(port=port, protocol=protocol)
#     except ValueError as e:
#         print(f"[!] 错误: {e}")
#         sys.exit(1)
    
#     try:
#         monitor.start_monitoring()
#         print("按 Ctrl+C 停止监控...")
#         while True:
#             time.sleep(5)
#             monitor.print_stats()
#     except KeyboardInterrupt:
#         monitor.stop_monitoring()
#         monitor.print_stats()
#         print("[-] 监控结束")

import builtins


print(type(print))
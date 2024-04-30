import socket
import threading
import socks
import ipaddress
import random
import time

class ProxyServer:
    def __init__(self, subnet="fe80::/64", prefix_length=64, num_proxies=1, rotation_interval=600, username=None, password=None, allowed_hosts=None, blocked_hosts=None):
        self.subnet = subnet
        self.prefix_length = prefix_length
        self.num_proxies = num_proxies
        self.rotation_interval = rotation_interval
        self.username = username
        self.password = password
        self.allowed_hosts = allowed_hosts
        self.blocked_hosts = blocked_hosts
        self.proxies = []
        self.rotate_ipv6_thread = None
        self.rotation_stop_event = threading.Event()


    def generate_ipv6(self):
        """
        Генерация случайного IPv6 адреса из заданной подсети.
        """
        
        ipv6_network = ipaddress.IPv6Network(self.subnet)
        return str(ipaddress.IPv6Address(random.randint(int(ipv6_network.network_address), int(ipv6_network.broadcast_address))))


    def rotate_ipv6(self):
        """
        Ротация IPv6 адресов каждые rotation_interval секунд.
        """
        
        while not self.rotation_stop_event.is_set():
            self.proxies = [self.generate_ipv6() for _ in range(self.num_proxies)]
            print(f"Rotated {self.num_proxies} IPv6 proxies")
            time.sleep(self.rotation_interval)


    def handle_client(self, client_socket, proxy_index):
        """
        Обработка подключения клиента.
        """
        
        proxy_ip = self.proxies[proxy_index]
        print(f"Client connected. Proxy IPv6: {proxy_ip}")
        client_socket.send(proxy_ip.encode())
        client_socket.close()


    def start_socks5_server(self):
        """
        Функция, которая осуществляет запуск SOCKS5 сервера.
        """
        
        server = socks.socksocket(socket.AF_INET6, socket.SOCK_STREAM)
        server.bind(('::', 1080))
        server.listen(5)
        print("[*] SOCKS5 Server started on :: at port 1080")

        self.rotate_ipv6_thread = threading.Thread(target=self.rotate_ipv6)
        self.rotate_ipv6_thread.start()

        while True:
            client_socket, addr = server.accept()
            print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
            proxy_index = random.randint(0, self.num_proxies - 1)
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket, proxy_index))
            client_handler.start()


    def stop_rotation(self):
        """
        Функция, которая выполняет остановку ротации IPv6 адресов.
        """
        
        self.rotation_stop_event.set()
        self.rotate_ipv6_thread.join()
        

    def get_proxy_info(self):
        """
        Функция, которая возвращает информацию о прокси-сервере
        """
        
        return {
            "num_proxies": self.num_proxies,
            "rotation_interval": self.rotation_interval,
            "username": self.username,
            "password": self.password,
            "allowed_hosts": self.allowed_hosts,
            "blocked_hosts": self.blocked_hosts
        }


if __name__ == "__main__":
    proxy_server = ProxyServer(subnet="fe80::", prefix_length=48, num_proxies=10, rotation_interval=300)
    proxy_server.start_socks5_server()

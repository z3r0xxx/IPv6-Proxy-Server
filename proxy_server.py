import socket
import threading
import socks
import ipaddress
import random
import time

class ProxyServer:
    def __init__(self, subnet="fe80::/64", prefix_length=64, num_proxies=1, username=None, password=None, allowed_hosts=None, blocked_hosts=None):
        self.subnet = subnet
        self.prefix_length = prefix_length
        self.num_proxies = num_proxies
        self.username = username
        self.password = password
        self.allowed_hosts = allowed_hosts
        self.blocked_hosts = blocked_hosts
        self._proxies = []

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
        
        self._proxies = [self.generate_ipv6() for _ in range(self.num_proxies)]
        print(f"Rotated {self.num_proxies} IPv6 proxies")


    def handle_client(self, client_socket, proxy_index):
        """
        Обработка подключения клиента.
        """
        
        if self.username and self.password:
            # Читаем заголовок авторизации от клиента
            auth_header = client_socket.recv(1024).decode()

            # Проверяем наличие и корректность заголовка авторизации
            if not auth_header.startswith('Authorization: Basic '):
                # Если заголовок не передан или некорректен, отправляем код статуса 401 Unauthorized
                client_socket.sendall(b"HTTP/1.1 401 Unauthorized\r\nWWW-Authenticate: Basic realm='Proxy Server'\r\n\r\n")
                client_socket.close()
                return

            # Извлекаем закодированные учетные данные из заголовка
            encoded_credentials = auth_header[len('Authorization: Basic '):]
            # Декодируем и разделяем учетные данные на логин и пароль
            credentials = encoded_credentials.strip().decode('base64').split(':')
            
            # Проверяем, совпадают ли переданные учетные данные с установленными
            if credentials[0] != self.username or credentials[1] != self.password:
                # Если учетные данные не совпадают, отправляем код статуса 401 Unauthorized
                client_socket.sendall(b"HTTP/1.1 401 Unauthorized\r\nWWW-Authenticate: Basic realm='Proxy Server'\r\n\r\n")
                client_socket.close()
                return

        # Ротация адресов
        self.rotate_ipv6()
        # Выбираем адрес клиенту
        proxy_ip = self._proxies[proxy_index]
        print(f"Client connected. Proxy IPv6: {proxy_ip}")
        
        # Если учетные данные верны или не требуется аутентификация
        # Отправляем клиенту IP адрес прокси
        client_socket.sendall(proxy_ip.encode())
        
        while True:
            request = client_socket.recv(4096)
            if not request:
                break
            print("Received request:")
            print(request.decode())

        client_socket.close()


    def start_socks5_server(self):
        """
        Функция, которая осуществляет запуск SOCKS5 сервера.
        """
        
        server = socks.socksocket(socket.AF_INET6, socket.SOCK_STREAM)
        server.bind(('::', 1081))
        server.listen(5)
        print("[*] SOCKS5 Server started on :: at port 1080")

        while True:
            client_socket, addr = server.accept()
            print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
            proxy_index = random.randint(0, self.num_proxies - 1)
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket, proxy_index))
            client_handler.start()
        

    def get_proxy_info(self):
        """
        Функция, которая возвращает информацию о прокси-сервере
        """
        
        return {
            "num_proxies": self.num_proxies,
            "username": self.username,
            "password": self.password,
            "allowed_hosts": self.allowed_hosts,
            "blocked_hosts": self.blocked_hosts
        }
    
    
    def get_all_proxies(self):
        """
        Функция, которая возвращает список всех текущих прокси-адресов.
        """
        return self._proxies
    

if __name__ == "__main__":

    # Создание экземпляра прокси-сервера
    proxy_server = ProxyServer(subnet="2a0f:cdc6:50:fe::/64", prefix_length=64, num_proxies=10)

    # Запуск SOCKS5 сервера
    proxy_server.start_socks5_server()

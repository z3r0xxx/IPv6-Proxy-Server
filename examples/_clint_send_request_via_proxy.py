import requests

proxy = {
    'http': f'socks5://user:password@[2a0f:cdc6:50:fe:bc8e:1bd9:4493:b816]:1082',
    'https': f'socks5://user:password@[2a0f:cdc6:50:fe:bc8e:1bd9:4493:b816]:1082'
}

url = 'http://ifconfig.me/ip'
try:
    response = requests.get(url, proxies=proxy, timeout=10)
    if response.status_code == 200:
        print("Successfull")
    else:
        print("Error with using proxy (responce.status):", response.status_code)
except Exception as e:
    print("Error with using proxy:", e)
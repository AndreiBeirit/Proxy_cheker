import requests
import json

paths = {
    'buy_proxy_path': 'D:/buy_proxy.txt',
    'us_proxy_path': 'D:/US.txt',
    'eu_proxy_path': 'D:/EU.txt',
    'not_supported_path': 'D:/NOT_supported_proxy.txt'
}

url = 'https://geo.battle.net/'

def save_proxy(line, country):
    match country:
        case 'GB' | 'CZ' | 'RU' | 'KZ':
            with open(paths['eu_proxy_path'], 'a', encoding='utf-8') as eu_file:
                eu_file.write(line + '\n')
            print(f"Страна {country}, сохранен в {paths['eu_proxy_path']}\n")
        case 'US' | 'MX' | 'CA':
            with open(paths['us_proxy_path'], 'a', encoding='utf-8') as us_file:
                us_file.write(line + '\n')
            print(f"Страна {country}, сохранен в {paths['us_proxy_path']}\n")
        case _:
            with open(paths['not_supported_path'], 'a', encoding='utf-8') as not_supported_file:
                not_supported_file.write(line + '\n')
            print(f"Страна {country}, сохранен в {paths['not_supported_path']}\n")

try:
    with open(paths['buy_proxy_path'], 'r', encoding='utf-8') as proxy_file:
        for line in proxy_file:
            line = line.strip()
            if not line:
                continue
            proxy_parts = line.split('@')
            if len(proxy_parts) == 2:
                ip_port, login_password = proxy_parts
                proxies = {
                    'https': f'http://{login_password}@{ip_port}'
                }
                try:
                    print(f"Проверка прокси: {line}")
                    response = requests.get('https://oauth.battle.net/', proxies=proxies)
                    if response.status_code == 403:
                        with open('D:/403.txt', 'a', encoding='utf-8') as forbidden_file:
                            forbidden_file.write(line + '\n')
                        print(f"Прокси {line} получил код 403. Сохранен в файл D:/403.txt")
                    else:
                        print(f"Прокси {line} прошел проверку. Переходим к проверке геоданных.")
                        response = requests.get(url, proxies=proxies)
                        if response.status_code == 200:
                            data = json.loads(response.text)
                            country = data.get('country')
                            if country:
                                save_proxy(line, country)
                            else:
                                print("Значение 'country' не найдено в ответе.")
                        else:
                            print(f"Ошибка при выполнении запроса. Статус-код: {response.status_code}")
                except requests.RequestException as e:
                    print(f"Произошла ошибка при выполнении запроса: {e}")
                except json.JSONDecodeError:
                    print("Ошибка при разборе JSON-ответа.")
            else:
                print(f"Некорректный формат прокси: {line}")

except FileNotFoundError:
    print(f"Файл с прокси не найден: {paths['buy_proxy_path']}")

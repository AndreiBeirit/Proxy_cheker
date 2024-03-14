import requests
import json

# buy_proxy_path = 'C:/battle.net-manager/buy_proxy.txt'

# us_proxy_path = 'C:/battle.net-manager/US.txt'
# eu_proxy_path = 'C:/battle.net-manager/EU.txt'
# not_supported_path = 'C:/battle.net-manager/NOT_supported_proxy.txt'

buy_proxy_path = 'D:/buy_proxy.txt'

us_proxy_path = 'D:/US.txt'
eu_proxy_path = 'D:/EU.txt'
not_supported_path = 'D:/NOT_supported_proxy.txt'

url = 'https://geo.battle.net/'

try:
    with open(buy_proxy_path, 'r', encoding='utf-8') as proxy_file:
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
                    response = requests.get(url, proxies=proxies)
                    if response.status_code == 200:
                        data = json.loads(response.text)
                        if 'country' in data:
                            country = data['country']
                            if country == 'US':
                                with open(us_proxy_path, 'a', encoding='utf-8', newline='') as us_file:
                                    us_file.write(line + '\n')
                                print(f"Страна {country}, сохранен в {us_proxy_path}\n")
                            elif country == 'GB':
                                with open(eu_proxy_path, 'a', encoding='utf-8', newline='') as eu_file:
                                    eu_file.write(line + '\n')
                                print(f"Страна {country}, сохранен в {eu_proxy_path}\n")
                            elif country == 'CZ':
                                with open(eu_proxy_path, 'a', encoding='utf-8', newline='') as eu_file:
                                    eu_file.write(line + '\n')
                                print(f"Страна {country}, сохранен в {eu_proxy_path}\n")
                            elif country == 'RU':
                                with open(eu_proxy_path, 'a', encoding='utf-8', newline='') as eu_file:
                                    eu_file.write(line + '\n')
                                print(f"Страна {country}, сохранен в {eu_proxy_path}\n")
                            else:
                                with open(not_supported_path, 'a', encoding='utf-8', newline='') as not_supported_file:
                                    not_supported_file.write(line + '\n')
                                print(f"Страна {country}, сохранен в {not_supported_path}\n")
                        else:
                            print(f"Значение 'country' не найдено в ответе.")
                    else:
                        print(f"Ошибка при выполнении запроса. Статус-код: {response.status_code}")
                except requests.RequestException as e:
                    print(f"Произошла ошибка при выполнении запроса: {e}")
                except json.JSONDecodeError:
                    print("Ошибка при разборе JSON-ответа.")
            else:
                print(f"Некорректный формат прокси: {line}")

except FileNotFoundError:
    print(f"Файл с прокси не найден: {buy_proxy_path}")

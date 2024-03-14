def format_proxy(proxy):
    parts = proxy.split(':')
    if len(parts) == 4:
        return f"{parts[0]}:{parts[1]}@{parts[2]}:{parts[3]}"
    else:
        return "Неверный формат прокси"


file_path = 'D:/buy_proxy.txt'

formatted_proxies = []

with open(file_path, 'r') as file:
    proxies = file.readlines()
    for proxy in proxies:
        formatted_proxies.append(format_proxy(proxy.strip()))

output_file = 'D:/formatted_proxies.txt'

with open(output_file, 'w') as file:
    for proxy in formatted_proxies:
        file.write(f"{proxy}\n")

print("Преобразование прокси завершено. Результат записан в файл:", output_file)

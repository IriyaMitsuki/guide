import requests
from bs4 import BeautifulSoup
import re
import sys
import os
import time

def parse_vpn_keys(start_id, end_id):
    base_url = "https://outlinekeys.com/key/"
    file_path = "vpn_keys.txt"

    if not os.path.exists(file_path):
        open(file_path, 'a', encoding="utf-8").close()

    total_keys = end_id - start_id + 1
    keys_processed = 0

    for key_id in range(start_id, end_id + 1):
        url = base_url + str(key_id)
        try:
            response = requests.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")
            title = soup.title.string.strip()
            cleaned_title = " ".join(title.split())

            if cleaned_title == "404: Not Found":
                print(f"Ключ {key_id}: Не найден (404)")
            else:
                match = re.match(r"Key (.+) #(\d+) / Outline VPN", cleaned_title)
                if match:
                    country_name = match.group(1)
                    extracted_id = int(match.group(2))

                    if extracted_id != key_id:
                        print(f"Ключ {key_id}: Несоответствие ID в заголовке ({extracted_id})")
                        continue  # Пропускаем текущую итерацию, если ID не совпадает

                    textarea = soup.find("textarea", {"id": "accessKey"})
                    if textarea:
                        key_text = textarea.text.strip()
                        formatted_key = f"{key_text}\n"
                        with open(file_path, "a", encoding="utf-8") as f:
                            f.write(formatted_key)
                        print(f"Ключ {key_id}: Успешно извлечен и записан в файл") # Этот print  будет перезаписан прогресс баром
                    else:
                        print(f"Ключ {key_id}: Текстовое поле не найдено") # Этот print  будет перезаписан прогресс баром

                else:
                    print(f"Ключ {key_id}: Неверный формат заголовка: {cleaned_title}") # Этот print  будет перезаписан прогресс баром


        except requests.exceptions.RequestException as e:
            print(f"Ключ {key_id}: Ошибка запроса: {e}") # Этот print  будет перезаписан прогресс баром

        finally:
            keys_processed += 1
            progress = (keys_processed / total_keys) * 100
            print(f"Прогресс: [{'#' * int(progress / 5)}{' ' * (20 - int(progress / 5))}] {progress:.1f}%", end='\r')
            time.sleep(0.1)

    print("\n")  # Перенос строки после завершения прогресс бара
    if os.path.getsize(file_path) > 0:
        print("Ключи сохранены в vpn_keys.txt")
    else:
        print("Ключи не найдены.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Использование: python script.py <начальный_ID> <конечный_ID>")
        sys.exit(1)

    try:
        start_id = int(sys.argv[1])
        end_id = int(sys.argv[2])

        if start_id <= 0 or end_id <= 0 or start_id > end_id:
            print("Неверный диапазон ID. Убедитесь, что начальный и конечный ID являются положительными целыми числами, и начальный ID меньше или равен конечному ID.")
            sys.exit(1)

        parse_vpn_keys(start_id, end_id)

    except ValueError:
        print("Неверный формат ID. Введите целые числа.")
        sys.exit(1)

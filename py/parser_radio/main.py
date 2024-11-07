import requests
from bs4 import BeautifulSoup

def parse_radio_data(url, output_file="radio_data.txt"):
    """
    Парсит данные о радиостанциях и добавляет их в текстовый файл.

    Args:
        url: Полный URL веб-страницы для парсинга.
        output_file: Имя выходного текстового файла.
    """

    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        buttons = soup.find_all("button", class_="b-play station_play")

        with open(output_file, "a", encoding="utf-8") as f:  # 'a' для добавления данных
            for button in buttons:
                stream = button.get("stream")
                radioimg = button.get("radioimg")
                radioname = button.get("radioname")

                if stream and radioimg and radioname:
                    f.write(f"{stream}|{radioimg}|{radioname}\n")

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к URL: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    url = input("Введите URL для парсинга: ")
    parse_radio_data(url)
    print(f"Данные добавлены в файл radio_data.txt")
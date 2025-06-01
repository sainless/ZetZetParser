from platform import machine

from bs4 import BeautifulSoup
from colorama import init
from colorama import Fore, Back, Style
import csv
import json
import time
import requests
init()
r = requests.get("https://zetzet.ru/category/originalnye-aksessuary-apple/apple/")
soup = BeautifulSoup(r.text, "lxml")


# Менюшечка

def menu() -> int:
    print(Fore.GREEN + "Приветствую. Я небольшой скрипт, который поможет тебе извлечь данные с интернет-магазина ZetZet\n\
    Выбери опцию, где ты будешь сохранять будущие данные:"
    )

    print(Fore.RED + "1. JSON")
    print(Fore.YELLOW + "2. CSV (рекомендую)")

    enter_user = int(input(Fore.CYAN + "Выберите опцию: "))
    print("Парсер запущен!")
    time.sleep(2)

    return enter_user


# Функция которая парсит Apple телефоны

def parser_apple():

    data = [] # список с данными
    numerate = 0 # Отчёт
    blocks = soup.find_all("li", itemtype="http://schema.org/Product")

    for block in blocks:

        title = block.find("span", itemprop="name")
        price = block.find("span", class_="price nowrap")
        links = block.find("a", title=f"{title.text}").get("href")
        numerate+=1
        data.append([numerate, title.text.strip('\u0420'), price.text, links.strip('/'), f"https://zetzet.ru/{links.strip('/')}/"])

    return data

# Функция позволяющая сохранять данные в CSV документе

def save_data_to_csv():
    data_csv = parser_apple()  # Получаем данные из парсера

    # Правильные заголовки столбцов
    headers = ["№", "Название", "Цена", "Артикул", "Ссылка"]

    with open("iphones_tech.csv", mode='w') as file:
        writer = csv.writer(file, delimiter=";")

        # Записываем заголовки
        writer.writerow(headers)

        # Записываем данные построчно
        for row in data_csv:
            writer.writerow(row)


# Функция позволяющая сохранять данные в JSON формате

def save_data_to_json():

    data = parser_apple()

    # Преобразуем в JSON-строку
    json_data = json.dumps(data, indent=4)  # indent для красивого форматирования

    # Сохраняем в Json
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

# Основная функция(необязательна)
def main():

    save_data_to_csv()
    match menu():
        case 1:

            print(save_data_to_json())
        case 2:
            save_data_to_csv()

main()
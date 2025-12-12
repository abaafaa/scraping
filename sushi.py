import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

categories = {
    "Десерты": "https://sushi-storm.ru/sushi_storm_deserty/",
    "Роллы": "https://sushi-storm.ru/sushi_storm_rolly/",
    "Пицца": "https://sushi-storm.ru/sushi_storm_picca/",
    "Наборы и сеты": "https://sushi-storm.ru/sushi_storm_nabory_sety/",
    "Суши": "https://sushi-storm.ru/sushi_storm_sushi/",
    "Горячие блюда": "https://sushi-storm.ru/sushi_storm_goryachie_blyuda/",
    "Детям": "https://sushi-storm.ru/detyam/",
    "Салаты": "https://sushi-storm.ru/sushi_storm_salaty/",
    "Супы": "https://sushi-storm.ru/sushi_storm_supy/",
    "Гарниры": "https://sushi-storm.ru/sushi_storm_garniry/",
    "Соусы": "https://sushi-storm.ru/sushi_storm_sousy/",
    "Напитки": "https://sushi-storm.ru/sushi_storm_napitki/"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

data = []

for cat_name, cat_url in categories.items():
    print(f"Парсим категорию: {cat_name} — {cat_url}")
    resp = requests.get(cat_url, headers=headers)
    soup = BeautifulSoup(resp.text, "lxml")

    # 👉 правильный CSS селектор
    products = soup.select("div.row.products_category div.product-layout")

    print(f"Найдено товаров: {len(products)}")

    for prod in products:
        try:
            name = prod.select_one("h4 a span").get_text(strip=True)

            link = prod.select_one("h4 a")["href"]

            img_tag = prod.select_one("div.image img")
            img_url = img_tag["src"] if img_tag else ""

            desc_tag = prod.select_one("div.short_description")
            desc_text = desc_tag.get_text(strip=True) if desc_tag else ""

            price_tag = prod.select_one("span[class*='price_no_format']")
            price_text = price_tag.get_text(strip=True) if price_tag else ""

            data.append({
                "Категория": cat_name,
                "Название": name,
                "Цена": price_text,
                "Описание": desc_text,
                "Ссылка на товар": link,
                "Ссылка на фото": img_url
            })

        except Exception as e:
            print("Ошибка:", e)

    time.sleep(1.2)

df = pd.DataFrame(data)
df.to_excel("sushi_storm_products.xlsx", index=False)

print("✔ Парсинг завершён! Файл создан: sushi_storm_products.xlsx")

import requests
from bs4 import BeautifulSoup
import pandas as pd

# ฟังก์ชันดึงข้อมูลจากแต่ละหน้าเว็บ
def scrape_recipe(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    print(response)
    if response.status_code != 200:
        print(f"❌ ไม่สามารถเข้าถึง {url}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # ดึงชื่อเมนู
    title_element = soup.find("h1", class_="entry-title")
    title = title_element.text.strip() if title_element else "ไม่พบชื่อเมนู"

    # ดึงส่วนผสม (จาก <ul> tag)
    ingredients_list = soup.select("ul li")
    ingredients = [item.text.strip() for item in ingredients_list if item.text.strip()]

    # ดึงวิธีทำ (จาก <p> tag)
    instructions_list = soup.select("p")
    instructions = [step.text.strip() for step in instructions_list if step.text.strip()]

    # รวมข้อมูลเป็น Dictionary
    recipe = {
        "title": title,
        "ingredients": ", ".join(ingredients),
        "instructions": " ".join(instructions),
        "url": url
    }
    return recipe

# ลิสต์ URL สูตรอาหารที่ต้องการดึงข้อมูล
recipe_urls = [
    "https://nlovecooking.com/ต้มยำกุ้ง/",
    "https://nlovecooking.com/ผัดกะเพรา/"
]

# เก็บข้อมูลทั้งหมด
recipes_data = []

# ดึงข้อมูลจากทุกหน้าเว็บ
for url in recipe_urls:
    recipe = scrape_recipe(url)
    if recipe:
        recipes_data.append(recipe)

# แปลงข้อมูลเป็น DataFrame
df = pd.DataFrame(recipes_data)

# บันทึกเป็น CSV
df.to_csv("recipes_dataset.csv", index=False, encoding="utf-8-sig")

# บันทึกเป็น JSON
df.to_json("recipes_dataset.json", orient="records", indent=4, force_ascii=False)

print("✅ ดึงข้อมูลสำเร็จ! บันทึกเป็น `recipes_dataset.csv` และ `recipes_dataset.json`")

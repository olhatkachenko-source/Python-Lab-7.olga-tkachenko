import matplotlib.pyplot as plt
import numpy as np
import requests
import csv

indicator = "SP.DYN.LE00.IN"  # Код показника: Очікувана тривалість життя
country1 = "Ukraine"
code1 = "ua"

print("=== ПРАКТИЧНА РОБОТА 7. ВІЗУАЛІЗАЦІЯ ДАНИХ (ВАРІАНТ 19) ===")
# Введення назви другої країни користувачем із клавіатури
country2 = input("Введіть назву другої країни англійською (наприклад, United States, Poland, Germany): ").strip()
if not country2:
    country2 = "United States"

# Автоматичне визначення коду країни для API Всесвітнього банку
c_lower = country2.lower()
if "united states" in c_lower or "usa" in c_lower:
    code2 = "us"
elif "poland" in c_lower:
    code2 = "pl"
elif "germany" in c_lower:
    code2 = "de"
elif "france" in c_lower:
    code2 = "fr"
else:
    code2 = "us"
    сл_зниження = "us"  # за замовчуванням США

# Формування URL-адрес для запитів до API Всесвітнього банку за 1991–2019 роки
url1 = f"https://api.worldbank.org/v2/country/{code1}/indicator/{indicator}?date=1991:2019&format=json&per_page=100"
url2 = f"https://api.worldbank.org/v2/country/{code2}/indicator/{indicator}?date=1991:2019&format=json&per_page=100"

# Обробка можливих помилок за допомогою конструкції try-except
try:
    # Отримання даних для України
    response1 = requests.get(url1, timeout=10)
    response1.raise_for_status()
    data1 = response1.json()

    ukraine_data = {}
    if len(data1) > 1 and data1[1]:
        for item in data1[1]:
            if item["value"] is not None:
                ukraine_data[int(item["date"])] = float(item["value"])

    # Отримання даних для другої країни
    response2 = requests.get(url2, timeout=10)
    response2.raise_for_status()
    data2 = response2.json()

    country2_data = {}
    if len(data2) > 1 and data2[1]:
        for item in data2[1]:
            if item["value"] is not None:
                country2_data[int(item["date"])] = float(item["value"])

    # Перевірка наявності даних
    common_years = sorted(list(set(ukraine_data.keys()).intersection(set(country2_data.keys()))))
    
    if not common_years:
        print("Помилка: Не вдалося знайти спільні дані для обраних країн.")
        exit()

    years = np.array(common_years)
    ukraine_vals = np.array([ukraine_data[yr] for yr in common_years])
    country2_vals = np.array([country2_data[yr] for yr in common_years])

    # Збереження отриманих даних у CSV-файл (як вимагається в завданні)
    filename = "lab7.csv"
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Country", "Year", "Life Expectancy"])
        for yr, val in zip(years, ukraine_vals):
            writer.writerow([country1, yr, val])
        for yr, val in zip(years, country2_vals):
            writer.writerow([country2, yr, val])
    print(f"Дані успішно завантажено та збережено у файл '{filename}'.\n")

    # Лінійний графік динаміки показника 
    plt.figure(figsize=(10, 5))
    plt.plot(years, ukraine_vals, label=country1, marker='o', color='blue')
    plt.plot(years, country2_vals, label=country2, marker='s', color='orange')
    plt.title(f'Динаміка очікуваної тривалості життя: {country1} та {country2}', fontsize=14)
    plt.xlabel('Рік', fontsize=12)
    plt.ylabel('Тривалість життя (років)', fontsize=12)
    plt.legend()
    plt.grid(True)
    plt.show()

    # Стовпчаста діаграма порівняння за роками 
    x = np.arange(len(years))
    width = 0.35

    plt.figure(figsize=(12, 6))
    plt.bar(x - width/2, ukraine_vals, width, label=country1, color='skyblue')
    plt.bar(x + width/2, country2_vals, width, label=country2, color='coral')
    plt.title(f'Порівняння показника для {country1} та {country2} за роками', fontsize=14)
    plt.xlabel('Рік', fontsize=12)
    plt.ylabel('Тривалість життя (років)', fontsize=12)
    plt.xticks(x, years, rotation=45)
    plt.legend()
    plt.grid(True, axis='y')
    plt.tight_layout()
    plt.show()

    # Кругова діаграма порівняння за обраний рік 
    print(f"Доступні роки для кругової діаграми: від {years[0]} до {years[-1]}")
    target_year_input = input("Введіть рік для побудови кругової діаграми: ").strip()
    
    while not target_year_input.isdigit() or int(target_year_input) not in years:
        target_year_input = input("Невірний рік. Введіть рік повторно з наявного діапазону: ").strip()
        
    target_year = int(target_year_input)
    idx = np.where(years == target_year)[0][0]

    pie_data = np.array([ukraine_vals[idx], country2_vals[idx]])
    pie_labels = np.array([country1, country2])

    def func(pct, allvals):
        absolute = np.round(pct / 100 * np.sum(allvals), 2)
        return f"{pct:.1f}%\n({absolute} р.)"

    plt.figure(figsize=(6, 6))
    plt.pie(
        pie_data,
        labels=pie_labels,
        autopct=lambda pct: func(pct, pie_data),
        colors=['skyblue', 'coral']
    )
    plt.title(f'Порівняння тривалості життя за {target_year} рік', fontsize=14)
    plt.show()

except requests.exceptions.RequestException as e:
    print(f"Помилка мережевого запиту до API: {e}")
except FileNotFoundError:
    print("Помилка: Файл не знайдено під час збереження/читання.")
except Exception as e:
    print(f"Сталася непередбачена помилка: {e}")

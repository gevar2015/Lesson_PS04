from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


def get_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Запуск в фоновом режиме
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    return driver


def search_wikipedia(driver, query):
    driver.get("https://ru.wikipedia.org/")
    search_box = driver.find_element(By.NAME, "search")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)


def list_paragraphs(driver):
    paragraphs = driver.find_elements(By.TAG_NAME, "p")
    for i, paragraph in enumerate(paragraphs):
        print(f"Параграф {i + 1}: {paragraph.text}\n")
        if i % 5 == 4:  # Показывать по 5 параграфов за раз
            cont = input("Продолжить листать параграфы? (да/нет): ").strip().lower()
            if cont != 'да':
                break


def list_links(driver):
    links = driver.find_elements(By.XPATH, "//div[@id='bodyContent']//a[@href]")
    for i, link in enumerate(links):
        print(f"{i + 1}. {link.text} ({link.get_attribute('href')})")
    return links


def main():
    driver = get_driver()
    while True:
        query = input("Введите ваш первоначальный запрос: ").strip()
        search_wikipedia(driver, query)

        while True:
            action = input("Выберите действие (1: Листать параграфы, 2: Перейти на связанную страницу): ").strip()
            if action == '1':
                list_paragraphs(driver)
            elif action == '2':
                links = list_links(driver)
                link_choice = int(input("Введите номер ссылки для перехода: ").strip()) - 1
                if 0 <= link_choice < len(links):
                    driver.get(links[link_choice].get_attribute('href'))
                else:
                    print("Неверный выбор, попробуйте снова.")
            else:
                print("Неверное действие, попробуйте снова.")

            cont = input("Хотите продолжить с текущей статьей? (да/нет): ").strip().lower()
            if cont != 'да':
                break

        end = input("Хотите завершить сеанс? (да/нет): ").strip().lower()
        if end == 'да':
            break

    driver.quit()


if __name__ == "__main__":
    main()

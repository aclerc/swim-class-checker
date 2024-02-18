from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


def get_url() -> str:
    return (
        r"https://traffordleisure.courseprogress.co.uk/onlinejoining/classes-results?filter=%7B%22centre%22:5,"
        r"%22courseGroupCategory%22:%5B1%5D,%22showFullCourses%22:true,%22dayOfWeek%22:%5B6%5D%7D"
    )


def get_elements(url: str) -> list[WebElement]:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    return WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_all_elements_located((By.CLASS_NAME, "my-4")),
    )


def get_search_conditions() -> tuple[str, str]:
    return "Swim Well - Stage 1", "Saturday 08:30 - 09:00"

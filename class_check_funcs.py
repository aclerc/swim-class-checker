from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from platform_funcs import check_platform


def get_url() -> str:
    return (
        r"https://traffordleisure.courseprogress.co.uk/onlinejoining/classes-results?filter=%7B%22centre%22:5,"
        r"%22courseGroupCategory%22:%5B1%5D,%22showFullCourses%22:true,%22dayOfWeek%22:%5B6%5D%7D"
    )


def get_elements(url: str) -> list[WebElement]:
    plfrm = check_platform()
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")

    if plfrm == "Windows":
        driver = webdriver.Chrome(options=options)
    elif plfrm == "Raspberry Pi":
        browser_driver = Service("/usr/lib/chromium-browser/chromedriver")
        driver = webdriver.Chrome(service=browser_driver, options=options)
    else:
        msg = "Unsupported platform"
        raise RuntimeError(msg)

    driver.get(url)
    return WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_all_elements_located((By.CLASS_NAME, "my-4")),
    )


def get_search_conditions() -> tuple[str, list[str]]:
    return "Swim Well - Stage 1", ["Saturday 07:", "Saturday 08:", "Saturday 09:00"]

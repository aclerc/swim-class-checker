from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from class_check_funcs import get_elements, get_search_conditions, get_url
from email_funcs import send_email


def check_course_availability() -> None:
    url = get_url()
    elements = get_elements(url)
    element_found = False
    target_title, target_time = get_search_conditions()
    for element in elements:
        try:
            title_element = element.find_element(By.CSS_SELECTOR, "p.text-primary.fs-21.font-weight-bold")
            time_element = element.find_element(By.CLASS_NAME, "font-weight-bold.m-0")
            if title_element.text == target_title and time_element.text == target_time:
                print("Found matching element:")
                print("Title:", title_element.text)
                print("Time:", time_element.text)
                places_left_element = element.find_element(By.CSS_SELECTOR, ".ml-md-auto.text-md-right")
                print(f"Places left: {places_left_element.text}")
                element_found = True
                break
        except NoSuchElementException:
            continue
    if not element_found:
        print("WARNING: did not find the class")
        send_email(
            "Course Not Found",
            f"Uh oh! The course was not found on the webpage: {target_title} {target_time}\n\n{url}",
        )
    elif places_left_element.text != "0 out of 10":
        send_email(
            f"Yay! Space available {target_title} {target_time}",
            f"{places_left_element.text} for {target_title} {target_time}\n\n{url}",
        )


if __name__ == "__main__":
    check_course_availability()

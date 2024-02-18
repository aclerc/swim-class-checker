import datetime
import random

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from class_check_funcs import get_elements, get_search_conditions, get_url
from email_funcs import send_email


def daily_subject() -> str:
    r = random.randint(1, 10)
    if r > 6:
        x = "botties"
    elif r == 3:
        x = "botty"
    else:
        x = "bum"

    y = "toast"
    r = random.randint(1, 14)
    # match r to various foods
    match r:
        case 1:
            y = "crumpet"
        case 2:
            y = "toast"
        case 3:
            y = "scone"
        case 4:
            y = "biscuit"
        case 5:
            y = "arpshires"
        case 6:
            y = "sweeze"
        case 7:
            y = "bish bingers"
        case 8:
            y = "poo"
        case 9:
            y = "egg"
        case 10:
            y = "pancake"
    r = random.randint(1, 10)
    if r == 10:
        x, y = y, x
    return f"{x} on {y}"


def send_daily_summary_email() -> None:
    url = get_url()
    elements = get_elements(url)
    target_title, target_time = get_search_conditions()
    matching_titles = []
    matching_times = []
    matching_places_left = []
    for element in elements:
        try:
            title_element = element.find_element(By.CSS_SELECTOR, "p.text-primary.fs-21.font-weight-bold")
            time_element = element.find_element(By.CLASS_NAME, "font-weight-bold.m-0")
            if title_element.text == target_title and time_element.text == target_time:
                places_left_element = element.find_element(By.CSS_SELECTOR, ".ml-md-auto.text-md-right")
                matching_titles.append(title_element.text)
                matching_times.append(time_element.text)
                matching_places_left.append(places_left_element.text)
        except NoSuchElementException:
            continue

    # get day of week

    msg = f"happy {datetime.datetime.now().strftime('%A')}!"
    if not matching_titles:
        msg += "\n\n I am happily running but I have not found any classes matching these criteria:\n\n"
        msg += f"title: {target_title}\ntime: {target_time}\n\n"
        msg += f"Here is the URL I am checking: {url}"
    else:
        msg += (
            "\n\nIf you are getting this email it means I will (probably) be checking these classes for you today:\n\n"
        )
        for title, time, places in zip(matching_titles, matching_times, matching_places_left, strict=False):
            msg += f"title: {title}\ntime: {time}\nplaces left: {places}\n\n"
    send_email(daily_subject(), msg, "DAILY_EMAIL_RECIPIENTS")


if __name__ == "__main__":
    send_daily_summary_email()

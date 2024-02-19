import datetime
import secrets
import time

import pytz
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from class_check_funcs import get_elements, get_search_conditions, get_url
from email_funcs import get_secrets_dict, send_email


def daily_subject() -> str:
    r = secrets.randbelow(10)
    if r > 6:
        x = "botties"
    elif r == 3:
        x = "botty"
    else:
        x = "bum"

    r = secrets.randbelow(10)
    if r == 3:
        x = "cheesy " + x
    if r > 8:
        x = "smelly " + x

    y = "toast"
    r = secrets.randbelow(10)
    match r:
        case 1:
            y = "crumpet"
        case 2:
            y = "toast"
        case 3:
            y = "a chinese"
        case 4:
            y = "burnt toast"
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
        case 0:
            y = "pancake"
    r = secrets.randbelow(10)
    if r == 7:
        x, y = y, x
    return f"{x} on {y}"


def send_daily_summary_email() -> None:
    url = get_url()
    elements = get_elements(url)
    target_title, target_times = get_search_conditions()
    matching_titles = []
    matching_times = []
    matching_places_left = []
    for element in elements:
        try:
            title_element = element.find_element(By.CSS_SELECTOR, "p.text-primary.fs-21.font-weight-bold")
            time_element = element.find_element(By.CLASS_NAME, "font-weight-bold.m-0")
            if target_title.lower() in title_element.text.lower() and any(
                (time_element.text.lower().startswith(x.lower()) for x in target_times),
            ):
                places_left_element = element.find_element(By.CSS_SELECTOR, ".ml-md-auto.text-md-right")
                matching_titles.append(title_element.text)
                matching_times.append(time_element.text)
                matching_places_left.append(places_left_element.text)
        except NoSuchElementException:
            continue
    msg = f"happy {datetime.datetime.now(pytz.timezone('Europe/London')).strftime('%A').lower()}!\n\n"
    if not matching_titles:
        msg += "I am happily running but I have not found any swimming classes matching these criteria:\n"
        for target_time in target_times:
            msg += f"title: {target_title}\ntime: {target_time}"
        msg += f"here is the URL I am checking:\n {url}"
    else:
        msg += "if you are getting this email it means I will (probably) be checking these classes for you today:\n\n"
        for title, time, places in zip(matching_titles, matching_times, matching_places_left, strict=False):
            msg += f"title: {title}\ntime: {time}\nplaces left: {places}\n\n"

    msg += "when I find more than 0 places I will send an email to:\n"
    secrets_dict = get_secrets_dict()
    msg += str(secrets_dict["CHECK_EMAIL_RECIPIENTS"]).replace(",", "\n")
    r = secrets.randbelow(3)
    if r == 1:
        pseudonym = "Isaac's favourite uncle"
    elif r == 2:
        pseudonym = "uncle Jenny's husband"
    else:
        pseudonym = "your legendary bro-in-law"
    msg += f"\nif this does not look right please contact {pseudonym}"
    send_email(daily_subject(), msg, "DAILY_EMAIL_RECIPIENTS")


if __name__ == "__main__":
    time.sleep(secrets.randbelow(120))
    print(f"\n\n{datetime.datetime.now(pytz.timezone('Europe/London'))}")
    print(f"running {__file__}...")
    send_daily_summary_email()

import datetime
import secrets
import time

import pytz
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from class_check_funcs import get_elements, get_search_conditions, get_url
from email_funcs import send_email


def check_for_course_places() -> None:
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
    if not matching_titles:
        send_email(
            "No courses found",
            f"Uh oh! No courses found: target_title={target_title} "
            f"target_times={','.join(target_times)}\n\nurl=\n{url}",
            "ADMIN_RECIPIENTS",
        )
    else:
        msg = f"{len(matching_places_left)} matches found\n"
        for i, places_left in enumerate(matching_places_left):
            print(f"{places_left} for {matching_titles[i]} {matching_times[i]}")
            msg += f"{places_left} for {matching_titles[i]} {matching_times[i]}\n"
            if int(places_left.split(" ")[0]) > 0:
                send_email(
                    f"Yay! place available for {matching_titles[i]} {matching_times[i]}",
                    f"{places_left} for {matching_titles[i]} {matching_times[i]}\n\n{url}",
                    "CHECK_EMAIL_RECIPIENTS",
                )
        if secrets.randbelow(100) == 1:  # PLR2004
            send_email("occasional check_for_places", msg, "ADMIN_RECIPIENTS")


if __name__ == "__main__":
    time.sleep(secrets.randbelow(120))
    print(f"\n\n{datetime.datetime.now(pytz.timezone('Europe/London'))}")
    print(f"running {__file__}...")
    check_for_course_places()

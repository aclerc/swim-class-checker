import smtplib
from email.mime.text import MIMEText

from dotenv import dotenv_values
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


def send_email(subject: str, message: str) -> None:
    recipient_emails = ["ajclerc@gmail.com", "katie.hancock@hotmail.co.uk"]
    sender_email = "swimming.checker@gmail.com"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = "swimming.checker@gmail.com"
    secrets = dotenv_values(".env")
    smtp_password = str(secrets["SMTP_PASSWORD"])

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = ", ".join(recipient_emails)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, recipient_emails, msg.as_string())


def check_course_availability() -> None:
    url = (
        r"https://traffordleisure.courseprogress.co.uk/onlinejoining/classes-results?filter=%7B%22centre%22:5,"
        r"%22courseGroupCategory%22:%5B1%5D,%22showFullCourses%22:true,%22dayOfWeek%22:%5B6%5D%7D"
    )
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    elements = WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_all_elements_located((By.CLASS_NAME, "my-4")),
    )
    element_found = False
    target_title = "Swim Well - Stage 1"
    target_time = "Saturday 08:30 - 09:00"
    for element in elements:
        try:
            title_element = element.find_element(By.CSS_SELECTOR, "p.text-primary.fs-21.font-weight-bold")
            time_element = element.find_element(By.CLASS_NAME, "font-weight-bold.m-0")
            # if title_element.text == "Swim Well - Stage 1" and time_element.text == "Saturday 08:30 - 09:00":
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

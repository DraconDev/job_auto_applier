import json
import math
import os
import random
import re
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

DOWNLOAD_FOLDER = "E:\\_DL\\"
LINK = "https://www.linkedin.com/jobs/search/?currentJobId=3508072244&f_AL=true&f_TPR=r2592000&f_WT=2&geoId=101165590&keywords=full%20stack%20developer&location=United%20Kingdom&refresh=true"


def setup_Chrome(folder=DOWNLOAD_FOLDER):
    chrome_options = Options()
    chrome_options.add_experimental_option(
        "prefs",
        {
            "download.default_directory": folder,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
        },
    )
    driver = webdriver.Chrome(
        "../../_Tools/webdriver/chromedriver.exe",
        options=chrome_options,
    )
    return driver


def import_email():
    with open("../../_login/_Site/indeed_login.json", "r") as f:
        return [*json.load(f).values()]


def open_site():
    driver = setup_Chrome()
    driver.get(LINK)
    sign_in_button = driver.find_element(
        By.CSS_SELECTOR,
        # "a:contains('Sign in')",
        "div.nav__cta-container > a.nav__button-secondary"
        # "a.nav__button-secondary",
    )
    sign_in_button.click()
    email, password = import_email()

    email_input = driver.find_element(By.ID, "username")
    email_input.send_keys(email)
    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys(password)

    login_button = driver.find_element(
        By.CSS_SELECTOR, "button.btn__primary--large.from__button--floating"
    )
    login_button.click()
    time.sleep(5)

    def click_next(driver, sleep=3):
        time.sleep(random.randint(sleep, sleep * 2))
        driver.find_elements(By.CSS_SELECTOR, "footer > div > button.ember-view")[
            -1
        ].click()

    jobs = driver.find_elements(By.CSS_SELECTOR, "li.jobs-search-results__list-item")

    for item in jobs[7:9]:
        item.click()
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, "button.jobs-apply-button").click()
        for i in range(4):
            successful = driver.find_elements(
                By.CSS_SELECTOR, "button.post-apply-add-skill__footer"
            )
            if successful:
                successful.click()
                break
            else:
                click_next(driver)

        close_window_button = driver.find_element(
            By.CSS_SELECTOR, "button.artdeco-modal__dismiss"
        )
        close_window_button.click()

        dismiss_button = driver.find_elements(
            By.CSS_SELECTOR, "button.artdeco-modal__confirm-dialog-btn"
        )[0]
        dismiss_button.click()
        time.sleep(2)

    time.sleep(3000)
    return

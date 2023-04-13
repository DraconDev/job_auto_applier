from selenium.common.exceptions import NoSuchElementException
import json
import os
import random
import re
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

DOWNLOAD_FOLDER = "E:\\_DL\\"
# monthly
LINK = "https://www.linkedin.com/jobs/search/?currentJobId=3508072244&f_AL=true&f_TPR=r2592000&f_WT=2&geoId=101165590&keywords=full%20stack%20developer&location=United%20Kingdom&refresh=true"

# Daily 50
# LINK = "https://www.linkedin.com/jobs/search/?currentJobId=3556250799&f_AL=true&f_TPR=r86400&f_WT=2&geoId=101165590&keywords=full%20stack%20developer&location=United%20Kingdom&refresh=true&count=50&start=0"


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
    with open("../../_Login/_Site/indeed_login.json", "r") as f:
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
    time.sleep(10)

    def click_next(driver, sleep=2):
        time.sleep(random.randint(sleep, sleep * 2))
        footers_buttons = driver.find_elements(
            By.CSS_SELECTOR, "footer > div > button.ember-view"
        )
        if len(footers_buttons) > 0:
            footers_buttons[-1].click()

    jobs = driver.find_elements(By.CSS_SELECTOR, "li.jobs-search-results__list-item")

    for item in jobs[29:48]:
        item.click()
        time.sleep(2)

        try:
            apply = driver.find_element(By.CSS_SELECTOR, "button.jobs-apply-button")
        except NoSuchElementException:
            apply = False

        if apply:
            apply.click()
            for i in range(4):
                button_elements = driver.find_elements(By.XPATH, "//button/span")
                successful = [
                    button_element.text == "Done " for button_element in button_elements
                ]
                # successful = driver.find_elements(By.XPATH, "//button[@value='Done']")

                if not successful:
                    click_next(driver)
                else:
                    break

                # if successful:
                #     click_next(driver)
                #     # successful.click()
                #     time.sleep(3)
                #     driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
                #     break
                # else:
                #     click_next(driver)

            close_window_button = driver.find_element(
                By.CSS_SELECTOR, "button.artdeco-modal__dismiss"
            )
            close_window_button.click()

            try:
                dismiss_button = driver.find_elements(
                    By.CSS_SELECTOR, "button.artdeco-modal__confirm-dialog-btn"
                )
            except NoSuchElementException:
                dismiss_button = False
            if dismiss_button:
                dismiss_button[0].click()

    time.sleep(3000)
    return

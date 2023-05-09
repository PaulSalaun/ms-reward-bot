from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def page_load(driver: WebDriver):
    wait = WebDriverWait(driver, 60)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))


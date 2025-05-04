import string
import random

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

url_steam = "https://store.steampowered.com/"
TIMEOUT = 10

visibl_el_page_1 = (By.ID, "home_featured_and_recommended")
visibl_el_page_log = (By.XPATH, "//*[text()='Вход']")
button_clc = (By.XPATH, "//*[@id ='global_actions']//a[text()='войти']")
login_input = (By.XPATH, "//*[@id='responsive_page_template_content']//input[@type = 'text']")
password_input = (By.XPATH, "//*[@id='responsive_page_template_content']//input[@type = 'password']")
clc_login = (By.XPATH, "//*[@id='responsive_page_template_content']//button[@type = 'submit']")
loadin_button = (By.XPATH, "//*[@id='responsive_page_template_content']//button//div[@class]")
error_message = (By.XPATH, "//*[contains(text(), 'проверьте')]")


def random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


class TestSteamLoginSuite:
    def test_login_with_invalid_credential(self, browser):
        browser.get(url_steam)
        WebDriverWait(browser, TIMEOUT).until(
            EC.visibility_of_element_located(visibl_el_page_1)) # проверка открытия страницы
        WebDriverWait(browser, TIMEOUT).until(
            EC.element_to_be_clickable(button_clc)).click()
        WebDriverWait(browser, TIMEOUT).until(
            EC.visibility_of_element_located(visibl_el_page_log))  # проверка загрузки стр
        login = random_string()
        password = random_string()
        browser.find_element(*login_input).send_keys(login)
        browser.find_element(*password_input).send_keys(password)
        browser.find_element(*clc_login).click()
        loading = WebDriverWait(browser, TIMEOUT).until(
            EC.visibility_of_element_located(loadin_button)
        )
        assert loading.is_displayed(), "Loading indicator is not displayed after submit"

        error_elem = WebDriverWait(browser, TIMEOUT).until(
            EC.visibility_of_element_located(error_message))
        error_text = error_elem.text.lower()
        assert "проверьте свой пароль и имя аккаунта" in error_text.lower(), (
            f"Expected error message to contain 'проверьте', but got: '{error_text}'"
        )

from faker import Faker

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

url_steam = "https://store.steampowered.com/"
TIMEOUT = 10

VISIBL_EL_PAGE_1 = (By.ID, "home_featured_and_recommended")
VISIBL_EL_PAGE_LOG = (By.XPATH, "//*[text()='Вход']")
BUTTON_CLC = (By.XPATH, "//*[@id ='global_actions']//a[text()='войти']")
LOGIN_INPUT = (By.XPATH, "//*[@id='responsive_page_template_content']//input[@type = 'text']")
PASSWORD_INPUT = (By.XPATH, "//*[@id='responsive_page_template_content']//input[@type = 'password']")
CLC_LOGIN = (By.XPATH, "//*[@id='responsive_page_template_content']//button[@type = 'submit']")
LOADIN_BUTTON = (By.XPATH, "//*[@id='responsive_page_template_content']//button//div[@class]")
ERROR_MESSAGE = (By.XPATH, "//*[contains(text(), 'проверьте')]")

fake = Faker()


class TestSteamLogin:
    def test_login_with_invalid_credential(self, browser):
        browser.get(url_steam)
        WebDriverWait(browser, TIMEOUT).until(
            EC.visibility_of_element_located(VISIBL_EL_PAGE_1))  # проверка открытия страницы
        WebDriverWait(browser, TIMEOUT).until(
            EC.element_to_be_clickable(BUTTON_CLC)).click()
        WebDriverWait(browser, TIMEOUT).until(
            EC.visibility_of_element_located(VISIBL_EL_PAGE_LOG))  # проверка загрузки стр
        login = fake.user_name()
        password = fake.password()
        login_input = WebDriverWait(browser, TIMEOUT).until(
            EC.visibility_of_element_located(LOGIN_INPUT))
        login_input.send_keys(login)
        password_input = WebDriverWait(browser, TIMEOUT).until(
            EC.visibility_of_element_located(PASSWORD_INPUT))
        password_input.send_keys(password)
        WebDriverWait(browser, TIMEOUT).until(
            EC.element_to_be_clickable(CLC_LOGIN)).click()
        loading = WebDriverWait(browser, TIMEOUT).until(
            EC.visibility_of_element_located(LOADIN_BUTTON)
        )
        assert loading.is_displayed(), "Loading indicator is not displayed after submit"

        error_elem = WebDriverWait(browser, TIMEOUT).until(
            EC.visibility_of_element_located(ERROR_MESSAGE))
        error_text = error_elem.text.lower()
        assert "проверьте свой пароль и имя аккаунта и попробуйте снова" in error_text.lower(), (
            f"Expected error message to contain 'проверьте', but got: '{error_text}'"
            # я сдаюсь, я не знаю к какому локатору привязаться, чтоб не было "проверьте"
        )

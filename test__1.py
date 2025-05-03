import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By



@pytest.fixture(scope="function")  # фикстура для открытия
def browser():
    browser = webdriver.Chrome()
    yield browser
    browser.quit()  # и закрытия браузера


class TestPage():

    def test_steam(self, browser):
        browser.get("https://store.steampowered.com/")
        browser.implicitly_wait(10)
        button_clc = browser.find_element(By.XPATH, "//*[@id ='global_actions']//a[text()='войти']")
        button_clc.click()
        login_input = browser.find_element(By.XPATH,
                                           "//*[@id='responsive_page_template_content']//input[@type = 'text']")
        login_input.send_keys("Sofia")
        password_input = browser.find_element(By.XPATH,
                                              "//*[@id='responsive_page_template_content']//input[@type = 'password']")
        password_input.send_keys("dshbfhsbjhz")
        browser.find_element(By.XPATH, "//*[@id='responsive_page_template_content']//button[@type = 'submit']").click()
        loadin_button = browser.find_element(By.XPATH,
                                             "//*[@id='responsive_page_template_content']//button/div[@class]")
        assert loadin_button.is_displayed()
        error_message = browser.find_element(By.XPATH, "//*[contains(text(), 'проверьте')]")
        assert 'проверьте' in error_message.text.lower()

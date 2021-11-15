from datetime import time
import glob, os
import time
from selenium import webdriver
import unittest


# chrome 90

class TestSelenium(unittest.TestCase):

    def setUp(self) -> None:
        self.driver= webdriver.Chrome('chromedriver.exe')
        time.sleep(5)
    def test_niepoprawna_rejestracja(self):
        user = 'Nowy10'
        password = 'P'
        email = user + '@gmail.com'
        print('start niepoprawnej rejestracji')
        self.driver.get('http://127.0.0.1:5000/register')
        #wypełnienie rejestracji

        self.driver.find_element_by_css_selector(
            'body > main > div > div > div.content-section > form > fieldset > div:nth-child(2) > #username')\
            .send_keys(user)
        self.driver.find_element_by_css_selector(
            'body > main > div > div > div.content-section > form > fieldset > div:nth-child(3) > #email') \
            .send_keys(email)
        self.driver.find_element_by_css_selector(
            'body > main > div > div > div.content-section > form > fieldset > div:nth-child(4) > #password') \
            .send_keys(password)
        self.driver.find_element_by_css_selector(
            'body > main > div > div > div.content-section > form > fieldset > div:nth-child(5) > #confirm_password') \
            .send_keys(password+'a')
        #klikniecie przycisku
        Btn = self.driver.find_element_by_css_selector('body > main > div > div > div.content-section > form > div > #submit')
        Btn.click()
        print('Nipoprawna rejestracja przebiegła pomyślnie')
        # sprawdzanie czy wystąpił błąd
        UserIsInDB = self.driver.find_element_by_css_selector(
            "body > main > div > div > div.content-section > form > fieldset > div:nth-child(2) > div > span").text
        emailIsInDB = self.driver.find_element_by_css_selector(
            "body > main > div > div > div.content-section > form > fieldset > div:nth-child(3) > div > span").text
        passIsInDB = self.driver.find_element_by_css_selector(
            "body > main > div > div > div.content-section > form > fieldset > div:nth-child(4) > div > span").text
        confirm_passwordIsInDB = self.driver.find_element_by_css_selector(
            "body > main > div > div > div.content-section > form > fieldset > div:nth-child(5) > div > span").text
        self.assertIn('Użytkownik o tym nicku istnieje!', UserIsInDB)
        self.assertIn('Email już jest użyty!', emailIsInDB)
        self.assertIn('Field must be between 2 and 20 characters long.', passIsInDB)
        self.assertIn('Field must be equal to password.', confirm_passwordIsInDB)

    def tearDown(self):
        self.driver.close()



if __name__ == "__main__":
    unittest.main()








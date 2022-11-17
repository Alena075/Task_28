# python -m pytest -v --driver Chrome --driver-path C:\Driver_for_Selenium\chromedriver.exe tests/test_auth_by_code.py

import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import valid_email, valid_password, valid_password_new, phone, name, surname
from config import no_valid_phone, no_valid_email, no_valid_password_1, no_valid_password_2


@pytest.fixture(autouse=True)
def testing_area():
    pytest.driver = webdriver.Chrome('C:\Driver_for_Selenium\chromedriver.exe')
    pytest.driver.get("https://b2c.passport.rt.ru/")

    yield
    pytest.driver.quit()

def test_01():
    """ Тест 1: Регистрация по корректным почте и паролю """
    pytest.driver.implicitly_wait(7)
    pytest.driver.find_element("xpath", '//*[@id="kc-register"]').click()
    pytest.driver.find_element("xpath", '//*[@id="page-right"]/div/div/div/form/div[1]/div[1]/div/input').send_keys(name)
    pytest.driver.find_element("xpath", '//*[@id="page-right"]/div/div/div/form/div[1]/div[2]/div/input').send_keys(surname)
    pytest.driver.find_element("xpath", '//*[@id="address"]').send_keys(valid_email)
    pytest.driver.find_element("xpath", '//*[@id="password"]').send_keys(valid_password)
    pytest.driver.find_element("xpath", '//*[@id="password-confirm"]').send_keys(valid_password)
    pytest.driver.find_element("xpath", '//*[@id="page-right"]/div/div/div/form/button').click()
    time.sleep(3)

@pytest.mark.xfail(reason="Тест проходит - БАГ!")
def test_02():
    """ Тест 2: Регистрации по некорректной почте и корректному паролю """
    pytest.driver.implicitly_wait(7)
    pytest.driver.find_element("xpath", '//*[@id="kc-register"]').click()
    pytest.driver.find_element("xpath", '//*[@id="page-right"]/div/div/div/form/div[1]/div[1]/div/input').send_keys(name)
    pytest.driver.find_element("xpath", '//*[@id="page-right"]/div/div/div/form/div[1]/div[2]/div/input').send_keys(surname)
    pytest.driver.find_element("xpath", '//*[@id="address"]').send_keys(no_valid_email)
    pytest.driver.implicitly_wait(10)
    pytest.driver.find_element("xpath", '//*[@id="password"]').send_keys(valid_password)
    pytest.driver.find_element("xpath", '//*[@id="password-confirm"]').send_keys(valid_password)
    pytest.driver.find_element("xpath", '//*[@id="page-right"]/div/div/div/form/button').click()
    time.sleep(3)

def test_03():
    """ Тест 3: Восстановление пароля """
    pytest.driver.implicitly_wait(7)
    pytest.driver.find_element("xpath", '//*[@id="forgot_password"]').click()
    pytest.driver.find_element("xpath", '//*[@id="username"]').send_keys(phone)
    text = pytest.driver.find_elements("xpath", '//*[@id="page-right"]/div/div/div/form/div[2]/div[1]/div[1]/img')
    text_captcha = str(text)
    pytest.driver.find_element("xpath", '//*[@id="captcha"]').send_keys(text_captcha)
    pytest.driver.find_element("xpath", '//*[@id="reset"]').click()
    time.sleep(3)

@pytest.mark.xfail(reason="Тест проходит - БАГ!")
def test_04():
    """ Тест 4: Ввести в поле "Подтверждение пароля" не корректный пароль """
    pytest.driver.implicitly_wait(7)
    pytest.driver.find_element("xpath", '//*[@id="kc-register"]').click()
    pytest.driver.find_element("xpath", '//*[@id="page-right"]/div/div/div/form/div[1]/div[1]/div/input').send_keys(name)
    pytest.driver.find_element("xpath", '//*[@id="page-right"]/div/div/div/form/div[1]/div[2]/div/input').send_keys(surname)
    pytest.driver.find_element("xpath", '//*[@id="address"]').send_keys(valid_email)
    pytest.driver.find_element("xpath", '//*[@id="password"]').send_keys(valid_password)
    pytest.driver.find_element("xpath", '//*[@id="password-confirm"]').send_keys(no_valid_password_1)
    pytest.driver.find_element("xpath", '//*[@id="page-right"]/div/div/div/form/button').click()
    time.sleep(3)

def test_05():
    """ Тест 5: При вводе пароля менее 8 символов выдается сообщение: Длина пароля должна быть не менее 8 символов  """
    pytest.driver.implicitly_wait(7)
    pytest.driver.find_element("xpath", '//*[@id="kc-register"]').click()
    pytest.driver.find_element("xpath", '//*[@id="page-right"]/div/div/div/form/div[1]/div[1]/div/input').\
        send_keys(name)
    pytest.driver.find_element("xpath", '//*[@id="page-right"]/div/div/div/form/div[1]/div[2]/div/input').\
        send_keys(surname)
    pytest.driver.find_element("xpath", '//*[@id="address"]').send_keys(valid_email)
    # pytest.driver.find_element("xpath", '//*[@id="address"]').send_keys(phone)
    WebDriverWait(pytest.driver, 5).until(EC.visibility_of_element_located(("xpath", '//*[@id="password"]'))).\
        send_keys(no_valid_password_2)
    WebDriverWait(pytest.driver, 5).until(EC.visibility_of_element_located(("xpath", '//*[@id="password-confirm"]'))).\
        send_keys(no_valid_password_2)
    pytest.driver.find_element("xpath", '//*[@id="page-right"]/div/div/div/form/button').click()
    assert pytest.driver.find_element(By.XPATH,
                                      '//*[@id="page-right"]/div/div/div/form/div[4]/div[1]/span').text == \
           "Длина пароля должна быть не менее 8 символов"
    assert pytest.driver.find_element(By.XPATH,
                                      '//*[@id="page-right"]/div/div/div/form/div[4]/div[2]/span').text == \
           "Длина пароля должна быть не менее 8 символов"
    time.sleep(3)

def test_06():
    """ Тест 6: При вводе пароля без заглавных букв выдается сообщение:
    Пароль должен содержать хотя бы одну заглавную букву  """
    pytest.driver.implicitly_wait(7)
    pytest.driver.find_element("xpath", '//*[@id="kc-register"]').click()
    pytest.driver.find_element("xpath", '//*[@id="page-right"]/div/div/div/form/div[1]/div[1]/div/input').\
        send_keys(name)
    pytest.driver.find_element("xpath", '//*[@id="page-right"]/div/div/div/form/div[1]/div[2]/div/input').\
        send_keys(surname)
    pytest.driver.find_element("xpath", '//*[@id="address"]').send_keys(valid_email)
    # pytest.driver.find_element("xpath", '//*[@id="address"]').send_keys(phone)
    WebDriverWait(pytest.driver, 5).until(EC.visibility_of_element_located(("xpath", '//*[@id="password"]'))).\
        send_keys(no_valid_password_1)
    WebDriverWait(pytest.driver, 5).until(EC.visibility_of_element_located(("xpath", '//*[@id="password-confirm"]'))).\
        send_keys(no_valid_password_1)
    pytest.driver.find_element("xpath", '//*[@id="page-right"]/div/div/div/form/button').click()
    assert pytest.driver.find_element(By.XPATH,
                                      '//*[@id="page-right"]/div/div/div/form/div[4]/div[1]/span').text == \
           "Пароль должен содержать хотя бы одну заглавную букву"
    assert pytest.driver.find_element(By.XPATH,
                                      '//*[@id="page-right"]/div/div/div/form/div[4]/div[2]/span').text == \
           "Пароль должен содержать хотя бы одну заглавную букву"
    time.sleep(3)

def test_07():
    """ Тест 7: При вводе пароля использовалась кириллица и выдается сообщение:
    Пароль должен содержать только латинские буквы  """
    pytest.driver.implicitly_wait(7)
    pytest.driver.find_element("xpath", '//*[@id="kc-register"]').click()
    pytest.driver.find_element("xpath", '//*[@id="page-right"]/div/div/div/form/div[1]/div[1]/div/input').\
        send_keys(name)
    pytest.driver.find_element("xpath", '//*[@id="page-right"]/div/div/div/form/div[1]/div[2]/div/input').\
        send_keys(surname)
    pytest.driver.find_element("xpath", '//*[@id="address"]').send_keys(valid_email)
    # pytest.driver.find_element("xpath", '//*[@id="address"]').send_keys(phone)
    WebDriverWait(pytest.driver, 5).until(EC.visibility_of_element_located(("xpath", '//*[@id="password"]'))).\
        send_keys(no_valid_password_1)
    WebDriverWait(pytest.driver, 5).until(EC.visibility_of_element_located(("xpath", '//*[@id="password-confirm"]'))).\
        send_keys(no_valid_password_1)
    pytest.driver.find_element("xpath", '//*[@id="page-right"]/div/div/div/form/button').click()
    assert pytest.driver.find_element(By.XPATH,
                                      '//*[@id="page-right"]/div/div/div/form/div[4]/div[1]/span').text == \
           "Пароль должен содержать только латинские буквы"
    assert pytest.driver.find_element(By.XPATH,
                                      '//*[@id="page-right"]/div/div/div/form/div[4]/div[2]/span').text == \
           "Пароль должен содержать только латинские буквы"
    time.sleep(3)

def test_08():
    """ Тест 8: Вход в личный кабинет с корректными данными (по почте) """
    pytest.driver.implicitly_wait(7)
    pytest.driver.find_element("xpath", '//*[@id="t-btn-tab-mail"]').click()
    pytest.driver.find_element("xpath", '//*[@id="username"]').send_keys(valid_email)
    pytest.driver.find_element("xpath", '//*[@id="password"]').send_keys(valid_password)
    pytest.driver.find_element("xpath", '//*[@id="page-right"]/div/div/div/form/div[3]/label/span[1]').click()
    pytest.driver.find_element("xpath", '//*[@id="kc-login"]').click()
    time.sleep(3)

def test_09():
    """ Тест 9: Вход в личный кабинет с некорректными данными (по почте) """
    pytest.driver.implicitly_wait(7)
    pytest.driver.find_element("xpath", '//*[@id="t-btn-tab-mail"]').click()
    pytest.driver.find_element("xpath", '//*[@id="username"]').send_keys(no_valid_email)
    pytest.driver.find_element("xpath", '//*[@id="password"]').send_keys(no_valid_password_1)
    pytest.driver.find_element("xpath", '//*[@id="page-right"]/div/div/div/form/div[3]/label/span[1]').click()
    pytest.driver.find_element("xpath", '//*[@id="kc-login"]').click()
    assert pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/p').text == "Неверный логин или пароль"
    time.sleep(3)

def test_10():
    """ Тест 10: Изменение пароля через личный кабинет """
    pytest.driver.implicitly_wait(7)
    pytest.driver.find_element("xpath", '//*[@id="username"]').send_keys(valid_email)
    pytest.driver.find_element("xpath", '//*[@id="password"]').send_keys(valid_password)
    pytest.driver.find_element("xpath", '//*[@id="page-right"]/div/div/div/form/div[3]/label/span[1]').click()
    pytest.driver.find_element("xpath", '//*[@id="kc-login"]').click()
    pytest.driver.find_element("xpath", '//*[@id="password_change"]').click()
    pytest.driver.find_element("xpath", '//*[@id="current_password"]').send_keys(valid_password)
    pytest.driver.find_element("xpath", '//*[@id="new_password"]').send_keys(valid_password_new)
    pytest.driver.find_element("xpath", '//*[@id="confirm_password"]').send_keys(valid_password_new)
    pytest.driver.find_element("xpath", '//*[@id="password_save"]').click()
    time.sleep(3)

def test_11():
    """ Тест 11: Регистрация по корректным телефону и паролю """
    pytest.driver.implicitly_wait(7)
    pytest.driver.find_element("xpath", '//*[@id="kc-register"]').click()
    pytest.driver.find_element("xpath", '//*[@id="page-right"]/div/div/div/form/div[1]/div[1]/div/input').send_keys(name)
    pytest.driver.find_element("xpath", '//*[@id="page-right"]/div/div/div/form/div[1]/div[2]/div/input').send_keys(surname)
    pytest.driver.find_element("xpath", '//*[@id="address"]').send_keys(phone)
    pytest.driver.find_element("xpath", '//*[@id="password"]').send_keys(valid_password)
    pytest.driver.find_element("xpath", '//*[@id="password-confirm"]').send_keys(valid_password)
    pytest.driver.find_element("xpath", '//*[@id="page-right"]/div/div/div/form/button').click()
    time.sleep(3)

def test_12():
    """ Тест 12: Вход в личный кабинет с корректными данными (по телефону) """
    pytest.driver.implicitly_wait(7)
    pytest.driver.find_element("xpath", '//*[@id="t-btn-tab-phone"]').click()
    pytest.driver.find_element("xpath", '//*[@id="username"]').send_keys(phone)
    pytest.driver.find_element("xpath", '//*[@id="password"]').send_keys(valid_password)
    pytest.driver.find_element("xpath", '//*[@id="page-right"]/div/div/div/form/div[3]/label/span[1]').click()
    pytest.driver.find_element("xpath", '//*[@id="kc-login"]').click()
    time.sleep(3)

def test_13():
    """ Тест 13: Вход в личный кабинет с некорректными данными (по телефону) """
    pytest.driver.implicitly_wait(7)
    pytest.driver.find_element("xpath", '//*[@id="t-btn-tab-phone"]').click()
    pytest.driver.find_element("xpath", '//*[@id="username"]').send_keys(no_valid_phone)
    pytest.driver.find_element("xpath", '//*[@id="password"]').send_keys(no_valid_password_1)
    pytest.driver.find_element("xpath", '//*[@id="page-right"]/div/div/div/form/div[3]/label/span[1]').click()
    pytest.driver.find_element("xpath", '//*[@id="kc-login"]').click()
    assert pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/p').text == "Неверный логин или пароль"
    time.sleep(3)

def test_14():
    """ Тест 14: Восстановление пароля при помощи e-mail """
    pytest.driver.implicitly_wait(7)
    pytest.driver.find_element("xpath", '//*[@id="t-btn-tab-mail"]').click()
    pytest.driver.find_element("xpath", '//*[@id="forgot_password"]').click()
    WebDriverWait(pytest.driver, 7).until(EC.visibility_of_element_located((By.ID, "username"))).send_keys(valid_email)
    WebDriverWait(pytest.driver, 7).until(EC.visibility_of_element_located((By.ID, "forgot_password"))).click()
    pytest.driver.get('https://b2c.passport.rt.ru/auth/realms/b2c/login-actions/'
                      'reset-credentials?client_id=account_b2c&tab_id=yO70VJtgeUI')
    WebDriverWait(pytest.driver, 7).until(EC.visibility_of_element_located((By.ID, "username"))).send_keys(valid_email)
    WebDriverWait(pytest.driver, 7).until(EC.visibility_of_element_located((By.ID, "captcha"))).send_keys('*******')
    WebDriverWait(pytest.driver, 7).until(EC.visibility_of_element_located((By.ID, "reset"))).click()
    WebDriverWait(pytest.driver, 7).until(EC.visibility_of_element_located((By.ID, "page-right",
            '/div[1]/div[1]/div[1]/form[1]/div[1]/label[2]/span[1]/span[2]'))).click()
    WebDriverWait(pytest.driver, 7).until(EC.visibility_of_element_located((By.ID, "rt-btn"))).click()
    pytest.driver.get('https://b2c.passport.rt.ru/auth/realms/b2c/login-actions/'
                      'reset-credentials?client_id=account_b2c&tab_')
    WebDriverWait(pytest.driver, 7).until(EC.visibility_of_element_located((By.ID, "password-new"))).send_keys(
        valid_password_new)
    WebDriverWait(pytest.driver, 7).until(EC.visibility_of_element_located((By.ID, "password-confirm"))).send_keys(
        valid_password_new)
    WebDriverWait(pytest.driver, 7).until(EC.visibility_of_element_located((By.ID, "t-btn-reset-pass"))).click()
    time.sleep(3)

def test_15():
    """ Тест 15: Восстановление пароля при помощи телефона """
    pytest.driver.implicitly_wait(7)
    pytest.driver.find_element("xpath", '//*[@id="t-btn-tab-phone"]').click()
    pytest.driver.find_element("xpath", '//*[@id="forgot_password"]').click()
    WebDriverWait(pytest.driver, 7).until(EC.visibility_of_element_located((By.ID, "username"))).send_keys(phone)
    WebDriverWait(pytest.driver, 7).until(EC.visibility_of_element_located((By.ID, "forgot_password"))).click()
    pytest.driver.get('https://b2c.passport.rt.ru/auth/realms/b2c/login-actions/'
                      'reset-credentials?client_id=account_b2c&tab_id=og1zRJVat3M')
    WebDriverWait(pytest.driver, 7).until(EC.visibility_of_element_located((By.ID, "username"))).send_keys(phone)
    WebDriverWait(pytest.driver, 7).until(EC.visibility_of_element_located((By.ID, "captcha"))).send_keys('*******')
    WebDriverWait(pytest.driver, 7).until(EC.visibility_of_element_located((By.ID, "reset"))).click()
    WebDriverWait(pytest.driver, 7).until(EC.visibility_of_element_located((By.ID, "page-right",
                        '/div[1]/div[1]/div[1]/form[1]/div[1]/label[1]/span[1]/span[3]/span[1]'))).click()
    WebDriverWait(pytest.driver, 7).until(EC.visibility_of_element_located((By.ID, "rt-btn"))).click()
    WebDriverWait(pytest.driver, 7).until(EC.visibility_of_element_located((By.ID, "rt-code-0"))).send_keys('******')
    pytest.driver.get('https://b2c.passport.rt.ru/auth/realms/b2c/login-actions/'
                      'reset-credentials?client_id=account_b2c&tab_id=og1zRJVat3M')
    WebDriverWait(pytest.driver, 7).until(EC.visibility_of_element_located((By.ID, "password-new"))).send_keys(
        valid_password_new)
    WebDriverWait(pytest.driver, 7).until(EC.visibility_of_element_located((By.ID, "password-confirm"))).send_keys(
        valid_password_new)
    WebDriverWait(pytest.driver, 7).until(EC.visibility_of_element_located((By.ID, "t-btn-reset-pass"))).click()
    time.sleep(3)

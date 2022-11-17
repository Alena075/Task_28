ЗАДАНИЕ 28

В рамках выполнения дипломного проекта необходимо протестировать новый интерфейс авторизации 
в личном кабинете от заказчика Ростелеком Информационные Технологии. 

→ Требования по проекту (.doc)
→ Объект тестирования: https://b2c.passport.rt.ru

Команда для запуска файла с тестами:
python -m pytest -v --driver Chrome --driver-path C:\Driver_for_Selenium\chromedriver.exe tests/test_auth_by_code.py
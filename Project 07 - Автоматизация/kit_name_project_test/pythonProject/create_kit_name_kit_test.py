import sender_stand_request
import data
import requests
import configuration

# Получение token
def get_user_token():
    return requests.post(configuration.URL_SERVICE + configuration.CREATE_USER_PATH,
                         json=data.user_body,
                         headers=data.headers
                         )
response_token = get_user_token()
data.auth_token["Authorization"] = "Bearer " + response_token.json()["authToken"]

# Функция изменения значения name в теле запроса
def get_kit_body(name):
    # Копируется словарь с телом запроса из data
    current_body = data.kit_body.copy()
    # Изменение значения в поле name
    current_body["name"] = name
    # Возвращается новый словарь с новым значением name
    return current_body

# Функция для позитивной проверки
def positive_assert(name):
    # Сохраняем новое тело запроса в переменную kit_body
    kit_body = get_kit_body(name)
    # Сохраняем результат запроса на создание набора в переменную kit_respons:
    kit_respons = sender_stand_request.post_new_client(kit_body, data.auth_token)
    # Проверяется, что код ответа равен 201
    assert kit_respons.status_code == 201
    # Проверяется, что в ответе есть не пустое поле name
    assert kit_respons.json()["name"] == name

#Функция для негативной проверки
def negative_assert_code_400(kit_body):
    #kit_body = get_kit_body(name)
    response = sender_stand_request.post_new_client(kit_body, data.auth_token)
    assert response.status_code == 400

# Тест 1. Успешное создание набора пользователя
# Параметр name = 1 символ
def test_create_kit_1_letter_in_name_get_success():
    positive_assert("a")

# Тест 2. Успешное создание набора пользователя
# Параметр name = 551 символ
def test_create_kit_511_letter_in_name_get_success():
    positive_assert("Abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd" +
            "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd" +
            "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd" +
            "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdabcdabcdabcdabcdabcd" +
            "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd" +
            "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd" +
            "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabC")

# Тест 3. Не создан набор пользователя:
# Параметр name = 0 символов
def test_create_kit_empty_name_get_error():
    kit_body = get_kit_body("")
    negative_assert_code_400(kit_body)

# Тест 4. Не создан набор пользователя:
# Параметр name = 512 символов
def test_create_kit_512_letter_in_name_get_error():
    kit_body = get_kit_body("Abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd" +
            "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd" +
            "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd" +
            "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdabcdabcdabcdabcdabcd" +
            "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd" +
            "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd" +
            "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcD")
    negative_assert_code_400(kit_body)

# Тест 5. Успешное создание набора пользователя
# Параметр name = английские буквы
def test_create_kit_english_letter_in_name_get_success():
    positive_assert("QWErty")

# Тест 6. Успешное создание набора пользователя
# Параметр name = русские буквы
def test_create_kit_russian_letter_in_name_get_success():
    positive_assert("Мария")

# Тест 7. Успешное создание набора пользователя
# Параметр name = спецсимволы
def test_create_kit_has_special_symbol_in_name_get_success():
    positive_assert("\"№%@\",")

# Тест 8. Успешное создание набора пользователя
# Параметр name = пробелы внутри параметра
def test_create_kit_has_space_in_name_get_success():
    positive_assert("Человек и Ко")

# Тест 9. Успешное создание набора пользователя
# Параметр name = цифры
def test_create_kit_has_number_in_name_get_success():
    positive_assert("123")

# Тест 10. Не создан набор пользователя:
# Параметр name не передан в запросе
def test_create_kit_no_name_get_error():
    kit_body = data.kit_body.copy()
    kit_body.pop("name")
    negative_assert_code_400(kit_body)

# Тест 11. Не создан набор пользователя:
# Передан тип параметра - число:
def test_create_kit_number_type_name_get_error():
    kit_body = get_kit_body(123)
    negative_assert_code_400(kit_body)
import data
import configuration
import requests


# Функция для создания нового набора пользователя
def post_new_client(kit_body, auth_token):
    return requests.post(configuration.URL_SERVICE + configuration.CREATE_USER_KITS,
                         headers=auth_token,
                         json=kit_body
                         )


response = post_new_client(data.kit_body, data.auth_token)
print(response.status_code)
print(response.json())

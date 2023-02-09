import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import json

class PetFriends:
    def __init__(self):
        self.base_url = 'https://petfriends.skillfactory.ru/'

    def get_api_key(self, email, password):
        header = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url + 'api/key', headers=header)
        status = res.status_code
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def get_api_key_for_invalid_user_data(self, email, invalid_password):
        header = {
            'email': email,
            'password': invalid_password
        }
        res = requests.get(self.base_url + 'api/key', headers=header)
        status = res.status_code
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def get_list_of_my_pets(self, auth_key, filter):
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}
        res = requests.get(self.base_url + 'api/pets', headers=headers, params=filter)
        status = res.status_code
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def create_new_pet(self, auth_key: json, name: str, animal_type: str,
                       age: str) -> json:

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result

    def add_photo_to_pet(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        data = MultipartEncoder(
            fields={
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/png')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + '/api/pets/set_photo/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""

        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def delete_pet(self, auth_key: json, pet_id: str) -> json:

        headers = {'auth_key': auth_key['key']}

        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def delete_pet_photo(self, auth_key: json, pet_photo: str) -> json:

        headers = {'auth_key': auth_key['key']}

        res = requests.delete(self.base_url + 'api/pets/' + pet_photo, headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def get_list_of_all_pets(self, auth_key, filter):
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}
        res = requests.get(self.base_url + 'api/pets', headers=headers, params=filter)
        status = res.status_code
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
        """Проверяем возможность обновления информации о питомце"""

        # Получаем ключ auth_key и список своих питомцев
        _, auth_key = pf.get_api_key(valid_email, valid_password)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

        # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
        if len(my_pets['pets']) > 0:
            status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

            # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
            assert status == 200
            assert result['name'] == name
        else:
            # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
            raise Exception("There is no my pets")




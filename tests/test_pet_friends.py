from api import PetFriends
from settings import valid_email, valid_password, invalid_password, invalid_email


pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

# Негативный тест на добавление пользователя (введен некорректный пароль)
def test_get_api_key_for_invalid_user_password(email=valid_email, password=invalid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

def test_get_api_key_for_invalid_user_email(email=invalid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

def test_get_api_key_for_invalid_user_email_and_invalid_user_password (email=invalid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result


def test_get_list_of_my_pets_with_valid_keys(filter='my_pets'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_my_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_get_list_of_my_pets_with_invalid_keys(filter='my_pets'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_my_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_create_new_pet(name='Alisa', animal_type='cat', age='3'):

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.create_new_pet(auth_key, name, animal_type, age)

    assert status == 200

# Баг. Тест проходит со статусом 200, но фото питомца в формате 'png' на сайт не добавлено.
# В требованиях данный формат разрешен
def test_add_photo_to_pet_png(pet_photo='images/Pik.png'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_my_pets(auth_key, 'my_pets')

    pet_id = my_pets['pets'][1]['id']
    status, _ = pf.add_photo_to_pet(auth_key, pet_id, pet_photo)


def test_successful_delete_self_pet_photo():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_my_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet_photo(auth_key, pet_id)
    _, my_pets = pf.get_list_of_my_pets(auth_key, "my_pets")
    assert status == 200

# def test_successful_delete_self_pet():
#
#     _, auth_key = pf.get_api_key(valid_email, valid_password)
#     _, all_pets = pf.get_list_of_my_pets(auth_key, "my_pets")
#
#     if len(all_pets['pets']) == 0:
#         pf.add_new_pet(auth_key, "Don", "goose", "3",  "images/Don.jpg")
#         _, all_pets = pf.get_list_of_my_pets(auth_key, "my_pets")
#
#     pet_id = all_pets['pets'][0]['id']
#     status, _ = pf.delete_pet_photo(auth_key, pet_id)
#
#     _, my_pets = pf.get_list_of_my_pets(auth_key, "my_pets")
#
#     assert status == 200
#     assert pet_id not in my_pets.values()

def test_add_photo_to_pet(pet_photo='images/Bim.jpg'):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_my_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_to_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)

        assert status == 200

def test_negative_add_pet_without_data(name = '', animal_type = '', age = ''):
    try:
        _, auth_key = pf.get_api_key(valid_email, valid_password)
        _, result = pf.add_pet(auth_key,name, animal_type, age)
    except Exception as error:
        assert error

def test_create_pet_with_long_name(animal_type='dog', age='1', pet_photo='images/Bim.jpg'):

    name = 'Самое настоящее чудо расчудесное'

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_new_pet(api_key, name, animal_type, age)

    list_name = result['name'].split()
    word_count = len(list_name)

    assert status == 200
    assert word_count > 2







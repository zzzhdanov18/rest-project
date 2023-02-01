from main import app
from fastapi.testclient import TestClient
import os.path
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))

# include()

client = TestClient(app)

test_menu_id = ''
test_submenu_id = ''
test_dish_id = ''
base_url = '/api/v1/menus'


# testing menu
def test_get_empty_menus():
    response = client.get(base_url)
    assert response.status_code == 200
    assert response.json() == []


def test_create_menu():
    global test_menu_id
    created_menu = {'title': 'My menu 1', 'description': 'My desc 1'}
    response = client.post(base_url, json=created_menu)

    test_menu_id = response.json()['id']

    assert response.status_code == 201
    assert response.json()['title'] == 'My menu 1'
    assert response.json()['description'] == 'My desc 1'
    assert response.json()['submenus_count'] == 0
    assert response.json()['dishes_count'] == 0


def test_update_menu():
    updated_menu = {'title': 'My updated menu 1',
                    'description': 'My updated desc 1'}
    url = f'{base_url}/{test_menu_id}'
    response = client.patch(url, json=updated_menu)

    assert response.json()['id'] == test_menu_id
    assert response.json()['title'] == 'My updated menu 1'
    assert response.json()['description'] == 'My updated desc 1'


def test_get_empty_submenus():
    url = f'{base_url}/{test_menu_id}/submenus'
    response = client.get(url)

    assert response.status_code == 200
    assert response.json() == []


def test_create_submenu():
    global test_submenu_id
    url = f'{base_url}/{test_menu_id}/submenus'
    create_submenu = {'title': 'My submenu 1', 'description': 'My subdesc 1'}

    response = client.post(url, json=create_submenu)
    test_submenu_id = response.json()['id']

    assert response.json()['title'] == 'My submenu 1'
    assert response.json()['description'] == 'My subdesc 1'
    assert response.json()['dishes_count'] == 0


def test_update_submenu():
    url = f'{base_url}/{test_menu_id}/submenus/{test_submenu_id}'
    update_submenu = {
        'title': 'My updated submenu 1',
        'description': 'My updated subdesc 1',
    }

    response = client.patch(url, json=update_submenu)

    assert response.json()['title'] == 'My updated submenu 1'
    assert response.json()['description'] == 'My updated subdesc 1'
    assert response.json()['dishes_count'] == 0


def test_submenus_count():
    url = f'{base_url}/{test_menu_id}'
    response = client.get(url)
    assert response.json()['submenus_count'] == 1


def test_get_empty_dishes():
    url = f'{base_url}/{test_menu_id}/submenus/{test_submenu_id}/dishes'
    response = client.get(url)
    assert response.status_code == 200
    assert response.json() == []


def test_create_dish():
    global test_dish_id
    url = f'{base_url}/{test_menu_id}/submenus/{test_submenu_id}/dishes'
    create_dish = {'title': 'My dish 1',
                   'description': 'My dish 1', 'price': '12.50'}

    response = client.post(url, json=create_dish)
    test_dish_id = response.json()['id']

    assert response.json()['title'] == 'My dish 1'
    assert response.json()['description'] == 'My dish 1'
    assert response.json()['price'] == '12.50'


def test_update_dish():
    url = f'{base_url}/{test_menu_id}/submenus/{test_submenu_id}/dishes/{test_dish_id}'
    update_dish = {
        'title': 'My updated dish 1',
        'description': 'My updated dish 1',
        'price': '14.50',
    }

    response = client.patch(url, json=update_dish)

    assert response.json()['title'] == 'My updated dish 1'
    assert response.json()['description'] == 'My updated dish 1'
    assert response.json()['price'] == '14.50'


def test_dishes_count_for_menu():
    url = f'{base_url}/{test_menu_id}'
    response = client.get(url)
    assert response.json()['dishes_count'] == 1


def test_dishes_count_for_submenu():
    url = f'{base_url}/{test_menu_id}/submenus/{test_submenu_id}'
    response = client.get(url)
    assert response.json()['dishes_count'] == 1


def test_delete_dish():
    url = f'{base_url}/{test_menu_id}/submenus/{test_submenu_id}/dishes/{test_dish_id}'
    client.delete(url)
    test_get_empty_dishes()


def test_dishes_count_for_menu2():
    url = f'{base_url}/{test_menu_id}'
    response = client.get(url)
    assert response.json()['dishes_count'] == 0


def test_dishes_count_for_submenu2():
    url = f'{base_url}/{test_menu_id}/submenus/{test_submenu_id}'
    response = client.get(url)
    assert response.json()['dishes_count'] == 0


def test_delete_submenu():
    url = f'{base_url}/{test_menu_id}/submenus/{test_submenu_id}'
    client.delete(url)
    test_get_empty_submenus()


def test_submenus_count2():
    url = f'{base_url}/{test_menu_id}'
    response = client.get(url)
    assert response.json()['submenus_count'] == 0


def test_delete_menu():
    url = f'{base_url}/{test_menu_id}'
    client.delete(url)
    test_get_empty_menus()

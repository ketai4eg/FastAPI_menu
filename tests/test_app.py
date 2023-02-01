import requests
import pytest
from tests.config import API_URL
from tests import api

DESCRIPTION = 'Bla-bla-bla'


# server availability test
def test_root():
    response = requests.get(f'{API_URL}')
    assert response.status_code == 404


#  TEST CREATE FROM CRUD
def test_create_menu(new_menu):
    assert 'id' in new_menu


def test_create_submenu(root_submenu):
    assert 'id' in root_submenu


def test_create_dish(root_dish):
    assert 'id' in root_dish


# TEST READ FROM CRUD
def test_get_menu(root_menu):
    menu = api.get_item(path=f'menus/{root_menu["id"]}')
    assert menu['title'] == root_menu['title']


def test_get_submenu(root_submenu):
    submenu = api.get_item(
        path=f'menus/{root_submenu["menu_id"]}/submenus/{root_submenu["id"]}',
    )
    assert submenu['title'] == root_submenu['title']


def test_get_dish(root_dish):
    dish = api.get_item(
        path=f'menus/{root_dish["menu_id"]}/submenus/{root_dish["submenu_id"]}/dishes/{root_dish["id"]}',
    )
    assert dish['title'] == root_dish['title']


def test_menu_not_existed():
    with pytest.raises(api.ApiError) as err_info:
        api.get_item(path='menus/99999999')
    assert err_info.value.status_code == 404
    assert err_info.value.message == {'detail': 'menu not found'}


def test_submenu_not_existed(root_menu):
    with pytest.raises(api.ApiError) as err_info:
        api.get_item(path=f'menus/{root_menu["id"]}/submenus/999999')
    assert err_info.value.status_code == 404
    assert err_info.value.message == {'detail': 'submenu not found'}


def test_dish_not_existed(root_dish):
    with pytest.raises(api.ApiError) as err_info:
        api.get_item(
            path=f'menus/{root_dish["menu_id"]}/submenus/{root_dish["submenu_id"]}/dishes/999999',
        )
    assert err_info.value.status_code == 404
    assert err_info.value.message == {'detail': 'dish not found'}


# TEST UPDATE FROM CRUD
def test_patch_menu(new_menu):
    api.patch_item(
        path=f'menus/{new_menu["id"]}', patch={'title': 'patched_title'},
    )
    menu = api.get_item(path=f'menus/{new_menu["id"]}')
    assert menu['title'] == 'patched_title'


def test_patch_submenu(new_submenu):
    api.patch_item(
        path=f'menus/{new_submenu["menu_id"]}/submenus/{new_submenu["id"]}',
        patch={'title': 'patched_title'},
    )
    submenu = api.get_item(
        path=f'menus/{new_submenu["menu_id"]}/submenus/{new_submenu["id"]}',
    )
    assert submenu['title'] == 'patched_title'


def test_patch_dish(new_dish):
    api.patch_item(
        f'menus/{new_dish["menu_id"]}/submenus/{new_dish["submenu_id"]}/dishes/{new_dish["id"]}',
        patch={'title': 'patched_title', 'price': 100500},
    )
    dish = api.get_item(
        f'menus/{new_dish["menu_id"]}/submenus/{new_dish["submenu_id"]}/dishes/{new_dish["id"]}',
    )
    assert dish['title'] == 'patched_title'
    assert float(dish['price']) == 100500


# TEST DELETE FROM CRUD
def test_delete_menu(new_menu):
    response = api.delete_item(path=f'menus/{new_menu["id"]}')
    assert response == {'ok': True}
    with pytest.raises(api.ApiError) as err_info:
        api.get_item(path=f'menus/{new_menu["id"]}')
    assert err_info.value.status_code == 404
    assert err_info.value.message == {'detail': 'menu not found'}


def test_delete_submenu(new_submenu):
    response = api.delete_item(
        path=f'menus/{new_submenu["menu_id"]}/submenus/{new_submenu["id"]}',
    )
    assert response == {'ok': True}
    with pytest.raises(api.ApiError) as err_info:
        api.get_item(
            path=f'menus/{new_submenu["menu_id"]}/submenus/{new_submenu["id"]}',
        )
    assert err_info.value.status_code == 404
    assert err_info.value.message == {'detail': 'submenu not found'}


def test_delete_dish(new_dish):
    response = api.delete_item(
        f'menus/{new_dish["menu_id"]}/submenus/{new_dish["submenu_id"]}/dishes/{new_dish["id"]}',
    )
    assert response == {'ok': True}
    with pytest.raises(api.ApiError) as err_info:
        api.get_item(
            path=f'menus/{new_dish["menu_id"]}/submenus/{new_dish["submenu_id"]}/dishes/{new_dish["id"]}',
        )
    assert err_info.value.status_code == 404
    assert err_info.value.message == {'detail': 'dish not found'}


# TEST ONDELETE = CASCADE

def test_ondelete_submenu(new_dish):
    response = api.delete_item(
        f'menus/{new_dish["menu_id"]}/submenus/{new_dish["submenu_id"]}',
    )
    assert response == {'ok': True}
    with pytest.raises(api.ApiError) as err_info:
        api.get_item(
            path=f'menus/{new_dish["menu_id"]}/submenus/{new_dish["submenu_id"]}/dishes/{new_dish["id"]}',
        )
    assert err_info.value.status_code == 404
    assert err_info.value.message == {'detail': 'dish not found'}


def test_ondelete_menu(new_dish):
    response = api.delete_item(f'menus/{new_dish["menu_id"]}')
    assert response == {'ok': True}
    with pytest.raises(api.ApiError) as err_info:
        api.get_item(
            path=f'menus/{new_dish["menu_id"]}/submenus/{new_dish["submenu_id"]}',
        )
    assert err_info.value.status_code == 404
    assert err_info.value.message == {'detail': 'submenu not found'}
    with pytest.raises(api.ApiError) as err_info:
        api.get_item(
            path=f'menus/{new_dish["menu_id"]}/submenus/{new_dish["submenu_id"]}/dishes/{new_dish["id"]}',
        )
    assert err_info.value.status_code == 404
    assert err_info.value.message == {'detail': 'dish not found'}

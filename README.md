# Инструкция по запуску
1) Вводим **docker-compose up -d**. Запускается база данных и FastAPI приложение в фоне. (Uvicorn сервер работает по адресу **0.0.0.0:8000**)
2) Прогон тестов  **docker-compose -f docker-compose.tests.yml up**

# API

| Описание                      | Метод          | Ресурс                                                         |
| :---                          |     :---:      | :---                                                           |
| Получить все меню             | `GET`          |/api/v1/menus                                                   |
| Создать меню                  | `POST`         |/api/v1/menus                                                   |
| Получить определенное меню    | `GET`          |/api/v1/menus/{menu_id}                                         |
| Обновить определенное меню    | `PATCH`        |/api/v1/menus/{menu_id}                                         |
| Удалить определенное меню     | `DELETE`       |/api/v1/menus/{menu_id}                                         |
| Получить все подменю          | `GET`          |/api/v1/menus/{menu_id}/submenus                                |
| Создать подменю               | `POST`         |/api/v1/menus/{menu_id}/submenus                                |
| Получить определенное подменю | `GET`          |/api/v1/menus/{menu_id}/submenus/{submenu_id}                   |
| Обновить определенное подменю | `PATCH`        |/api/v1/menus/{menu_id}/submenus/{submenu_id}                   |
| Удалить определенное подменю  | `DELETE`       |/api/v1/menus/{menu_id}/submenus/{submenu_id}                   |
| Получить все блюда            | `GET`          |/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes            |
| Создать блюдо                 | `POST`         |/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes            |
| Получить определенное блюдо   | `GET`          |/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}  |
| Обновить определенное блюдо   | `PATCH`        |/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}  |
| Удалить определенное блюдо    | `DELETE`       |/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}  |


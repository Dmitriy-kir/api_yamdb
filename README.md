## Описание проекта:
Проект "YaMDb". 
Проект YaMDb - агрегатор отзывов (Review) пользователей на произведения 
(Title). Произведения делятся на категории, которые постоянно пополняются.
<!-- TABLE OF CONTENTS -->
<details>
  <summary>Содержание</summary>
  <ol>
    <li>
      <a href="#Описание-проекта">Описание проекта</a>
    </li>
    <li>
      <a href="#Запуск-проекта">Запуск проекта</a>
    </li>
    <li>
    <a href="#Примеры">Примеры</a>
    <li><a href="#Требования">Требования</a></li>
    <li><a href="#Авторы">Авторы</a></li>
    <li><a href="#Полезные ссылки">Полезные ссылки</a></li>
  </ol>
</details>

## Документация доступна по ссылке:

```
http://127.0.0.1:8000/redoc/
```
***

## Запуск проекта

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/AntonVovchik/api_yamdb
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```
<p align="right">(<a href="#top">back to top</a>)</p>

***
## Примеры

#### Примеры работы с API 
Подробная документация доступна по адресу http://127.0.0.1:8000/redoc/.
* Для неавторизованных пользователей при работе с API доступны следующие 
эндпоинты:
1. __POST__ `/api/v1/auth/signup/` - Получить код подтверждения для регистрации
2. __POST__ `/api/v1/auth/token/` Получение JWT-токена в обмен на username и 
confirmation code
3. __GET__ `/api/v1/titles/` - Получить список всех объектов
4. __GET__ `/api/v1/titles/{titles_id}/` - Информация о произведении
5. __GET__ `/api/v1/genres/` - Получить список всех жанров
6. __GET__ `/api/v1/categories/` - Получить списка всех категорий
7. __GET__ `/api/v1/titles/{title_id}/reviews/` - Получить отзыв по id для 
указанного произведения.
8. __GET__ `/api/v1/titles/{title_id}/reviews/{review_id}/comments/` Получить 
список всех комментариев к отзыву по id
9. __GET__ `/api/v1/titles/{title_id}/reviews/{review_id}/comments/
   {comment_id}/`- Получение 
   списка всех комментариев к отзыву
* Для авторизованных пользователей с ролью __Администратор__ доступны следующие эндпоинты:
10. __GET__ `/api/v1/users/` - Получить список всех пользователей
11. __POST__ `/api/v1/users/` - Добавить нового пользователя
12. __GET__ `/api/v1/users/{username}/` - Получить пользователя по username
13. Все другие возможные эндопоинты, предусмотренные проектом
* Для авторизованных пользователей с ролью __Пользователь__ доступны следующие эндпоинты:
14. __POST__ `/api/v1/titles/{title_id}/reviews/` - Добавить новый отзыв. 
Пользователь может оставить только один отзыв на произведение.
15. __PATCH__ `/api/v1/titles/{title_id}/reviews/{review_id}/` - Частично 
обновить отзыв по id. (_*Права доступа: Автор отзыва, модератор или 
    администратор._)
16. __DEL__ `/api/v1/titles/{title_id}/reviews/{review_id}/` - Частично 
обновить отзыв по id. (_*Права доступа: Автор отзыва, модератор или 
    администратор._)
17. __POST__ `/api/v1/titles/{title_id}/reviews/{review_id}/comments/` - 
Добавить новый комментарий для отзыва
18. __PATCH__ `/api/v1/titles/{title_id}/reviews/{review_id}/comments/
    {comment_id}/` - Частично обновить комментарий к отзыву по id
19. __DEL__ `/api/v1/titles/{title_id}/reviews/{review_id}/comments/
    {comment_id}/` - Удалить комментарий к отзыву по id
20. __GET__ `/api/v1/users/me/` - Получить данные своей учетной записи
21. __PATCH__ `/api/v1/users/me/` - Изменить данные своей учетной записи
***
### Требования

* [Python 3.7](https://www.python.org/downloads/release/python-370/)
* [Django 2.2.16](https://docs.djangoproject.com/en/4.0/releases/2.2.16/)
* [djangorestframework 3.12.4](https://www.django-rest-framework.org/)
* [djangorestframework-simplejwt 4.7.2](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
***
### Авторы
* [__Антончик Владимир__](https://github.com/AntonVovchik)
* [__Киреев Дмитрий__](https://github.com/Dmitriy-kir)
* [__Туманян Алексей__](https://github.com/philotelist)
***
###### Полезные ссылки
* [Aggregation](https://docs.djangoproject.com/en/4.0/topics/db/aggregation/)
* [How send email DRF](
https://stackoverflow.com/questions/53404738/how-to-send-email-with-django-rest-framwork
)
* [Creating tokens manually](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/creating_tokens_manually.html)
* [DRF documentation](https://www.django-rest-framework.org/)
* [README гайд](
https://github.com/sandino/Markdown-Cheatsheet/blob/master/README.md
)
* [README шаблон](
https://github.com/othneildrew/Best-README-Template/blob/master/README.md?plain=1
)

<p align="right">(<a href="#top">back to top</a>)</p>
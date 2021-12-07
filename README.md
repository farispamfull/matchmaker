# Matchmaker
[![Django-app workflow](https://github.com/farispamfull/matchmaker/actions/workflows/matchmaker.yml/badge.svg?branch=main)](https://github.com/farispamfull/matchmaker/actions/workflows/matchmaker.yml)
* [Техническое задание](#tech-task)
* [Описание проекта](#description)
* [Процесс регистрации](#registations)
* [API](#api)

Вход в админку:

farispamfull@gmail.com
581360004564

Приложение по адресу: http://3.124.145.142/

## Техническое задание <a name="tech-task"></a>

Задачи:
* Создать модель участников. У участника должна быть аватарка, пол, имя и фамилия, почта.
* Создать эндпоинт регистрации нового участника: /api/clients/create (не забываем о пароле и совместимости с авторизацией модели участника).
* При регистрации нового участника необходимо обработать его аватарку: наложить на него водяной знак (в качестве водяного знака можете взять любую картинку).
* Создать эндпоинт оценивания участником другого участника: /api/clients/{id}/match. В случае, если возникает взаимная симпатия, то ответом выдаем почту клиенту и отправляем на почты участников: «Вы понравились <имя>! Почта участника: <почта>».
* Создать эндпоинт списка участников: /api/list. Должна быть возможность фильтрации списка по полу, имени, фамилии. Советую использовать библиотеку Django-filters.
* Реализовать определение дистанции между участниками. Добавить поля долготы и широты. В api списка добавить дополнительный фильтр, который показывает участников в пределах заданной дистанции относительно авторизованного пользователя. Не забывайте об оптимизации запросов к базе данных
https://en.wikipedia.org/wiki/Great-circle_distance
* Задеплоить проект на любом удобном для вас хостинге, сервисах PaaS (Heroku) и т.п. Должна быть возможность просмотреть реализацию всех задач. Если есть какие-то особенности по тестированию, написать в Readme. Там же оставить ссылку/ссылки на АПИ проекта


## Описание проекта <a name="description"></a>

* В качестве аутентификация выбран authtoken. Такой способ отлично подходит для подключения в будущем одностраничного приложения через фронт. Реализован контроллер для logout.

* Реализованы новые endpoints, которые расширяют и дополняют проект.

* реализована новая роль moderator 

* Настроена админка

* Созданы новые фильтра по тому, кто тебе дал match и кому ты дал match

* В качестве деплоя выбран AWS сервер с СI/CD через github actions. Проект находится в связке postgres + Nginx + django в контейнере docker-compose.

* Фильтрация по дистанции (км) - происходит по query param `distance` (int)

* Использован django gis и postgis для быстрых пространственных вычислений



## Процесс регистрации <a name="registations"></a>
1. Пользователь отправляет post запрос с параметрами  `email`,`first_name`,`last_name`,`gender(female/male)`,`avatar`,`password` на `/clients/create/`.
2. Далее пользователь отправляет запрос с параметрами `email`,`password` на `auth/token/login/`
3. Сервер в ответ отправляет его токен (authtoken)




## API
**Prefix** /api/

**auth/token/login/**

* post

**auth/token/logout/**

* get


**clients/**
 
* get (permissions: authentication)

Доступная фильтрация: gender(str), first_name(str), last_name(str), is_swiped(bool), is_swiper(bool), distance(int)


**clients/:id/** 

* get (permissions: authentication)
* delete (permissions: moderator/staff)




**clients/create/**

* post

**clients/set_password/** 

* post (permissions: authentication)

**clients/me/**

* get (permissions: authentication)
* patch (permissions: authentication)

**clients/:id/match/**

* get (permissions: authentication)
* delete (permissions: authentication)


# Gas-api-python

### Что использовалась для разработки API?

Для разработки использовались библиотеки **FastApi, SQL Alchemy**.
В качестве БД я использовал **PostgreSQL** для хранения и управления данными. Так же я использовал **PGadmin4** для удобного использования PostgreSQL.
Для CRUD запросов использовал расширение Postman для VScode. Там можно будет собрать свою коллекцию запросов для каждой сущности, чтобы ускорить работу с API вручную.

### Краткая информация о приложении.

Это приложение, реализующее Api для сети АЗС. С помощью него можно:

- Создать нового пользователя с набором следующих параметров: **username, password, email, role, loyaltylvl, score, regdate, reviews.**
  - username - проверяется на уникальность, длинна должна быть >3 и <50 символов.
  - email - проверяется на уникальность и правильность доменного имени.
  - password - должен быть длиннее 8 символов и при попадании в бд шифруется.
  - regdate - ставится автоматически.
  - reviews - отзывы подтягивается из одноименной сущности. При создании пользователя отзывов у него нет.
  - role - по умолчанию "user", но если пользователя создаёт админе, то роль может быть назначена "admin", что даст доступ ко всем возможностям Api.
- Создавать, изменять, удалять объекты сущностей Gas, Review, FDU, Fuel, User.

### Установка

1. Клонируйте реапозиторий к себе на Пк командой `git clone https://github.com/Maximka6699/gas-api-python.git`
2. Установите зависимости командой `pip install -r requirements.txt`
   Базу данных для теста API на гитхаб выгружу в ближайшее время, а пока что придётся наполнить БД своими данными.
3. Далее надо будет запустить PGadmin4 и создать там пустую базу данных. Далее подключите свою БД в этом поле файла database.py: `DATABASE_URL = "postgresql://postgres(user):1111(password)@localhost:5432(адрес и порт на котором работает постгрес)/gas(название бд)"
4. Теперь можно приступать к запуску приложения. Запустить можно в одном из 2-х режимов:
   1. запуск приложения `python -m uvicorn app.main:app --reload `
   2. запуск приложения в режиме отладки `python -m uvicorn app.main:app --reload --log-level debug` нужно для расширенных логов ошибки 500 (ошибка сервера)

### Пример использования приложения

#### Создание пользователя и получение токена.

Первым делом нам надо будет создать пользователя. Можно создать как админа, так и обычного пользователя. Создавать можно двумя способами: 1) Через PGadmin4; 2) Через POST-запрос.

1. **Создание пользователя через запрос:**
   Команда `http://localhost:8000/create-user/` типа POST с телом запроса как на картинке: ![Pasted image 20241022130940](https://github.com/user-attachments/assets/6dd34ddd-9d84-4652-babe-a4500eb4190d)
2. **Получение токена с помощью username+password:**
   Команда для его получения: `http://localhost:8000/token`. Тело запроса как на картинке, только с вашими данными.
   ![Pasted image 20241022131245](https://github.com/user-attachments/assets/32bc96aa-fc74-47d1-aeb8-2499e69f9bd5)
   После того как получили токен передаем его в поле Authorization. В токене хранится информация о пользователе и его роли, с помощью него в путях запроса проверяется роль пользователя и в зависимости от неё выдается доступ к функциям. Т.Е. если ваша роль не Администратор, то вы сможете только просматривать некоторую информацию о сущностях, и изменить некоторые из своих данных, тогда как админу будет доступен весь функционал.
   **Примеры ограничения доступа:**
   Обычному пользователю запрещено просматривать информацию о всех пользователях, удалять других пользователей и тп. ![[Pasted image 20241022112031.png]]![[Pasted image 20241022112237.png]]
   Если же вы забыли получить токен, то доступа к функциям у вас не будет, так как вы не авторизовались. ![Pasted image 20241022132123](https://github.com/user-attachments/assets/66527284-c58b-417d-9e48-9449693e6d5a)
3. **Финал:**
   После того как вы создали пользователя и получили токен, можно использовать приложение! **Токен действителен в течении 1200 минут.** При желании можно увеличить или уменьшить время действия токена.

#### Запросы к FUEL(топливо)
![Pasted image 20241022152028](https://github.com/user-attachments/assets/b6efb916-ce6e-424d-9ecd-419760ca26f5)

1. Просмотр всего топлива: запрос - `http://localhost:8000/fuels`
   ![Pasted image 20241022133837](https://github.com/user-attachments/assets/8953f66e-7d4b-47ff-8318-10ccec37402c)
2. Просмотр конкретного топлива: запрос - `http://localhost:8000/fuels/13`
   ![Pasted image 20241022134128](https://github.com/user-attachments/assets/8c160a70-a8f0-4a1c-a0ad-73f1d83b5dcb)
3. Добавление топлива:
   1. Добавление без прикрепления к ТРК: POST-запрос `http://localhost:8000/fuels/add/` с телом
      ![Pasted image 20241022134333](https://github.com/user-attachments/assets/183c6dfa-a2de-487c-bfb3-f176eaa9315a)
   2. Добавление с прикреплением с ТРК: POST-запрос `http://localhost:8000/fuels/add/` с телом
      ![Pasted image 20241022145840](https://github.com/user-attachments/assets/f172efb5-9812-4162-b185-5b4b19e6c6b8)
   3. Обновление данных о топливе: PUT-запрос `http://localhost:8000/fuels/12` с телом как на картинке. Кроме цены и ТРК в которых есть топливо можно менять название топлива.
      ![Pasted image 20241022151148](https://github.com/user-attachments/assets/3f188131-adc9-45ed-9049-26f37b88c250)
   4. Удаление топлива: DELETE-запрос `http://localhost:8000/fuels/delete` с телом как на картинке. Можно удалять несколько видов топлива за раз, либо одно.
      ![Pasted image 20241022151521](https://github.com/user-attachments/assets/c9925af5-4172-4793-a6e2-ee338a109a92)

Все GET & DEL запросы похожи по сути между собой, так что описывать их не буду. Опишу только GET запрос на просмотр всех элементов сразу, PUT запрос на обновление объекта и POST запрос на его обновление.

#### Запросы к FDU(ТРК - колонка с топливом.)

service_date проставляется автоматически.

1. Просмотр всех ТРК: запрос - `http://localhost:8000/fdus/`
   ![Pasted image 20241022152753](https://github.com/user-attachments/assets/71b913fe-028d-42ca-8c72-4243f0659042)
2. Добавление ТРК:
   1. POST-запрос `http://localhost:8000/fdus/add/` с телом. так же можно добавлять без прикрепления к заправке и сделать это позже с помощью PUT запроса.
      ![Pasted image 20241022152825](https://github.com/user-attachments/assets/b118e31e-3aae-4e79-a391-d7b7610062bc)
3. Обновление данных о ТРК: PUT-запрос `http://localhost:8000/fdus/16` с телом как на картинке.
   ![Pasted image 20241022153119](https://github.com/user-attachments/assets/278545f8-aac5-4dbc-9301-6cfdaab90041)

#### Запросы к GAS(заправка)

1. Просмотр всех Заправок: запрос - `http://localhost:8000/gases/`
   ![Pasted image 20241022153427](https://github.com/user-attachments/assets/e3fdff5a-716c-46d1-b09e-071f6e793519)
2. Добавление Заправки:
   1. POST-запрос `http://localhost:8000/gases/add/` с телом. Адрес указывать обязательно, а вот фото и ТРК можно будет прикрепить позже. Так же можно добавить и все нужные поля за раз.
      ![Pasted image 20241022153954](https://github.com/user-attachments/assets/2b81c81c-d3b2-4d64-8f76-185eca7d4d75)
3. Обновление данных о ТРК: PUT-запрос `http://localhost:8000/gases/4` с телом как на картинке.
   ![Pasted image 20241022154257](https://github.com/user-attachments/assets/a0fe3cc7-9316-4a8f-a0fb-76e79f51d63e)
   
#### Запросы к Review(Отзывы)

1. Получить отзывы можно 3-мя способами:
   - get reviews by gas id: запрос - `http://localhost:8000/gases/2/reviews`
     отзыв для заправки 2 ![Pasted image 20241022154751](https://github.com/user-attachments/assets/228bb6c8-116d-47c9-804e-58134591dab6)
   - get reviews by id: запрос - `http://localhost:8000/reviews/1`
     получение отзыва по id отзыва ![Pasted image 20241022154838](https://github.com/user-attachments/assets/2c2a3066-da12-493f-b350-ca3f2864f5b2)
   - get all reviews: запрос - `http://localhost:8000/reviews/`
     ![Pasted image 20241022155012](https://github.com/user-attachments/assets/c95bf9bc-5ef9-4c19-80b2-38e449225f09)
2. Добавление отзыва:
   1. POST-запрос `http://localhost:8000/reviews/add/5` с телом.
      ![Pasted image 20241022155116](https://github.com/user-attachments/assets/cb95763c-2db3-439e-8b4c-e7194d319a17)
3. Обновление данных об отзыве: PUT-запрос `http://localhost:8000/reviews/1` с телом как на картинке.
   ![Pasted image 20241022155212](https://github.com/user-attachments/assets/1f378e9d-b2c7-40dc-9f8c-3e11aeef2d2a)

#### Пользователь и админ.

1. Запрос по которому можно узнать админ ты или нет - GET запрос `http://localhost:8000/admin/`
   - не авторизован ![Pasted image 20241022162100](https://github.com/user-attachments/assets/261bc41d-13b1-44fd-ab0d-12b3db46c823)
   - админ ![Pasted image 20241022162450](https://github.com/user-attachments/assets/b1633d61-7c31-491e-a045-9b013c2c5f71)
   - пользователь ![Pasted image 20241022162709](https://github.com/user-attachments/assets/fe8c425b-f8ad-4d15-98b6-3a74c10c1b24)
2. Получение всех пользователей, запрос может выполнить только админ. GET-запрос - `http://localhost:8000/admin/users/` ![Pasted image 20241022162909](https://github.com/user-attachments/assets/22d527c6-034b-4c13-bf32-b7dbb2a07edb)
3. Получение пользователя по id. GET-запрос - `http://localhost:8000/admin/users/5` ![Pasted image 20241022163821](https://github.com/user-attachments/assets/4882b85a-128d-4c56-b938-092512a4dd2d)
4. Получение информации о себе. GET-запрос - `http://localhost:8000/users/me/`
   1. админ ![Pasted image 20241022164013](https://github.com/user-attachments/assets/fff40c44-94ff-465f-b6fc-a57697367b8f)
   2. пользователь ![Pasted image 20241022164611](https://github.com/user-attachments/assets/0b25d792-569f-490a-b579-f38f60ecb42b)
5. Обновление информации о себе:
   Можно изменить Имя пользователя, пароль (понадобится старый пароль), почту. ![Pasted image 20241022165343](https://github.com/user-attachments/assets/cd237619-1f41-48aa-9338-b63d280353be)


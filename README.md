# happy-birthday

### Навык для Яндекс станции, рассказывающий об именинниках из контактов Google календаря.

Через Google Calendar API идет обращение к календарю с данными по дням рождения контактов.
На основании текущей даты, определяются именинники.  
Если именинники есть, то рассчитывается их возраст и
Яндекс станция произносит короткое напоминание о необходимости поздравить именинника, а также его данные (имя, возраст).  
Если на текущую дату именинников нет, то мы получаем напоминание о предстоящем событии (ближайшем дне рождения) контакта
с данными (имя, возраст и дата рождения).
***
### Подключение
1. Для подключения необходимо создать сервисный аккаунт в Google Cloud.
2. Создать аккаунт на Yandex Cloud.
3. На Yandex Cloud в консоли управления создать новую функцию.
   - Добавить содержимое, полученного на шаге №1 файла-ключа, в переменную окружения под именем `private_key` для функции, созданной на шаге №2. 
   - Прописать в переменную окружения под именем `calendar_id` идентификатор Google календаря для этой же функции. 
4. В файле [settings.py](settings.py) присвоить переменной `my_name` Ваше имя (для того, чтобы Алиса обращалась к Вам по имени).
5. Добавить файлы [happy_birthday.py](happy_birthday.py), [requirements.txt](requirements.txt) 
и [settings.py](settings.py) в Yandex Cloud.
***
После всех настроек, достаточно в приложении "Умный Дом" создать сценарий для Алисы, с фразой активации, например, 
"Алиса, у кого сегодня день рождения?". По этой фразе запускать навык. В ответ, Алиса сразу расскажет об именинниках.

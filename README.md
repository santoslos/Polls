# Polls
Api системы для опросов пользователей
# Описание тз
## Функционал для администратора системы
- добавление/изменение/удаление опросов. Атрибуты опроса: название, дата старта, дата окончания, описание.
- После создания поля "дата старта"  у опроса менять нельзя добавление/изменение/удаление вопросов в опросе. Атрибуты вопросов: текст вопроса, тип вопроса (ответ текстом, ответ с выбором одного варианта, ответ с выбором нескольких вариантов)  
## Функционал для пользователей системы
- получение списка активных опросов
-  прохождение опроса: опросы можно проходить анонимно, в качестве идентификатора пользователя в API передаётся числовой ID, по которому сохраняются ответы пользователя на вопросы; один пользователь может участвовать в любом количестве опросов
-  получение пройденных пользователем опросов с детализацией по ответам (что выбрано) по ID уникальному пользователя

# Развертывание приложения
* склонируйте репозиторий
* перейдити в дерикторию src 
* ввидите команду docker-compose build
* затем команду   docker-compose up
* приложение будет доступна по адресу: http://127.0.0.1:8000/
* имя администратора admin, пароль admin
# Документация api
Аутенфикация доступна по адресу http://127.0.0.1:8000/admin/v1/base-auth/login/
Все методоты  начинаются с http://127.0.0.1:8000/api/v1
# Опрос
- polls список всех опросов 
- polls/detail/<int:pk>/questions/ получение списка вопросов по id опроса 
- polls/create/ создание опроса (Доступоно администратору)
- polls/detail/<int:pk>/ если отправить метод get выведет запрос, если put отредактирует, если delete удалит (Доступоно администратору)
- polls/questions/answer/<int:pk> получение пройденных пользователем опросов с детализацией по ответам  по ID уникальному пользователя (Доступоно администратору)
# Вопросы 
- questions/create создасть вопрос, если опрос не начат (Доступоно администратору)
- questions/<int:pk>, если отправить метод put обновит вопрос или delete удалит, если опрос не начат  (Доступоно администратору)
# Варианты 
- choice/create  добавит вариант ответа к вопросу, если вопрос имеет тип ответ с выбором одного варианта или ответ с выбором нескольких вариантов и вопрос не относится к  начатому опросу (Доступоно администратору)
- choice/detail/<int:pk>/ если отправить метод put обновит вариант ответа, delete удалит, если опрос не начат или если у него не текстовой тип (Доступоно администратору)
# Ответы 
- answer/create добавит ответ, если опрос начат и пользователь не отвечал на этот вопрос
- answer/<int:pk> если отправить метод put обновит ответ, delete удалит (Доступоно администратору)







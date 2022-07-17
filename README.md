# notebook

## Для запуска
```
docker-compose up
```

### Подключил удаленный amqp instance: [cloudamqp.com](https://www.cloudamqp.com/)
Все запросы между сервисами работают через RabbitMQ

## Репозиторий сервиса контактных данных пользовалей: [YesseyMelis/user_info](https://github.com/YesseyMelis/user_info)

# API
## SWAGGER
```
http://0.0.0.0:8000/api/v1/swagger/
```

## Создать пользователя
```
POST: api/v1/users
```
## Авторизация
```
POST: api/v1/users/token
```
## Обновить контактные данные пользователя
```
PUT: api/v1/users/{id}
```
## Получить контактные информации по всем пользователям
```
GET: api/v1/users/users_info
```
## скачать файл excel с контактными данными пользователей
```
GET: api/v1/users/download_excel
```

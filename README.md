# Secret service 

Проект secret service - это простой HTTP сервис для одноразовых секретов, наподобие https://onetimesecret.com/.

### Инструменты

- Python >= 3.9
- Django Rest Framework
- Docker

## Старт
#### 1) Клонировать репозиторий 

    git clone https://github.com/Icebeear/secret_service.git


#### 2) Создать образ и запустить контейнер

    docker-compose up --build

#### 3) Перейти по адресу

    http://127.0.0.1:8000/swagger/
# VetClinic MVP

Проста система для одного ветеринара на Django Templates.

## Що реалізовано

- обов'язковий вхід у систему;
- картки пацієнтів без окремої сутності клієнта;
- дані тварини та власника в одній картці;
- історія прийомів;
- вакцинації зі статусами:
  - зелений: актуальна;
  - жовтий: скоро потрібно повторити;
  - червоний: прострочена;
- блок вакцинацій на головній сторінці;
- простий склад товарів;
- операції складу `Придбано` і `Продано` через modal window;
- Django admin panel.

## Технології

- Python 3.11
- Django 5.2
- SQLite
- Django Templates
- Bootstrap 5

Без React, REST API, JWT, Docker, Celery, Redis, WebSockets і PostgreSQL.

## Структура

```text
vetclinic/
├── backend/
│   ├── backend/          # settings, urls, wsgi/asgi
│   ├── clinic/           # основний Django app
│   ├── templates/        # Django templates
│   ├── static/           # CSS
│   └── manage.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Встановлення

З кореня проєкту:

```bash
python -m venv .venv_clinic
source .venv_clinic/bin/activate
pip install -r requirements.txt
```

## Міграції

```bash
python backend/manage.py migrate
```

Якщо моделі змінювались:

```bash
python backend/manage.py makemigrations
python backend/manage.py migrate
```

## Створення користувача

Поточний користувач для локальної перевірки:

```text
Login: Dmitro
Password: dog_cat_1
```

Щоб створити нового адміністратора вручну:

```bash
python backend/manage.py createsuperuser
```

## Запуск

```bash
python backend/manage.py runserver
```

Після запуску:

- сайт: http://127.0.0.1:8002/
- сторінка входу: http://127.0.0.1:8002/login/
- admin panel: http://127.0.0.1:8002/admin/

Початкова сторінка `/` без входу автоматично перенаправляє на `/login/`.

## Перевірка

```bash
python backend/manage.py check
python backend/manage.py test
```

## Основні моделі

- `Patient` - головна сутність, картка тварини та власника.
- `Visit` - прийом, прив'язаний до `Patient`.
- `Vaccination` - вакцинація, прив'язана до `Patient`.
- `InventoryItem` - товар складу.

Зв'язки:

- `Visit.patient` має `ForeignKey` на `Patient`.
- `Vaccination.patient` має `ForeignKey` на `Patient`.
- при видаленні пацієнта його прийоми і вакцинації видаляються автоматично через `CASCADE`.

## Корисні команди

Зупинити сервер, якщо потрібний порт зайнятий:

```bash
lsof -nP -iTCP:8002 -sTCP:LISTEN
kill <PID>
```

Запустити на іншому порту:

```bash
python backend/manage.py runserver 127.0.0.1:8003
```

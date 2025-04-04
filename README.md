# Установка

```bash
git clone <GIT-РЕПОЗИТОРИЙ_ВАШЕГО_ПРОЕКТА>

cd <НАЗВАНИЕ_ВАШЕГО_ПРОЕКТА>
```

Переключаемся на ветку `main`

```bash
git checkout main

git push -u origin main
```

Копируем файл `.env.example` в файл `.env`

```bash
cp .env.example .env.dev
```

Редактируем файл '.env.dev', 
заполняем своими данными.
Особенно важно задать:
- SECRET_KEY

Запускаем проект

```bash
make up
```
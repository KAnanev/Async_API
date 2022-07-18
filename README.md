# Проектная работа 5 спринта

Ссылка на репозиторий https://github.com/Michail-Ign/Async_API_sprint_2.

## Как запустить тесты
 - Создайте в папке `src/` файл `.env` и заполните его нужными переменными окружения (образец в файле `.env.example`).
 - Запустите `docker-compose.yml` в папке `src/tests/functional`:

```bash
docker-compose -f src/tests/functional/docker-compose.yml up --build
```

Если Docker Compose при запуске выдаёт ошибку `Error response from daemon: pull access denied for api-image, repository does not exist or may require 'docker login': denied: requested access to the resource is denied`,
то соберите сначала образ сервиса `api`:

```bash
docker-compose -f src/tests/functional/docker-compose.yml build api
```
---

В папке **tasks** ваша команда найдёт задачи, которые необходимо выполнить во втором спринте модуля "Сервис Async API".

Как и в прошлом спринте, мы оценили задачи в стори поинтах.

Вы можете разбить эти задачи на более маленькие, например, распределять между участниками команды не большие куски задания, а маленькие подзадачи. В таком случае не забудьте зафиксировать изменения в issues в репозитории.

**От каждого разработчика ожидается выполнение минимум 40% от общего числа стори поинтов в спринте.**

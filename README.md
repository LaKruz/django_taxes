# Taxes
Сервис, проверяющий корректность исчисления НДФЛ
## Разворачивание локально
1. Рекумендуется создать виртуальное окружение
2. Установка зависимостей:
```bash
pip install -r requirements.txt
```
3. Создание файла .env, содержащего переменные окружения
- `DJANGO_SECRET_KEY` секретный ключ Django
- `DJANGO_DEBUG` режим отладки (по умолчанию `True`)
- `DJANGO_ALLOWED_HOSTS` разрешённые хосты
## Разворачивание через docker
1. Создание файла .env, содержащего переменные окружения
2. Создание docker image
```bash
docker buildx b --pull --rm -f "Dockerfile" -t taxes:latest "." 
```
3. Запуск docker container
```bash
docker run --rm -d -p 8000:8000/tcp taxes:latest
```

## Использование
1. Перейти по адресу http://**HOST_ADDRESS**:8000/
где HOST_ADDRESS это адрес сервера.(например при локальном запуске это http://127.0.0.1:8000/)
2. Выбрать файл соответствующий формату в файле `/test_task/example_data.xlsx`
3. Нажать "Отправить"
4. В результате будет скачан файл, где заголовок отформатирован в соответствии с образцом `/test_task/rept_header.xlsx` и столбец "Отклонения" отформатирован в соответствии с заданием `/test_task/test_task_text.md`
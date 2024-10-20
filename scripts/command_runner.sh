# Виртуальный окружение
python3 -m venv venv-document-bot
source venv-document-bot/bin/activate
# deactivate
# rm -rf venv-document-bot

# Зависимости
python3 -m poetry install # Установка зависимостей из poetry.lock
python3 -m poetry lock # Заполнение poetry.lock
# poetry install

# Запуск
docker-compose up --build -d
# docker kill $(docker ps -a -q)
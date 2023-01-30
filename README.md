# Инструкция по запуску
1) Вводим **docker-compose up -d**. Запускается база данных и FastAPI приложение в фоне. (Uvicorn сервер работает по адресу **0.0.0.0:8000**)
2) Прогон тестов  **docker-compose -f docker-compose.tests.yml up**

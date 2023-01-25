# Инструкция по запуску
1) После загрузки из-под папки с проектом выполить команту **pip install -r requirements.txt**
2) Вводим **docker-compose up -d**. Запускается база данных и FastAPI приложение в фоне. (Uvicorn сервер работает по адресу **0.0.0.0:8000**) 
3) Прогон тестов  **docker-compose -f docker-compose.tests.yml up**
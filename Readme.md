# WeatherAPI

Проект **WeatherAPI** предоставляет API для получения информации о погоде с использованием **Open-Meteo**. В нем реализованы четыре метода, которые позволяют работать с прогнозами погоды для различных городов.

## Методы API

1. **Метод 1**: 
    - Принимает координаты (широту и долготу) и возвращает данные о температуре, скорости ветра и атмосферном давлении на момент запроса.
    
2. **Метод 2**: 
    - Принимает название города и добавляет его в список городов, для которых отслеживается прогноз погоды. Сервер хранит прогноз погоды для указанных городов на текущий день и обновляет его каждые 15 минут.
    
3. **Метод 3**: 
    - Возвращает список городов, для которых доступен прогноз погоды.
    
4. **Метод 4**: 
    - Принимает название города и время, и возвращает погоду на текущий день в указанное время, взятую из базы данных. Также предоставляет возможность выбирать параметры погоды для получения в ответе: температура, влажность, скорость ветра, осадки.

## Используемые технологии

- **aiohttp**: для асинхронных запросов к API Open-Meteo.
- **FastAPI**: для обработки HTTP-запросов и создания API.
- **Pydantic**: для валидации данных.
- **SQLAlchemy**: для работы с базой данных.
- **Open-Meteo**: источник данных о погоде (координаты городов берутся из Open-Meteo для исключения ошибок пользователя).

## Структура проекта

Проект разбит на три слоя:

- **Презентации (API)**: обработка HTTP-запросов.
- **Бизнес-логики (BLL)**: логика обработки данных и работы с сервисами.
- **Доступа к данным (DAL)**: взаимодействие с базой данных.

Все зависимости между слоями описаны в файле `src/dependencies.py`.

## Установка и запуск

1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/Saveliy19/WeatherAPI.git
    ```
    
2. Перейдите в папку с проектом:
    ```bash
    cd .\WeatherAPI\src\
    ```
    
3. Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```

4. Запустите приложение:
    ```bash
    python main.py
    ```
    
    Приложение будет доступно по адресу: `http://127.0.0.1:8000`

5. Для тестирования эндпоинтов откройте документацию по адресу:  
    `http://127.0.0.1:8000/docs`
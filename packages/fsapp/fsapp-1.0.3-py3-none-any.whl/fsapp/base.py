from fastapi import FastAPI

from fsapp.core.config import settings
from fsapp.api.routers import api_router
from fsapp.classes import BaseExecutor
from fsapp.core.config import create_settings_files

create_settings_files()

# Основной объект приложения
# todo argument comments
app = FastAPI(
    title=settings.required.instance,
    docs_url="/docs",
)

settings.token = None
# Подключение всех эндпоинтов
app.include_router(api_router)
# Добавляем базовый класс обработчиков
app.base_class = BaseExecutor


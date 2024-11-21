from fastapi import FastAPI
from db import init_models
from contextlib import asynccontextmanager
from advertisement import router as advertisement
from user import router as user


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Включение")
    await init_models()
    print("База данных включилась")
    yield
    print("Выключение")


app = FastAPI(lifespan=lifespan)
app.include_router(advertisement)
app.include_router(user)

# uvicorn main:app --reload запуск

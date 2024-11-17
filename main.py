from fastapi import FastAPI
from database.db import init_models
from contextlib import contextmanager
from routers.advertisement import router as advertisement
from routers.user import router as user


@contextmanager
def lifespan(app: FastAPI):
    print("Включение")
    init_models()
    print("База данных включилась")
    yield
    print("Выключение")


app = FastAPI(lifespan=lifespan)
app.include_router(advertisement)
app.include_router(user)

# unicorn main:app --reload запуск

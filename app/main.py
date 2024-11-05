from fastapi import FastAPI, HTTPException, Depends
from typing import Optional
from schema import MyAdvertisement, UpdateAdvertisement
from database.db import Advertisement, create_tables, connect_session, Session, engine
from contextlib import contextmanager

sess = Session()

@contextmanager
def lifespan(app: FastAPI):
    create_tables(engine)
    yield
    print("Выключение")


app = FastAPI(lifespan=lifespan)


@app.post("/advertisement") 
def post_advertisement(new_adv: MyAdvertisement):
    save_adv = Advertisement(**new_adv)
    connect_session(save_adv,True)
    return new_adv


@app.patch("/advertisement/{advertisement_id}/")
def patch_advertisement(advertisement_id: int ,new_adv: UpdateAdvertisement):
    update_adv = sess.query(Advertisement).filter(Advertisement.id == advertisement_id).first()
    if update_adv:
        for key,value in new_adv.dict().items():
            setattr(update_adv, key, value)
        connect_session(update_adv)
    else:
        raise HTTPException(status_code=404, detail=f"Advertisement {advertisement_id} not found in the database.")
    
    
@app.delete("/advertisement/{advertisement_id}/")
def del_one(advertisement_id: int):
    for_del = sess.query(Advertisement).filter(Advertisement.id == advertisement_id).delete()
    connect_session(for_del)    
    return {f"advertisement {advertisement_id}" : "Delete"}

@app.get("/advertisement/{advertisement_id}/")
def get_advertisement(advertisement_id: int, new_adv: MyAdvertisement):
    adv = sess.query(Advertisement).filter(Advertisement.id == advertisement_id).first()
    if adv:
        return adv
    else:
        raise HTTPException(status_code=404, detail=f"Advertisement {advertisement_id} not found in the database.")

@app.get("/advertisement/")
def get_query_string(id: Optional[int] = None,
                     params: UpdateAdvertisement = Depends()):
    query = sess.query(Advertisement)

    if id is not None:
        query = query.filter(Advertisement.id == id)
    if params.title is not None:
        query = query.filter(Advertisement.title.ilike(f"%{params.title}%"))
    if params.description is not None:
        query = query.filter(Advertisement.description.ilike(f"%{params.description}%"))
    if params.price is not None:
        query = query.filter(Advertisement.price == params.price)
    if params.author is not None:
        query = query.filter(Advertisement.author.ilike(f"%{params.author}%"))

    result = query.all()
    return result


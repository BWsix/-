from hashlib import md5
from fastapi import HTTPException

from sqlalchemy.orm import Session

from . import models, schemas


def get_url(db: Session, id: str):
    return db.query(models.Item).filter(models.Item.id == id).first()

def get_url_id(url: str):
    val = url
    while True:
        val = md5(val.encode()).digest().hex()
        yield val[:4]

def create_item(db: Session, item: schemas.ItemCreate):
    print(item)
    if item.id:
        if get_url(db, item.id):
            raise HTTPException(status_code=400, detail=f'id "{item.id}" already taken')
    else:
        for id in get_url_id(str(item.url)):
            if get_url(db, id) is None:
                item.id = id
                break

    db_item = models.Item(id=item.id, url=str(item.url))
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

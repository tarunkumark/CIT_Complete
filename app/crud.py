from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_items_by_title(db: Session, title: str):
    return db.query(models.Item).filter(models.Item.title == title).all()

def get_items_by_owner(db: Session, owner_id: int):
    return db.query(models.Item).filter(models.Item.owner_id == owner_id).all()

def update_item(db:Session, item_id:int, item_data: schemas.ItemCreate):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).one()
    if not db_item:
        return False
    db_item.title = item_data.title
    db_item.description = item_data.description
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db:Session, item_id:int):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).one()
    if not db_item:
        return False
    db.delete(db_item)
    db.commit()
    return {"msg":"deleted successfully"}
    

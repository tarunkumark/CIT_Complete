from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#Create a route function to create a user using POST method
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)
        



#Create a route function to get all users using GET method
@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users
        



#Create a route to get a user by id using GET method
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user




#Create a route function to create an item for a user using POST method
@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)
        



#Create a route function to get all items using GET method
@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items
        



#Create a route function to get all items by title using GET method
@app.get("/items/{title}", response_model=list[schemas.Item])
def read_items_by_title(title: str, db: Session = Depends(get_db)):
    items = crud.get_items_by_title(db, title)
    return items
        



#Create a route function to get all items by owner using GET method
@app.get("/items/owner/{owner_id}", response_model=list[schemas.Item])
def read_items_by_owner(owner_id: int, db: Session = Depends(get_db)):
    items = crud.get_items_by_owner(db, owner_id)
    return items
        



    





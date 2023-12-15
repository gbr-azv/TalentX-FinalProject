from typing import List
#
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
#
from . import models, schemas
from .database import engine, get_db
from .routers import order, user, auth

# Called to create the tables in the database based on the defined models
models.Base.metadata.create_all(bind=engine)

# Creates an instance of the FastAPI application
app = FastAPI()

############################## ROUTES ##############################

# [GET] Request The Restaurant's Home Page
@app.get("/")
def home():
    return {"Message":"Welcome to Joe's Restaurant Delivery"}

# [GET] Request The Restaurant Menu
@app.get("/menu", response_model=List[schemas.MenuResponse])
def get_menu(db: Session = Depends(get_db)):
    menu = db.query(models.Product).all()
    return menu

# Include routes from another router, in the main application
# Which are in: "routers/order.py", "routers/user.py", and "routers/auth.py"'
# Useful for organizing and modularizing routes in different parts of the code
app.include_router(order.router)
app.include_router(user.router)
app.include_router(auth.router)
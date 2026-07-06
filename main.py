from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import User

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/users", status_code=200)
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()

    return users


@app.get("/users/{user_id}", status_code=200)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


@app.post("/users", status_code=201)
def create_user(user: dict, db: Session = Depends(get_db)):
    new_user = User(
        id=user["id"],
        name=user["name"],
        age=user["age"],
        city=user["city"]
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User created successfully",
        "user": new_user
    }


@app.put("/users/{user_id}", status_code=200)
def update_user(user_id: int, updated_user: dict, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.name = updated_user["name"]
    user.age = updated_user["age"]
    user.city = updated_user["city"]

    db.commit()
    db.refresh(user)

    return {
        "message": "User updated successfully",
        "user": user
    }


@app.patch("/users/{user_id}", status_code=200)
def patch_user(user_id: int, updated_user: dict, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if "name" in updated_user:
        user.name = updated_user["name"]

    if "age" in updated_user:
        user.age = updated_user["age"]

    if "city" in updated_user:
        user.city = updated_user["city"]

    db.commit()
    db.refresh(user)

    return {
        "message": "User updated successfully",
        "user": user
    }


@app.delete("/users/{user_id}", status_code=200)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    db.delete(user)
    db.commit()

    return {
        "message": "User deleted successfully"
    }
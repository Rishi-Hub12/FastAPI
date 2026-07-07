from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import User
from schemas import UserCreate, UserUpdate, UserPatch, UserResponse

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/users", status_code=200, response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()

    return users


@app.get("/users/{user_id}", status_code=200, response_model=UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


@app.post("/users", status_code=201)
def create_user(user: None, db: Session = Depends(get_db)):
    new_user = User(
        id=user.id,
        name=user.name,
        age=user.age,
        city=user.city
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User created successfully",
        "user": new_user
    }


@app.put("/users/{user_id}", status_code=200)
def update_user(user_id: int, updated_user: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.name = updated_user.name
    user.age = updated_user.age
    user.city = updated_user.city

    db.commit()
    db.refresh(user)

    return {
        "message": "User updated successfully",
        "user": user
    }


@app.patch("/users/{user_id}", status_code=200)
def patch_user(user_id: int, updated_user: UserPatch, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if updated_user.name is not None:
        user.name = updated_user.name

    if updated_user.age is not None:
        user.age = updated_user.age

    if updated_user.city is not None:
        user.city = updated_user.city

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
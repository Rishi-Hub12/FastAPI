from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import User

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/users", status_code=200)
def get_all_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@app.get("/users/{user_id}", status_code=200)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if user:
        return user

    raise HTTPException(
        status_code=404,
        detail="User not found"
    )


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

    if not user:
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
def patch_user(user_id: int, updated_fields: dict, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    for key, value in updated_fields.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return {
        "message": "User updated successfully",
        "user": user
    }


@app.delete("/users/{user_id}", status_code=200)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    db.delete(user)
    db.commit()

    return {
        "message": "User deleted successfully"
    }
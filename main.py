from fastapi import FastAPI, HTTPException

app = FastAPI()

users = [
    {
        "id": 1,
        "name": "Rishi",
        "age": 24,
        "city": "Chennai"
    },
    {
        "id": 2,
        "name": "Arun",
        "age": 25,
        "city": "Madurai"
    },
    {
        "id": 3,
        "name": "Kumar",
        "age": 26,
        "city": "Coimbatore"
    },
    {
        "id": 4,
        "name": "Ajith",
        "age": 27,
        "city": "Kerla"
    },
    {
        "id": 5,
        "name": "Vijay",
        "age": 23,
        "city": "Ooty"
    },
    {
        "id": 6,
        "name": "Praveen",
        "age": 26,
        "city": "Mysore"
    },
    {
        "id": 7,
        "name": "Naveen",
        "age": 21,
        "city": "Bangalore"
    },
    {
        "id": 8,
        "name": "Sarath",
        "age": 26,
        "city": "Vellore"
    },
    {
        "id": 9,
        "name": "Ajay",
        "age": 26,
        "city": "Trichy"
    },
    {
        "id": 10,
        "name": "Akash",
        "age": 26,
        "city": "Salem"
    }
    
]


@app.get("/users", status_code=200)
def all_users():
    return users


@app.get("/users/{user_id}", status_code=200)
def user_by_id(user_id: int):
    for user in users:
        if user["id"] == user_id:
            return user

    raise HTTPException(
        status_code=404,
        detail="User not found"
    )


@app.post("/users", status_code=201)
def create_user(user: dict):

    users.append(user)

    return {
        "message": "User created successfully",
        "user": user
    }


@app.put("/users/{user_id}", status_code=200)
def update_user(user_id: int, updated_user: dict):

    for index, user in enumerate(users):

        if user["id"] == user_id:

            users[index] = updated_user

            return {
                "message": "User updated successfully",
                "user": updated_user
            }

    raise HTTPException(
        status_code=404,
        detail="User not found"
    )


@app.patch("/users/{user_id}", status_code=200)
def patch_user(user_id: int, updated_fields: dict):

    for user in users:

        if user["id"] == user_id:

            user.update(updated_fields)

            return {
                "message": "User updated successfully",
                "user": user
            }

    raise HTTPException(
        status_code=404,
        detail="User not found"
    )

@app.delete("/users/{user_id}", status_code=200)
def delete_user(user_id: int):

    for user in users:

        if user["id"] == user_id:

            users.remove(user)

            return {
                "message": "User deleted successfully"
            }

    raise HTTPException(
        status_code=404,
        detail="User not found"
    )
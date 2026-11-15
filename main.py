# This is a sample Python script.
from __future__ import annotations

from argparse import ArgumentParser


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
app = FastAPI()


class User(BaseModel):
    name: str
    age: int
    city: str


users: list[User] = [
    User(name="An", age=22, city="HCM"),
    User(name="Binh", age=30, city="HN"),
    User(name="Chi", age=27, city="HCM"),
]


@app.get("/users")
def list_users(city: Optional[str] = None) -> list[User]:
    if city:
        return [u for u in users if u.city == city]
    return users


@app.get("/users/{user_id}")
def get_user(user_id: int) -> User:
    if user_id < 0 or user_id >= len(users):
        raise HTTPException(status_code=404, detail="Không tìm thấy user")
    return users[user_id]


@app.post("/users", status_code=201)
def create_user(user: User) -> User:
    users.append(user)
    return user

@app.get("/stats")
def get_stats() -> dict:
    if not users:
        return {"count": 0, "average_age": 0.0, "cities": {}}

    # Đếm số lượng theo từng thành phố
    cities_count = {}
    for u in users:
        cities_count[u.city] = cities_count.get(u.city, 0) + 1

    return {
        "count": len(users),
        "average_age": round(sum(u.age for u in users) / len(users), 2),
        "cities": cities_count,
    }

@app.delete("/users/{user_id}")
def delete_user(user_id: int) -> User:
    if user_id < 0 or user_id >= len(users):
        raise HTTPException(status_code=404, detail= "Không tìm thấy user")
    popped_user = users.pop(user_id)
    print("Đã xoá thành công")
    return popped_user


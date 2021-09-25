import uvicorn
from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/users")
def get_users(limit: int = None):
    return {"limit": limit}


@app.get("/users/me")
def get_current_user():
    return {"user_id": 123}


@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

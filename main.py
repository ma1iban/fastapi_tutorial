import uvicorn
from typing import Optional, List
from fastapi import FastAPI, status, Path, Query, Cookie, Header
from pydantic import BaseModel, HttpUrl, EmailStr, parse_obj_as, Field

app = FastAPI()


@app.get("/header")
def get_headers(x_token: str = Header(None, title="토큰", convert_underscores=True)):
    return {"X-Token": x_token}


@app.get("/cookie")
def get_cookies(ga: str = Cookie(None)):
    return {"ga": ga}

######################################################################

inventory = (
    {
        "id": 1,
        "user_id": 1,
        "name": "레전드포션",
        "price": 2500.0,
        "amount": 100,
    },
    {
        "id": 2,
        "user_id": 1,
        "name": "포션",
        "price": 300.0,
        "amount": 50,
    },
)


class Item(BaseModel):
    name: str = Field(default=..., min_length=1, max_length=100, title="이름")
    price: float = Field(default=None, ge=0)  # greater than equal:
    amount: int = Field(
        default=1,
        gt=0,
        le=100,  # less than equal : 작거나 같다
        title="수량",
        description="아이템 갯수. 1~100 개 까지 소지 가능",
    )


@app.post("/users/{user_id}/item")
def create_item(item: Item):
    return item


@app.get("/users/{user_id}/inventory", response_model=List[Item])
def get_item(
    user_id: int = Path(..., gt=0, title="사용자 id", description="DB의 user.id"),
        # ... : alias 객체: 생략
        # gt: Greater than : 보다 큰
    name: str = Query(None, min_length=1, max_length=2, title="아이템 이름"),
        # None : 선택
):
    user_items = []
    for item in inventory:
        if item["user_id"] == user_id:
            user_items.append(item)

    response = []
    for item in user_items:
        if name is None:
            response = user_items
            break
        if item["name"] == name:
            response.append(item)

    return response


##################################################################################

class User(BaseModel):
    name: str
    avatar_url: HttpUrl = "https://icotar.com/avatar/fastcampus.png?s=200"


class CreateUser(User):
    password: str


@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: CreateUser):
    return user


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8001)

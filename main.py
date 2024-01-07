from fastapi import FastAPI
import requests
from pydantic import BaseModel, Field
from typing import List

app = FastAPI()


class Instance(BaseModel):
    instance: str = Field(..., example="misskey.io")


class InstanceList(BaseModel):
    data: List[Instance]


@app.get("/")
async def root():
    return {"message": "This App is running on FastAPI"}


@app.get("/misskey", response_model=InstanceList)
async def get_misskey_server_list():
    # https://instanceapp.misskey.page/instances.json からインスタンス一覧をrequestsで取得
    response = requests.get("https://instanceapp.misskey.page/instances.json")

    json_data = response.json()
    # extract url list
    url_list = {
        "data": [
            {"instance": instance["url"]} for instance in json_data["instancesInfos"]
        ]
    }

    return url_list

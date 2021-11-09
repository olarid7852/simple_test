from typing import Optional

from fastapi import FastAPI, status
from db import async_session
from manager import MemberDal, TeamDAL
from schemas import Member as MemberSchema

app = FastAPI()

@app.get("/teams/average_age/")
async def get_team_average_age(desc: Optional[int] = 0):
    async with async_session() as session:
        async with session.begin():
            return await TeamDAL.get_average_age(session, desc)

@app.get("/player/{id}")
async def get_player_by_id(id: int) -> MemberSchema:
    async with async_session() as session:
        async with session.begin():
            player = await MemberDal.get_by_id(session, id)
            return MemberSchema.from_model_object(player)


@app.post("/create_player", status_code=status.HTTP_201_CREATED)
async def create_player(player: MemberSchema):
    async with async_session() as session:
        async with session.begin():
            created_player = await MemberDal.create(session, player)
            return MemberSchema.from_model_object(created_player)


@app.put("/player/{id}")
async def update_player(player: MemberSchema, id: int):
    async with async_session() as session:
        async with session.begin():
            created_player = await MemberDal.update(session, id, player)
            return MemberSchema.from_model_object(created_player)

@app.delete("/player/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_player(id: int):
    async with async_session() as session:
        async with session.begin():
            await MemberDal.delete(session, id)
            return None


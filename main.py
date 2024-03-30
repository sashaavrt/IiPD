from fastapi import FastAPI

app = FastAPI()
@app.get("/")

async def home():
  return {"data": "Hello World"}
from pydantic import BaseModel

class STaskAdd(BaseModel):
  name: str
  description: str | None = None


from fastapi import Depends

@app.post("/")
async def add_task(task: STaskAdd = Depends()):
  return {"data": task}

from datetime import datetime
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

engine = create_async_engine("sqlite+aiosqlite:///tasks.db")
new_session = async_sessionmaker(engine, expire_on_commit=False)

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Model(DeclarativeBase):
  pass

class TaskOrm(Model):
  __tablename__ = "tasks"
  id: Mapped[int] = mapped_column(primary_key=True)
  name: Mapped[str]
  description: Mapped[str | None]

async def create_tables():
  async with engine.begin() as conn:
    await conn.run_sync(Model.metadata.create_all)

async def delete_tables():
  async with engine.begin() as conn:
    await conn.run_sync(Model.metadata.drop_all)

from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import create_tables, delete_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
  await create_tables()
  print("База готова")
  yield
  await delete_tables()
  print("База очищена")

app = FastAPI(lifespan=lifespan)
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
from databases import Database

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure database
SQLALCHEMY_DATABASE_URL = "sqlite:///./tasks.db"
database = Database(SQLALCHEMY_DATABASE_URL)
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define models
class TaskIn(BaseModel):
    title: str
    done: bool = False

class TaskOut(TaskIn):
    id: int

class TaskUpdate(BaseModel):
    title: str
    done: bool

class TaskDB(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    done = Column(Boolean, default=False)

# Create tables
Base.metadata.create_all(bind=engine)

# API endpoints
@app.post('/tasks', response_model=TaskOut)
async def create_task(task: TaskIn):
    query = TaskDB.insert().values(**task.dict())
    last_record_id = await database.execute(query)
    return {**task.dict(), "id": last_record_id}

@app.get('/tasks', response_model=list[TaskOut])
async def get_tasks():
    query = TaskDB.select()
    return await database.fetch_all(query)

@app.get('/tasks/{task_id}', response_model=TaskOut)
async def get_task(task_id: int):
    query = TaskDB.select().where(TaskDB.id == task_id)
    task = await database.fetch_one(query)
    if not task:
        raise HTTPException(status_code=404, detail='Task not found')
    return TaskOut(**task)

@app.put('/tasks/{task_id}', response_model=TaskOut)
async def update_task(task_id: int, task: TaskUpdate):
    query = TaskDB.update().where(TaskDB.id == task_id).values(**task.dict())
    await database.execute(query)
    return {**task.dict(), "id": task_id}

@app.delete('/tasks/{task_id}')
async def delete_task(task_id: int):
    query = TaskDB.delete().where(TaskDB.id == task_id)
    await database.execute(query)
    return {'success': True}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)

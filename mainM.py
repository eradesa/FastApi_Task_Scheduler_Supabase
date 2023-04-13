from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


app = FastAPI()

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://era-task-scheduler.netlify.app/","https://era-task-scheduler.netlify.app","http://127.0.0.1:5500","http://127.0.0.1:5501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the SQLite database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./tasks.db"

# Create the database engine and session factory
engine = create_engine(SQLALCHEMY_DATABASE_URL)
#SessionLocal = sessionmaker(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Define the SQLAlchemy model for tasks
Base = declarative_base()
"""
# Define models
class TaskIn(BaseModel):
    title: str
    description:str
    done: bool = False

class TaskOut(TaskIn):
    id: int

class TaskUpdate(BaseModel):
    title: str
    description:str
    done: bool
"""
class Task(BaseModel):
    title: str
    description: Optional[str] = None
    done: Optional[bool] = False

class TaskCom(BaseModel):
    
    done: Optional[bool] = False

class TaskDB(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    done = Column(Integer, default=0)

# Create the tasks table in the database
Base.metadata.create_all(bind=engine)

# Define the API endpoints
@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/tasks")
async def read_tasks():
    with SessionLocal() as session:
        tasks = session.query(TaskDB).all()
        return tasks

"""@app.post("/tasks")
async def create_task(title: str, description: str):
    with SessionLocal() as session:
        task = TaskDB(title=title, description=description)
        session.add(task)
        session.commit()
        session.refresh(task)
        return task"""


@app.post("/tasks")
async def create_task(task: Task):
    with SessionLocal() as session:
        db_task = TaskDB(title=task.title, description=task.description)
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task


@app.put("/tasks/{task_id}")
async def update_task(task_id: int, task: Task):
    with SessionLocal() as session:
        db_task = session.query(TaskDB).filter(TaskDB.id == task_id).first()
        if not db_task:
            raise HTTPException(status_code=404, detail="Task not found")
        #if task:
        db_task.title = task.title
        db_task.description = task.description
        db_task.done = task.done
        session.commit()
        session.refresh(db_task)
        return db_task

@app.put("/tasks-com/{task_id}")
async def update_task(task_id: int, task: TaskCom):
    with SessionLocal() as session:
        db_task = session.query(TaskDB).filter(TaskDB.id == task_id).first()
        if not db_task:
            raise HTTPException(status_code=404, detail="Task not found")
        #if task:
        #db_task.title = task.title
        #db_task.description = task.description
        db_task.done = task.done
        session.commit()
        session.refresh(db_task)
        return db_task


"""@app.put("/tasks/task_id}")
async def update_task(task_id: int, title: str = None, description: str = None, done: int = None):
    with SessionLocal() as session:
        task = session.query(TaskDB).filter(TaskDB.id == task_id).first()
        if not task:
            return {"error": "Task not found"}
        if title:
            task.title = title
        if description:
            task.description = description
        if done is not None:
            task.done = done
        session.commit()
        session.refresh(task)
        return task"""

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    with SessionLocal() as session:
        task = session.query(TaskDB).filter(TaskDB.id == task_id).first()
        if not task:
            return {"error": "Task not found"}
        session.delete(task)
        session.commit()
        return {"message": "Task deleted successfully"}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)

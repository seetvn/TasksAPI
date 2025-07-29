from fastapi import APIRouter, Depends, HTTPException
from typing import List
from schemas import TaskCreate, TaskRead, TaskUpdate
from tasks import utils
from auth.dependencies import get_current_user
from models import User

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskRead)
async def create_task(task: TaskCreate, current_user: User = Depends(get_current_user)):
    return await utils.create_task_for_user(task, current_user.id)


@router.get("/", response_model=List[TaskRead])
async def get_tasks(current_user: User = Depends(get_current_user)):
    return await utils.get_user_tasks(current_user.id)


@router.get("/{task_id}", response_model=TaskRead)
async def get_task(task_id: int, current_user: User = Depends(get_current_user)):
    task = await utils.get_user_task_by_id(task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=TaskRead)
async def update_task(task_id: int, update: TaskUpdate, current_user: User = Depends(get_current_user)):
    task = await utils.update_task_status_for_user(task_id, current_user.id, update)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    print("Task updated:", task)
    return task


@router.delete("/{task_id}")
async def delete_task(task_id: int, current_user: User = Depends(get_current_user)):
    success = await utils.delete_user_task(task_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task deleted"}

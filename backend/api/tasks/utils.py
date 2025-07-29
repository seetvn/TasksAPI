from sqlmodel import select
from models import Task, TaskStatus
from database import async_session


async def create_task_for_user(task_data, user_id: int) -> Task:
    """
    Create a new task for a specific user.

    Args:
        task_data: The data for the new task.
        user_id (int): The ID of the user.

    Returns:
        Task: The created Task object.
    """
    async with async_session() as session:
        task = Task(**task_data.dict(), user_id=user_id)
        session.add(task)
        await session.commit()
        await session.refresh(task)
        return task


async def get_user_tasks(user_id: int) -> list[Task]:
    """
    Retrieve all tasks belonging to a specific user.

    Args:
        user_id (int): The ID of the user.

    Returns:
        list[Task]: A list of Task objects.
    """
    async with async_session() as session:
        result = await session.execute(select(Task).where(Task.user_id == user_id))
        return result.scalars().all()


async def get_user_task_by_id(task_id: int, user_id: int) -> Task | None:
    """
    Retrieve a specific task by its ID for a given user.

    Args:
        task_id (int): The ID of the task.
        user_id (int): The ID of the user.

    Returns:
        Task | None: The Task object if found, else None.
    """
    async with async_session() as session:
        result = await session.execute(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        )
        return result.scalar_one_or_none()


async def update_task_status_for_user(task_id: int, user_id: int, new_status: TaskStatus) -> Task | None:
    """
    Update the status of a specific task for a given user.

    Args:
        task_id (int): The ID of the task.
        user_id (int): The ID of the user.
        new_status (TaskStatus): The new status to set.

    Returns:
        Task | None: The updated Task object if found, else None.
    """
    async with async_session() as session:
        result = await session.execute(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        )
        task = result.scalar_one_or_none()
        if not task:
            print(" === Task not found or does not belong to user === ")
            return None
        print(new_status)
        task.status = new_status
        await session.commit()
        await session.refresh(task)
        return task


async def delete_user_task(task_id: int, user_id: int) -> bool:
    """
    Delete a specific task for a given user.

    Args:
        task_id (int): The ID of the task.
        user_id (int): The ID of the user.

    Returns:
        bool: True if the task was deleted, False otherwise.
    """
    async with async_session() as session:
        result = await session.execute(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        )
        task = result.scalar_one_or_none()
        if not task:
            return False
        await session.delete(task)
        await session.commit()
        return True


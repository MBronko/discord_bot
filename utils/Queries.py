from utils.Models import *
from sqlalchemy.orm import Session


# TodoList
def get_all_todo_lists(session: Session, server_id: int) -> list[Todolist]:
    return session.query(Todolist).where(Todolist.server_id == server_id).all()


def get_todo_list(session: Session, server_id: int, todo_id: str) -> Todolist:
    return session.query(Todolist).where(Todolist.server_id == server_id, Todolist.todo_id == todo_id).first()


def get_todo_list_by_msg(session: Session, server_id: int, msg_id: id) -> Todolist:
    return session.query(Todolist).where(Todolist.server_id == server_id, Todolist.msg_id == msg_id).first()


def get_todo_sects(session: Session, server_id: int, todo_id: str) -> list[TodoSect]:
    return session.query(TodoSect).where(TodoSect.server_id == server_id, TodoSect.todo_id == todo_id).order_by(
        TodoSect.timestamp).all()

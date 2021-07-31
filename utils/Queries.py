from utils.Models import Rules, Leaguechamps, Todolist, TodoSect
from sqlalchemy.orm import Session
from sqlalchemy import column, func


# ChampRoll
def get_champ_by_name(session: Session, name: str) -> Leaguechamps:
    return session.query(Leaguechamps).where(Leaguechamps.name == name).first()


def get_champs_by_lane_not_in_list(session: Session, lane: column, used_champs: list[str], limit: int) -> list[
    Leaguechamps]:
    return session.query(Leaguechamps).where(lane, Leaguechamps.name.not_in(used_champs)).order_by(func.random()).limit(
        limit).all()


def get_champs_by_lane(session: Session, lane: column, limit: int) -> list[Leaguechamps]:
    return session.query(Leaguechamps).where(lane).order_by(func.random()).limit(limit).all()


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

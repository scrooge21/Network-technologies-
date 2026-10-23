from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from database.connection import get_session
from models.events import Event, EventUpdate

event_router = APIRouter(tags=["Events"])


@event_router.get("/", response_model=List[Event], summary="Список всех событий",
                  description="Возвращает все события из базы данных.")
async def retrieve_all_events(session: Session = Depends(get_session)) -> List[Event]:
    return session.exec(select(Event)).all()


@event_router.get("/{id}", response_model=Event, summary="Получить событие по ID",
                  responses={404: {"description": "Событие с таким ID не найдено"}})
async def retrieve_event(id: int, session: Session = Depends(get_session)) -> Event:
    event = session.get(Event, id)
    if event:
        return event
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event with supplied ID does not exist")


@event_router.post("/new", summary="Создать событие",
                   description="Добавляет событие в базу. ID назначается автоматически.")
async def create_event(new_event: Event, session: Session = Depends(get_session)) -> dict:
    session.add(new_event)
    session.commit()
    session.refresh(new_event)
    return {"message": "Event created successfully", "id": new_event.id}


@event_router.put("/edit/{id}", response_model=Event, summary="Изменить событие",
                  description="Меняет только те поля, которые переданы в теле запроса.",
                  responses={404: {"description": "Событие с таким ID не найдено"}})
async def update_event(id: int, new_data: EventUpdate, session: Session = Depends(get_session)) -> Event:
    event = session.get(Event, id)
    if event:
        for key, value in new_data.model_dump(exclude_unset=True).items():
            setattr(event, key, value)
        session.add(event)
        session.commit()
        session.refresh(event)
        return event
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event with supplied ID does not exist")


@event_router.delete("/delete/{id}", summary="Удалить событие по ID",
                     responses={404: {"description": "Событие с таким ID не найдено"}})
async def delete_event(id: int, session: Session = Depends(get_session)) -> dict:
    event = session.get(Event, id)
    if event:
        session.delete(event)
        session.commit()
        return {"message": "Event deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event with supplied ID does not exist")
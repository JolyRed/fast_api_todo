from fastapi import FastAPI, Depends, Request, HTTPException, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import TodoItem
from schemas import TodoItemCreate
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=templates.TemplateResponse)
def read_items(request: Request, db: Session = Depends(get_db)):
    items = db.query(TodoItem).all()
    return templates.TemplateResponse("index.html", {"request": request, "items": items})

@app.post("/add/")
def create_item(title: str = Form(...), description: str = Form(...), db: Session = Depends(get_db)):
    db_item = TodoItem(title=title, description=description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return RedirectResponse(url='/', status_code=302)

@app.post("/delete/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(TodoItem).filter(TodoItem.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return RedirectResponse(url='/', status_code=302)

@app.post("/edit/{item_id}")
def edit_item(item_id: int, title: str = Form(...), description: str = Form(...), completed: bool = Form(False), db: Session = Depends(get_db)):
    db_item = db.query(TodoItem).filter(TodoItem.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db_item.title = title
    db_item.description = description
    db_item.completed = completed
    db.commit()
    return RedirectResponse(url='/', status_code=302)

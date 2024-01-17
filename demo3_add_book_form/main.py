from datetime import date
from typing import Annotated
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastui import FastUI, AnyComponent, prebuilt_html, components as c
from fastui.components.display import DisplayMode, DisplayLookup
from fastui.events import BackEvent, GoToEvent
from fastui.forms import fastui_form
from pydantic import BaseModel, Field

app = FastAPI()

# Models
class Book(BaseModel):
    id: int
    name: str
    publish_date: date = Field(title='Publish date')

class BookForm(BaseModel):
    name: str = Field(title='Name', min_length=3)
    publish_date: date = Field(title='Publish date')


# Define books list (Should be a database in real app)
books = [
    Book(id=1, name='Clean Code', publish_date=date(2008, 8, 1)),
    Book(id=2, name='The Pragmatic Programmer', publish_date=date(2019, 1, 1)),
    Book(id=3, name='The Phoenix Project', publish_date=date(2014, 1, 1)),
    Book(id=4, name="Don't Make Me Think", publish_date=date(2000, 1, 1)),
]

# Endpoints
@app.get("/api/", response_model=FastUI, response_model_exclude_none=True)
def books_table_page() -> list[AnyComponent]:
    return [
        c.Page(  # Page provides a basic container for components
            components=[
                c.Heading(text='Books', level=2),  # renders `<h2>Books</h2>`
                c.Table( # renders to <table>
                    data=books,
                    columns=[
                        DisplayLookup(field='name', on_click=GoToEvent(url='/books/{id}/')),
                        DisplayLookup(field='publish_date', mode=DisplayMode.date),
                    ]
                ),
                c.Div(components=[
                    c.Button(
                        text="Add Book",
                        on_click=GoToEvent(url='/add-book/')
                    )
                ])
            ]
        ),
    ]

@app.get('/api/add-book/', response_model=FastUI, response_model_exclude_none=True)
def add_book_page():
    return [
        c.Page(components=[
            c.Heading(text='Add Book', level=2),
            c.Paragraph(text="Add book to the list"),
            c.Link(components=[c.Text(text='Back')], on_click=BackEvent()),
            c.ModelForm(model=BookForm, submit_url='/api/add-book/')
        ])
    ]

@app.post('/api/add-book/')
def add_pook(form: Annotated[BookForm, fastui_form(BookForm)]):
    _id = books[-1].id + 1
    book = Book(id=_id, **form.model_dump())
    books.append(book)
    return [c.FireEvent(event=GoToEvent(url='/'))]

@app.get("/api/books/{book_id}/", response_model=FastUI, response_model_exclude_none=True)
def book_details_page(book_id: int) -> list[AnyComponent]:
    try:
        book = next(b for b in books if b.id == book_id)
    except StopIteration:
        raise HTTPException(status_code=404, detail="Book not found")
    return [
        c.Page(
            components=[
                c.Heading(text=book.name, level=2),
                c.Link(components=[c.Text(text='Back')], on_click=BackEvent()),
                c.Details(data=book),
            ]
        ),
    ]

@app.get('/{path:path}')
async def html_landing() -> HTMLResponse:
    """Simple HTML page which serves the React app, comes last as it matches all paths."""
    return HTMLResponse(prebuilt_html(title='FastUI Demo'))
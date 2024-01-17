from datetime import date
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastui import FastUI, AnyComponent, prebuilt_html, components as c
from fastui.components.display import DisplayMode, DisplayLookup
from pydantic import BaseModel, Field

app = FastAPI()

# Data Models
class Book(BaseModel):
    id: int
    name: str
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
                c.Heading(text='Books', level=2),  # renders `<h2>Users</h2>`
                c.Table( # renders to <table>
                    data=books,
                ),
            ]
        ),
    ]

@app.get('/{path:path}')
async def html_landing() -> HTMLResponse:
    """Simple HTML page which serves the React app, comes last as it matches all paths."""
    return HTMLResponse(prebuilt_html(title='FastUI Demo'))
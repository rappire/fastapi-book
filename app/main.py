from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.models import mongodb
import app.config as config
from app.models.book import BookModel
from app.scraper import BookScraper

app = FastAPI()
templates = Jinja2Templates(directory=config.BASE_DIR / "app" / "templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):

    return templates.TemplateResponse(
        "./index.html", {"request": request, "title": "BOOK"}
    )


@app.get("/search", response_class=HTMLResponse)
async def search(request: Request, keyword: str):
    if not keyword:
        return templates.TemplateResponse("./index.html", {"request": request})

    if await mongodb.engine.find_one(BookModel, BookModel.keyword == keyword):
        books = await mongodb.engine.find(BookModel, BookModel.keyword == keyword)
        return templates.TemplateResponse(
            "./index.html", {"request": request, "books": books}
        )

    book_scraper = BookScraper()
    books = await book_scraper.scraper(keyword, 10)
    book_models = []
    for book in books:
        book_model = BookModel(
            keyword=keyword,
            publisher=book["publisher"],
            price=int(book["discount"]),
            image=book["image"],
            link=book["link"],
        )
        book_models.append(book_model)
    await mongodb.engine.save_all(book_models)

    return templates.TemplateResponse(
        "./index.html", {"request": request, "books": book_models}
    )


@app.on_event("startup")
def on_app_start():
    mongodb.connect()


@app.on_event("shutdown")
async def on_app_shutdown():
    mongodb.disconnect()

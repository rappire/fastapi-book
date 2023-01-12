from odmantic import Model


class BookModel(Model):
    keyword: str
    publisher: str
    price: int
    image: str
    link: str

    class Config:
        collection = "books"

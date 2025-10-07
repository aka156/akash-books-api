import os
from fastapi import FastAPI, status
from pydantic import BaseModel, Field
import uuid
import json
import logging

app = FastAPI()

logging.basicConfig(level = logging.DEBUG,
                           format='%(asctime)s - %(levelname)s - %(message)s')
logger =logging.getLogger(__name__)

DATA_FILE = "data/books-data.json"

books_db:list[dict[str,any]] = []

def _load_data():
    global books_db
    try:
        with open(DATA_FILE,'r') as f:
            books_db = json.load(f)
        logger.info(f"Successfully loaded {len(books_db)} records from {DATA_FILE}")
    except FileNotFoundError:
        logger.warning(f"{DATA_FILE} not found.Initializing with empty database")
        books_db =[]
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON from {DATA_FILE}. Initializing with empty database.")
        books_db = []

def _save_data():
    try:
        with open(DATA_FILE, 'w') as f:
            # Use indent=2 for readability in the file
            json.dump(books_db, f, indent=2)
        logger.info(f"Successfully saved {len(books_db)} records to {DATA_FILE}")
    except Exception as e:
        logger.error(f"Failed to save data to {DATA_FILE}: {e}")

_load_data()
# logger.info(f"data:  {books_db}")

class Author(BaseModel):
    name: str = Field(min_length=3, description="The full name of the author.")
    country : str = Field(min_length= 2,max_length=50,description="The authors country of origin.")


class BookBase(BaseModel):
    title:str = Field(min_lentgh = 1,description="The title of the book.")
    year: int = Field(gt=1980,It=2025,description="The publication year of the book.")
    author:Author

class Book(BookBase):
    id:  uuid.UUID = Field(description="The unique identifier for the book.")

@app.get("/healthz", status_code=status.HTTP_200_OK)
def health_check():
    file_exists = os.path.exists(DATA_FILE)

    status_detail = {
        "status":"OK",
        "service":"Book CRUD API",
        "data_file_status":"Available" if
          file_exists else "Missing (check deployment volume)"
        }
    
    logger.info(f"health check performed. Data file status:{status_detail['data_file_status']}")
    return status_detail

@app.post("/books",response_model=Book, status_code=status.HTTP_201_CREATED)
def create_book(book_data:BookBase):

    new_id = uuid.uuid4()


    new_book=book_data.model_dump()
    new_book["id"] = str (new_id)

    books_db.append(new_book)
    _save_data()

    logger.info(f"Book created with ID:{new_book['id']}")
    return new_book
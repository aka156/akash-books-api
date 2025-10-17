import requests
import json
import time
import os
import uuid



BASE_URL = "http://127.0.0.1:8000" #localhost base url
BOOK_ENDPOINT = f"{BASE_URL}/books/" #post endpoint
HEADERS = {"Content-Type": "application/json"}
NEW_BOOK_ID = ""

def print_response(title, response, expected_status):
    """Helper function to print formatted response details."""
    print(f"\n--- {title} ---")
    print(f"URL: {response.url}")
    print(f"Method: {response.request.method}")
    print(f"Expected Status: {expected_status}, Received Status: {response.status_code}")
    try:
        print(f"Response Body: {json.dumps(response.json(), indent=2)}")
    except requests.exceptions.JSONDecodeError:
        print(f"Response Body: {response.text}")
    print("-" * 30)
    return response


def test_create_book():
    """Tests the POST /books/ endpoint."""
    global NEW_BOOK_ID

    print("\n\n##################### 1. TEST CREATE (POST) #####################")
    new_book_data = {
        "title": "Cosmic Rails",
        "year": 2024,
        "author": {
            "name": "Alex K.",
            "country": "USA"
        }
    }
    
    response = requests.post(BOOK_ENDPOINT, headers=HEADERS, json=new_book_data)
    response = print_response("POST: Create New Book", response, 201)
    
    if response.status_code == 201:
        NEW_BOOK_ID = response.json().get("id")
        print(f"Successfully created book. Captured ID: {NEW_BOOK_ID}")
    
    return response.status_code == 201


def test_read_all():
    """Tests the GET /books/ endpoint."""
    print("\n\n##################### . TEST READ ALL (GET) #####################")
    response = requests.get(BOOK_ENDPOINT)
    return print_response("GET: Read All Books", response, 200).status_code == 200

def update_all():
      
      print("\n\n##################### . update the book (put) #####################")
      
      book_id = "a9b8c7d6-1f0e-47b1-b541-7755c6f89a1b"
      url = f"http://127.0.0.1:8000/books/{book_id}"
      
      book_data = {
        "title": "1985",
        "year": 1990,
        "author": {
        "name": "George rowell",
        "country": "UAK"
         }
    }
      response = requests.put(url, headers=HEADERS, json=book_data)
      response = print_response("PUT: Updated existing book", response, 200)
    
      if response.status_code == 200:
            book_id = response.json().get("id")
            print(f"Successfully updated book. With ID: {book_id}")
      
      else:
           print(f"Book not found with ID {book_id}")
           
        
      return response.status_code == 200

    #   if response.status_code == 200:
    #      print_response("PUT: updated book", response, 200)
    #   else:
    #      print(f"Failed to update book. Status: {response.status_code}, Response: {book_id} not found")
      
      
#  print_response()
# test_create_book()
# test_read_all()
update_all()

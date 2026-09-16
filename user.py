## This module contains the user interface for the library system. 
# It allows users to search for books, borrow books, and return books.

## Import the necessary functions from the admin module. 
# Replace "function_name1" with the actual function names you want to import.

from admin import (
    load_library,
    save_library,
    find_book
)



## Search books by category.
## This function should return book IDs that match the given category.
def books_in_category(
    books,
    category
):
    category = str(category).strip().lower()
    if not category:
        return []
    result = []
    for book_id, book in books.items():
        book_category = str(book.get("category","")).strip().lower()
        if book_category == category:
            result.append(book_id)
            
    return result
        
    


## Search books by full or partial title.
## This function should return book IDs that match the given title or part of the title.
def search_by_title(
    books,
    search_text
):
    search_text = str(search_text).strip().lower()
    if not search_text:
        return []

    result = []
    for book_id, book in books.items():
        book_title = str(book.get("title","")).strip().lower()
        if search_text in book_title:
            result.append(book_id)
            
    return result
    


## Create logic to let users borrow books.
## The function should check if the book is available or on loan, or if the borrower name is provided.
## If the book is not found, then return "BOOK_NOT_FOUND"
## If the borrower name is empty, then return "EMPTY_NAME"
## If the book is not available, then return "NOT_AVAILABLE"
## If the book is successfully borrowed, then return "OK"
def borrow_book(
    books,
    loans,
    search_text,
    borrower
):
    book_id = find_book(books,search_text)

    if book_id is None:
        return "BOOK_NOT_FOUND"

    borrower = str(
        borrower
    ).strip()

    if not borrower:
        return "EMPTY_NAME"

    book = books[
        book_id
    ]

    on_loan = False

    for loan in loans:

        loan_book_id = str(
            loan.get(
                "book_id",
                ""
            )
        ).strip().lower()

        if (
            loan_book_id
            == book_id.lower()
        ):
            on_loan = True
            break
    if (
        not book.get(
            "available",
            False
        )
        or on_loan
    ):
        return "NOT_AVAILABLE"
    book[
        "available"
    ] = False
    loans.append(
        {
            "book_id": book_id,
            "borrower": borrower
        }
    )
    return "OK"



    


## Create logic to let users return books.
## The function should check if the book is on loan, or if the borrower name is provided
## If the book is not found, then return "BOOK_NOT_FOUND"
## If the borrower name is empty, then return "EMPTY_NAME"
## If the book is not on loan, then return "NOT_ON_LOAN"
## If the book is successfully returned, then return "OK"

def return_book(
    books,
    loans,
    book_title,
    borrower
):
    book_id = find_book(books,book_title)
    if book_id is None:
        return "BOOK_NOT_FOUND"

    borrower = str(
        borrower
    ).strip()

    if not borrower:
        return "EMPTY_NAME"

    on_loan = False

    for loan in loans:

        loan_book_id = str(
            loan.get(
                "book_id",
                ""
            )
        ).strip().lower()

        if (
            loan_book_id
            == book_id.lower()
        ):
            on_loan = True
            break
    if not on_loan:
        return "NOT_ON_LOAN"
    book = books[
        book_id
    ]
    book[
        "available"
    ] = True
    loans.remove(
        {
            "book_id": book_id,
            "borrower": borrower
        }
    )
    return "OK"

    



## The main function that runs the user interface for the library system.
## The function must first load the library data from a JSON file, then display a menu for the user to select options.
## The options include searching for books by title or category, borrowing a book, returning a book, and exiting the program.
## When the user selects an option, the corresponding function is called to perform the action.
## The program continues to display the menu until the user chooses to exit, at which point the library data is saved back to the JSON file.
## The main function should also handle invalid selections by displaying an error message and prompting the user to select again.
def main():
    filename = "library.json"
    data = load_library(filename)
    books = data.get("books",{})
    loans = data.get("loans",[])
    library = data.get("library",{})
    print("Library loaded successfully")
    print("-------------------------------------------------- ")
    print("LIBRARY USER SYSTEM")
    print("-------------------------------------------------- ")
    while True: 
        print("Available options:")
        print("1. Search books by title")
        print("2. Search books by category")
        print("3. Borrow a book")
        print("4. Return a book")
        print("5. Exit the program")
        print("-------------------------------------------------- ")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            search_text = input("Enter the book title to search: ").strip()
            result = search_by_title(books,search_text)
            if not result:
                print("No books found")
            else:
                print("Books found:")
                for book_id in result:
                    book = books[book_id]
                    if book["available"]:
                        status = "AVAILABLE"
                    else:
                        status = "ON LOAN"
                    print(book_id,book["title"],book["category"],status) 
        elif choice == "2":
            search_text = input("Enter the book category to search: ").strip()
            result = search_by_category(books,search_text)
            if not result:
                print("No books found")
            else:
                print("Books found:")
                for book_id in result:
                    book = books[book_id]
                    if book["available"]:
                        status = "AVAILABLE"
                    else:
                        status = "ON LOAN"
                    print(book_id,book["title"],book["category"],status) 
        elif choice == "3":
            book_title = input("Enter the book title to borrow: ").strip()
            borrower = input("Enter your name: ").strip()
            result = borrow_book(books,loans,book_title,borrower)
            if result == "OK":
                print("Book borrowed successfully")
            else:
                print(result)
        elif choice == "4":
            book_title = input("Enter the book title to return: ").strip()
            borrower = input("Enter your name: ").strip()
            result = return_book(books,loans,book_title,borrower)
            if result == "OK":
                print("Book returned successfully")
            else:
                print(result)

        elif choice == "5":
            save_library(data,filename)
            print("Library data saved successfully")

            break

        else:
            print("Invalid choice. Please select again.")
                
if __name__ == "__main__":
    main()



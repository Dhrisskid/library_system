from services.library_service import LibraryService

class MainMenu:
    def __init__(self):
        self.service = LibraryService()

    def _search_and_select(self, search_func, query: str):
        books = search_func(query)
        if not books:
            print("No books found.")
            return None
        print("\nMatching books:")
        for idx, book in enumerate(books, 1):
            print(f"{idx}. {book.title} by {book.author}, Available: {book.available_copies}/{book.total_copies})")
        choice = input("\nSelect a book number (or 0 to cancel): ")
        try:
            idx = int(choice)
            if idx == 0:
                return None
            if 1 <= idx <= len(books):
                selected = books[idx-1]
                print("\n--- Book Details ---")
                print(f"Row number: {idx}")
                print(f"ISBN: {selected.isbn}")
                print(f"Title: {selected.title}")
                print(f"Author: {selected.author}")
                print(f"Category: {selected.category}")
                print(f"Total copies: {selected.total_copies}")
                print(f"Borrowed copies: {selected.borrowed_copies}")
                print(f"Available copies: {selected.available_copies}")
                return selected
            else:
                print("Invalid selection.")
                return None
        except ValueError:
            print("Invalid input.")
            return None

    def _search_menu(self):
        while True:
            print("\n--- Search Books ---")
            print("1. By Title")
            print("2. By Author")
            print("3. By Category")
            print("4. By ISBN (exact match)")
            print("0. Back to main menu")
            choice = input("Choose: ")
            match choice:
                case "1":
                    title = input("Enter title (or part): ")
                    self._search_and_select(self.service.search_books_by_title, title)
                case "2":
                    author = input("Enter author name: ")
                    self._search_and_select(self.service.search_books_by_author, author)
                case "3":
                    category = input("Enter category: ")
                    self._search_and_select(self.service.search_books_by_category, category)
                case "4":
                    isbn = input("Enter ISBN: ")
                    book = self.service.search_book_by_isbn(isbn)
                    if book:
                        print("\n--- Book Details ---")
                        print(f"ISBN: {book.isbn}")
                        print(f"Title: {book.title}")
                        print(f"Author: {book.author}")
                        print(f"Category: {book.category}")
                        print(f"Total copies: {book.total_copies}")
                        print(f"Borrowed copies: {book.borrowed_copies}")
                        print(f"Available copies: {book.available_copies}")
                    else:
                        print("Book not found.")
                case "0":
                    break
                case _:
                    print("Invalid option.")

    def run(self):
        while True:
            print("\nLIBRARY MANAGEMENT SYSTEM")
            print(" 1. Add book")
            print(" 2. Register user")
            print(" 3. Borrow book")
            print(" 4. Return book")
            print(" 5. Search books")
            print(" 6. Display borrowed books")
            print(" 7. Get all books")
            print(" 8. Get all users")
            print(" 9. Remove a user")
            print("10. Remove a book")
            print("11. Exit")
            choice = input("Pick an option: ")

            match choice:
                case "1":
                    try:
                        isbn = input("Enter ISBN: ")
                        title = input("Enter book title: ")
                        author = input("Enter author: ")
                        category = input("Enter category: ")
                        while True:
                            copies_input = input("Enter number of copies (or 9 to cancel): ")
                            if copies_input == "9":
                                print("Operation cancelled.")
                                break
                            try:
                                copies = int(copies_input)
                                if copies <= 0:
                                    print("Number of copies must be positive. Try again or press 9.")
                                    continue
                                self.service.add_book(isbn, title, author, category, copies)
                                print("Book added successfully")
                                break
                            except ValueError as e:
                                print(f"Invalid input: {e}. Try again or press 9.")
                    except ValueError as e:
                        print(f"Error: {e}")

                case "2":
                    try:
                        user_id = input("Enter user ID: ")
                        name = input("Enter user name: ")
                        username = input("Enter username: ")
                        self.service.register_user(user_id, name, username)
                        print("User registered successfully")
                    except ValueError as e:
                        print(f"Error: {e}")

                case "3":
                    try:
                        title = input("Enter book title: ")
                        username = input("Enter borrower username: ")
                        self.service.borrow_book(title, username)
                        print("Book borrowed successfully")
                    except ValueError as e:
                        print(f"Error: {e}")

                case "4":
                    try:
                        title = input("Enter book title: ")
                        username = input("Enter returner username: ")
                        self.service.return_book(title, username)
                        print("Book returned successfully")
                    except ValueError as e:
                        print(f"Error: {e}")

                case "5":
                    self._search_menu()

                case "6":
                    self.service.display_borrowed_books()

                case "7":
                    self.service.get_all_books()

                case "8":
                    self.service.get_all_users()

                case "9":
                    try:
                        username = input("Enter username of user to remove: ")
                        confirm = input(f"Are you sure you want to delete user '{username}'? (y/n): ")
                        if confirm.lower() == 'y':
                            self.service.delete_user(username)
                            print("User deleted successfully.")
                        else:
                            print("Deletion cancelled.")
                    except ValueError as e:
                        print(f"Error: {e}")

                case "10":
                    try:
                        isbn = input("Enter ISBN of book to remove: ")
                        confirm = input(f"Are you sure you want to delete the book with ISBN {isbn}? (y/n): ")
                        if confirm.lower() == 'y':
                            self.service.delete_book(isbn)
                            print("Book deleted successfully.")
                        else:
                            print("Deletion cancelled.")
                    except ValueError as e:
                        print(f"Error: {e}")

                case "11":
                    print("Bye.")
                    break

                case _:
                    print("Invalid option. Please try again.")
# 1. Import the FastAPI app you already built in api/app.py
from api.app import app

# 2. Import your CLI menu
from menu.main_menu import MainMenu

# 3. CLI execution block
# This ensures the menu ONLY runs if you type `python main.py` in the terminal,
# but stays out of the way when Uvicorn runs `uvicorn main:app`.
if __name__ == "__main__":
    menu = MainMenu()
    menu.run()
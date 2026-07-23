from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import books, users, borrow, chat


app = FastAPI(title="Library Management System API")

app.add_middleware(
    CORSMiddleware,
    # Replace the "*" with your EXACT frontend URL (no slash at the end)
    allow_origins=["https://scaling-meme-wr7x44j6qvgx29r64-5500.app.github.dev"],
    allow_credentials=True, 
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(books.router)
app.include_router(users.router)
app.include_router(borrow.router)
app.include_router(chat.router)




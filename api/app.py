from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import books, users, borrow

app = FastAPI(title="Library Management System API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(books.router)
app.include_router(users.router)
app.include_router(borrow.router)



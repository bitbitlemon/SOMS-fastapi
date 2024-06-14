from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from .views import user as user_view
from .views import entity as entity_view


app = FastAPI(
    title="SOMS-fastapi",
    description="",
    version="0.1.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_view.router)
app.include_router(entity_view.router)


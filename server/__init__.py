from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

import config

app = FastAPI(
    title="SOMS-fastapi",
    description="",
    version="0.1.0",
    debug=config.DEBUG
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


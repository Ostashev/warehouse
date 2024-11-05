import uvicorn
from fastapi import FastAPI

from app.api.routers import main_router
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

app = FastAPI(root_path=settings.api_root_path)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(main_router)


if __name__ == "main":
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.routers import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("File API starting...")
    yield
    print("File ETL API shutting down...")


app = FastAPI(
    title="ETL File event_driven Data pipeline",
    version="1.0.0",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ONLY ONE ROUTER
app.include_router(router, prefix="/api")


@app.get("/")
def root():
    return {"message": "ETL system is running"}


@app.get("/health")
def health():
    return {"status": "ok"}
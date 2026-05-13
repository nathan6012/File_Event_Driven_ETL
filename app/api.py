from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app import routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 🔹 startup logic (DB, Redis, etc. later)
    print("File API starting...")

    yield

    # 🔹 shutdown logic
    print("File ETL API  shutting down...")


# =========================
# APP INIT
# =========================
app = FastAPI(
    title="ETL File event_driven Data pipeline",
    version="1.0.0",
    lifespan=lifespan
)


# =========================
# CORS (frontend support)
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later restrict to Streamlit domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Upload csv file router endpoint 
app.include_router(routers.router, prefix="/routers", tags=["Router"])


# =========================
# ROOT + HEALTH
# =========================
@app.get("/")
def root():
    return {"message": "ETL system is running"}


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}
    
#uvicorn app.api:app --reload
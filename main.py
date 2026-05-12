from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import database, models
from .routers import auth_router, farmer_router, ai_router, sos_router

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Madhu-Siri API",
    description="Backend for Bee Farmer Harmony App",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(farmer_router.router)
app.include_router(ai_router.router)
app.include_router(sos_router.router)

@app.get("/")
def root():
    return {"message": "Welcome to Madhu-Siri API"}

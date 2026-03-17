from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
<<<<<<< HEAD
from app.routers import auth, trips
=======
from app.routers import auth
>>>>>>> 37b5bafc8839473980d31976cb119392abc83d47

app = FastAPI(title="Travel Planner API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
<<<<<<< HEAD
app.include_router(trips.router)
=======
>>>>>>> 37b5bafc8839473980d31976cb119392abc83d47

@app.get("/health")
async def health():
    return {"status": "ok", "version": "1.0.0"}
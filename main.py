from fastapi import FastAPI
from db.tables import create_tables
from routers import posts, users



async def lifespan(app: FastAPI):
    print('Check database...')
    yield
    create_tables()

app = FastAPI(lifespan=lifespan)


app.include_router(users.router)
app.include_router(posts.router)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
from fastapi import FastAPI
from routers import posts, users


app = FastAPI()


app.include_router(users.router)
app.include_router(posts.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}

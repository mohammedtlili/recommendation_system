import sys
import uvicorn
from fastapi import FastAPI
from routes import router
from db import engine, Base

Base.metadata.create_all(bind=engine)

sys.stdout.write("Doing nothing ")


app = FastAPI()

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

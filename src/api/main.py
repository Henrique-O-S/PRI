from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/post")
def post_data(item: dict):
    # Process the data received in POST request
    return {"Received data": item}


"""
HOW TO RUN:
uvicorn main:app --reload --port 8001
"""
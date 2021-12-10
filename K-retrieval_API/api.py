from fastapi import FastAPI

app = FastAPI()

@app.post("/source")
async def load_source(source:str):
    pass

@app.post("/search")
async def search(query:str):
    pass

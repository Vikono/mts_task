import json
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from info_retrieval import get_all_tariffs
from parcer import start
from fastapi.responses import FileResponse
import uvicorn
import logging

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # maybe should be rewritten
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/tariffs")
async def load_everything():
    tariffs = get_all_tariffs()
    # json_obj = json.dumps(tariffs)
    # print(json_obj)
    return tariffs


@app.get("/tariffs/parce")
async def parce_all_tariffs_and_return_new_version():
    start()
    tariffs = get_all_tariffs()
    return tariffs


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8012, lifespan='on', log_level="info")
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

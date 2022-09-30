
import string
from fastapi import FastAPI,Request
import random
import string
from pydantic import BaseModel



# importing the module
from pytube import YouTube


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/download")
async def downloadFile(request:Request):
    body =  await request.json()
    print(body["Link"])
    link = body["Link"]
    
  
    try:
        yt = YouTube(link)
        yt.streams.filter(adaptive=True, file_extension='mp4').get_by_itag(137).download()
    except:
        return {"error":"Connection Error"}  # to handle exception


  
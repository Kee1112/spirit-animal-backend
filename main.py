from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()


app.mount("/static", StaticFiles(directory= "spirit-animal/frontend/static"), name="static") #this simply takes care of static files like css and js 

@app.get("/")
def file():
    return FileResponse("frontend/index.html") # html is not a static file so we serve it like this 


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

def get_spirit_animal(vowel_count : int):
    if vowel_count <= 2:
        return "Phoenix 🔥"
    elif vowel_count <= 4:
        return "Dragon 🐉"
    elif vowel_count <= 6:
        return "Horse 🐎"
    else:
        return "Unicorn 🦄"
    
class NameRequest(BaseModel): #better to use Basemodel coz this is how body is sent through requests(otherwise could get confused to query or url params)
    name : str

@app.post("/spirit-animal")
def spirit_animal(data  : NameRequest): #data is the name ur giving to the namerequest type
    vowels = "aeiouAEIOU"
    vowel_count = sum(1 for c in data.name if c in vowels) # to access in name from the data object we use data.name
    animal = get_spirit_animal(vowel_count)
    return {
        "name" : data.name,
        "vowel_count" : vowel_count,
        "spirit_animal" : animal
    }


from fastapi import FastAPI
from pydantic import BaseModel
from services.openai_service import extract_diagnostico
from core.model import analyze

class Item(BaseModel):
 comment: str


app = FastAPI() # nombre de la iinstancia

@app.post("/items")
def crear_item(item: Item):
 response_ai = extract_diagnostico(item.comment)
 response_reglas = analyze(item.comment).raw_score

 if response_reglas < 1: 
        response_lexicon = 0
 else: 
        response_lexicon = 1
 response = max(response_ai, response_lexicon)
 
 return {
  "item":  response
 }
from fastapi import FastAPI


import api_model

app = FastAPI()


@app.get("/")
def read_root():
  return {"Hello": "World"}


@app.post("/recommendation")
def recommendation(req: api_model.RecommendationRequest):
  return req

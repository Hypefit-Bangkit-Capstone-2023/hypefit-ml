from fastapi import FastAPI
from api_model import RecommendationRequest
from api_utils import get_image_url
from dominant_colors import get_dominant_colors, rgb_to_hsv
from fuzzy_color import FuzzyColor
from color_matching import ColorMatching
import os
import uvicorn
from dotenv import load_dotenv

load_dotenv()


app = FastAPI()
fc = FuzzyColor()


@app.get("/")
def read_root():
  return {"Hello": "World"}


@app.post("/recommendation")
def recommendation(req: RecommendationRequest):
  matches = []

  dominant_colors = {
    "tops": {},
    "bottoms": {},
    "shoes": {}
  }

  color_descriptions = {
    "tops": {},
    "bottoms": {},
    "shoes": {}
  }

  for top_key in req.top_keys:
    top_color, _ = get_dominant_colors(get_image_url(top_key))[0]
    dominant_colors["tops"][top_key] = top_color.tolist()
    top_color_desc = fc.get_color_description(*rgb_to_hsv(top_color))
    color_descriptions["tops"][top_key] = top_color_desc

  for bottom_key in req.bottom_keys:
    bottom_color, _ = get_dominant_colors(get_image_url(bottom_key))[0]
    dominant_colors["bottoms"][bottom_key] = bottom_color.tolist()
    bottom_color_desc = fc.get_color_description(*rgb_to_hsv(bottom_color))
    color_descriptions["bottoms"][bottom_key] = bottom_color_desc

  for shoe_key in req.shoe_keys:
    shoe_color, _ = get_dominant_colors(get_image_url(shoe_key))[0]
    dominant_colors["shoes"][shoe_key] = shoe_color.tolist()
    shoe_color_desc = fc.get_color_description(*rgb_to_hsv(shoe_color))
    color_descriptions["shoes"][shoe_key] = shoe_color_desc

  for top_key in req.top_keys:
    top_color = dominant_colors["tops"][top_key]
    top_color_desc = color_descriptions["tops"][top_key]

    for bottom_key in req.bottom_keys:
      bottom_color = dominant_colors["bottoms"][bottom_key]
      bottom_color_desc = color_descriptions["bottoms"][bottom_key]

      for shoe_key in req.shoe_keys:
        shoe_color = dominant_colors["shoes"][shoe_key]
        shoe_color_desc = color_descriptions["shoes"][shoe_key]

        cm = ColorMatching([
          top_color_desc,
          bottom_color_desc,
          shoe_color_desc
        ])

        valid_matches = cm.get_all_valid_matches()

        matches.append({
          "image_keys": [top_key, bottom_key, shoe_key],
          "dominant_colors": [top_color, bottom_color, shoe_color],
          "color_descriptions": [top_color_desc, bottom_color_desc, shoe_color_desc],
          "valid_matches": valid_matches,
        })

  return matches


port = int(os.environ.get("PORT", 8000))
host = os.environ.get("HOST", '0.0.0.0')
if __name__ == "__main__":
  uvicorn.run(app, host=host, port=port)

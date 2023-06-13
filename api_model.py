from pydantic import BaseModel
from typing import List


class RecommendationRequest(BaseModel):
  top_keys: List[str]
  bottom_keys: List[str]
  shoe_keys: List[str]

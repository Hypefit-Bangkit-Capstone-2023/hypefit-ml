import os
import uvicorn
from dotenv import load_dotenv

load_dotenv()

port = int(os.environ.get("PORT", 8000))
if __name__ == "__main__":
  uvicorn.run('api:app', port=port, reload=True)

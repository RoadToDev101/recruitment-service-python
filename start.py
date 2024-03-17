import os
import uvicorn
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    uvicorn.run(
        "src.app.main:app",
        host="127.0.0.1",
        port=int(os.getenv("PORT", "8000")),
        reload=bool(os.getenv("ENV") == "development"),
        log_level=os.getenv("LOG_LEVEL", "debug"),
    )

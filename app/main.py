from api.routes import router as api_router
import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


@app.get("/")
def status():
    return "Server running"


app.include_router(api_router)


def main():
    uvicorn.run(app, host='0.0.0.0', port=8080, log_level='info')


if __name__ == "__main__":
    main()
    print(dir())

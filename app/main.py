from fastapi import FastAPI
import uvicorn
from api.routes import router as api_router

app = FastAPI()


@app.get("/")
def status():
    return "Server Running"


app.include_router(api_router)


def main():
    uvicorn.run(app, host='0.0.0.0', port=8080, log_level='info')


if __name__ == "__main__":
    main()
    print(dir())
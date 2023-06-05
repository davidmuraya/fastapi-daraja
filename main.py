
import uvicorn

from app import app as application
app = application


if __name__ == '__main__':
    uvicorn.run("app:app", port=5000)

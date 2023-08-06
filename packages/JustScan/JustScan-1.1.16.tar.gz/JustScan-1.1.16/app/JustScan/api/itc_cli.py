import uvicorn
import gunicorn
from .just_scan_api import app


def run_api():
    gunicorn.run(app, host="0.0.0.0", port=8000)


def main():
    run_api()


if __name__ == "__main__":
    main()

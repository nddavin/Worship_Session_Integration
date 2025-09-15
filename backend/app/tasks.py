from dotenv import load_dotenv
import os
from celery import Celery
from typing import Any, Dict

# Load environment variables from .env file
load_dotenv()

# Configure the Celery app using environment variables
app = Celery(
    __name__,
    broker=os.getenv('CELERY_BROKER_URL', 'pyamqp://guest@localhost//'),
    backend=os.getenv('CELERY_RESULT_BACKEND', 'rpc://')
)

# Define your tasks
@app.task
def example_task(param: Any) -> str:
    # Your task implementation here
    return f"Task executed with param: {param}"

@app.task
def another_task(param1: Any, param2: Any) -> str:
    # Your task implementation here
    return f"Another task executed with params: {param1}, {param2}"

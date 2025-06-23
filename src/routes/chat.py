from fastapi import Request
from fastapi import APIRouter
from fastapi import BackgroundTasks
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse

import asyncio


from libs.utils.schemas.chat import ChatRequest
from src.helper import chat as chat_helper
from src import logger

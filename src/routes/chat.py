import asyncio
from fastapi import Request
from fastapi import APIRouter
from fastapi import BackgroundTasks
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse

from libs.utils.schemas.chat import ChatRequest
from src.helpers import chat as chat_helper
from src import logger


templates = Jinja2Templates(directory="templates")

chat_router = APIRouter(prefix="/chats", tags=["chat"])


@chat_router.post("/")
async def get_chat_response(data: ChatRequest, background_tasks: BackgroundTasks):
    logger.info(f"Entered chat route: {data}")
    try:
        input_data = await chat_helper.extract_input_data(data)
        logger.info(f"Extracted input data: {input_data}")

        logger.info(f"Determining flow keyword")
        flow_keyword = await chat_helper.determine_flow_keyword(input_data)
        query_extractor_keywords = [
            "static_merchant", "account_details", "account_balance", "savings",
            "transfer_money", "pay_bills", "account_statement", "term_deposits"
        ]
        logger.info(f"Flow keyword determined: {flow_keyword}")
        
        logger.info(f"Processing flow with keyword: {flow_keyword}")
        stream_generator =  chat_helper.process_flow(flow_keyword, input_data, query_extractor_keywords)
        
        if stream_generator is None:
            logger.error("Stream generator is None")
            return JSONResponse({"error": "Stream generator is None"}, status_code=500)

        if asyncio.iscoroutine(stream_generator):
            logger.error("Stream generator is a coroutine, not awaited")
            return JSONResponse({"error": "Stream generator is coroutine (not awaited)"}, status_code=500)
        
        if not hasattr(stream_generator, "__aiter__"):
            logger.error("Stream generator is not async iterable")
            return JSONResponse({"error": "Stream generator is not async iterable"}, status_code=500)
        
        logger.info("Returning StreamingResponse")
        return StreamingResponse(stream_generator, media_type="text/plain")
    except Exception as e:
        logger.error(f"[Error] get_chat_response: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)


@chat_router.get("/ui", response_class=JSONResponse)
async def chat_frontend(request: Request):
    
    """
    This function renders the chat frontend
    """

    logger.info("Rendering chat frontend")
    return templates.TemplateResponse("index.html", {"request": request})



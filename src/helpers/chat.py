from libs.utils.prompts import flow_detector_prompts,extractor_prompts
from src.helpers import assistance
from src import logger

from src.helpers.assistance import handle_assistant_flow
from typing import AsyncGenerator
from src.helpers.query_extractor import run_query_extractor


async def extract_input_data(data):
    return {
        "session_id": data.session_id,
        "flow_keyword": data.flow_keyword or "None",
        "question": data.question,
        "thread_id": data.thread_id if data.thread_id not in [None, "", "None", "string"] else None,
        "json_extractor_thread_id": data.json_extractor_thread_id,
        "is_user_registered": str(data.is_user_registered).lower() == "true"
    }



async def determine_flow_keyword(input_data):
    """
    Determine the flow keyword based on the input data.
    """

    flow_keyword = input_data.get("flow_keyword", "")

    if input_data["is_user_registered"]:
        prompt = flow_detector_prompts["registered_user"]
    else:
        prompt = flow_detector_prompts["not_registered_user"]

    if flow_keyword in [None, "", "None", "null", "Null", 'string']:

        flow_keyword, usage = assistance.flow_detector(input_data["question"], prompt)
        

    return flow_keyword


async def process_flow(flow_keyword, input_data, query_extractor_keywords) -> AsyncGenerator[str, None]:
    client = assistance.client
    thread_id = input_data.get("thread_id", None)
    question = input_data["question"]

    if flow_keyword == "assistant":
       

        logger.info("Calling handle_assistant_flow for assistant flow.")
        stream = await handle_assistant_flow(client, thread_id, question)

        async for chunk in stream:
            yield chunk

    elif flow_keyword in query_extractor_keywords:
        logger.info(f"Running query extractor for flow: {flow_keyword}")
        prompt = extractor_prompts[flow_keyword]

        async for chunk in run_query_extractor(client, question, flow_keyword, prompt):
            yield chunk

    else:
        logger.warning(f"No handler for flow keyword: {flow_keyword}")
        yield f"[Unhandled flow: {flow_keyword}]"

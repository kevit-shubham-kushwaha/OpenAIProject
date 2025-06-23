import asyncio
from typing import AsyncGenerator
from openai import OpenAI
from typing import AsyncGenerator, Optional
from typing import List, Optional

from libs.utils.config import config  
from src import logger

client = OpenAI(api_key=config.OPENAI_API_KEY)

async def create_thread():

    """
    Create a new chat thread.
    """
    try:
        logger.info("Creating a new thread for the assistant flow.")
        thread = await asyncio.to_thread(client.beta.threads.create)
        logger.info(f"Thread created with ID: {thread.id}")

        return thread
    except Exception as e:
        logger.error(f"[Error] create_thread: {e}")
        raise e



def flow_detector(questions,prompt):
    """
    Detect the flow keyword based on the user question and prompt.
    """

    logger.info("Detecting flow keyword using OpenAI Assistants API.")
    if config.OPENAI_MODEL_NAME is None:
        logger.error("OPENAI_MODEL_NAME is not set in the configuration.")
        raise ValueError("OPENAI_MODEL_NAME is not set in the configuration.")
    
    try:
        
       
        completion = client.chat.completions.create(
            model=config.OPENAI_MODEL_NAME,
            messages=[
                    {'role': 'system','content': prompt},
                    {'role': 'user','content': questions}
                ],
        )
        response = completion.choices[0].message.content
        logger.info(f"Flow keyword detected: {response}")
        usage = completion.usage

        return response , usage
    except Exception as e:
        logger.error(f"[Error] flow_detector: {e}")
        raise e




def extract_files_from_stream_event(event) -> Optional[List[str]]:
    """
    Helper to extract file IDs from an Assistants API streaming event.
    
    Args:
        event: A single event object from the stream (OpenAI AssistantEvent)
    
    Returns:
        List of file_ids if any are found, else None.
    """
    logger.info("Extracting file IDs from stream event.")
    file_ids = []

    
    logger.info(f"Processing event: {event.event}")
    if event.event == "thread.message.created":
        message = event.data
        for content in message.content:
            if content.type == "file_reference":
                file_id = content.file_id
                file_ids.append(file_id)
    logger.info(f"Extracted file IDs: {file_ids}")
    return file_ids if file_ids else None

async def run_assistant_stream(client,  thread_id: str,user_input: str, assistance_id) -> AsyncGenerator[str, None]:
    """
    Stream assistant response using OpenAI Assistants API with stream=True.
    """
    logger.info("Running assistant stream with OpenAI Assistants API.")
    attached_files = []

    
    try:
        await asyncio.to_thread(
            client.beta.threads.messages.create,
            thread_id=thread_id,
            role="user",
            content=user_input,
        )
        logger.info("User message successfully sent.")
    except Exception as e:
        logger.exception("Failed to send user message to thread.")
        yield f"[Error] Failed to send message: {str(e)}"
        return

    
    try:
        def create_run():
            return client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=assistance_id,
                stream=True
            )

        stream = await asyncio.to_thread(create_run)
        logger.info("Assistant run created. Streaming response...")
    except Exception as e:
        logger.exception("Failed to create assistant run.")
        yield f"[Error] Failed to initiate assistant run: {str(e)}"
        return

   
    try:
        for event in stream:
            try:
                if hasattr(event, "event") and event.event == "thread.message.delta":
                    parts = getattr(event.data.delta, "content", [])
                    for part in parts:
                        if hasattr(part, "text") and hasattr(part.text, "value"):
                            yield part.text.value

                file_ids = extract_files_from_stream_event(event)
                if file_ids:
                    attached_files.extend(file_ids)
                    for fid in file_ids:
                        yield f"\n[Document Attached: file_id={fid}]"
            except Exception as e:
                logger.warning(f"Error while handling stream event: {str(e)}")
    except Exception as e:
        logger.exception("Error during stream processing.")
        yield f"[Error] Issue while streaming assistant response: {str(e)}"



async def handle_assistant_flow(client,thread_id,user_input):
    """
    Handle the assistant flow by creating a thread and running the assistant.
    """
    logger.info("Handling assistant flow.")
    if not thread_id:
        
        thread = await create_thread()
        thread_id = thread.id

    assistance_id = config.OPENAI_ASSISTANT_ID

    try:
        if assistance_id is None:

            logger.error("OPENAI_ASSISTANT_ID is not set in the configuration.")

            raise ValueError("OPENAI_ASSISTANT_ID is not set in the configuration.")
        
        logger.info(f"Using assistant ID: {assistance_id} for thread ID: {thread_id}")
        
        return  run_assistant_stream(client,  thread_id,user_input, assistance_id)
    except Exception as e:
        logger.error(f"[handle_assistant_flow ERROR]: {e}")
        async def error_gen():
            yield f"Assistant failed: {str(e)}"
        return error_gen()


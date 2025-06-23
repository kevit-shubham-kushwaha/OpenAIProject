import json
from typing import AsyncGenerator
import asyncio
from src import logger


async def query_extrator(client, user_input, flow_keyword, prompt) -> AsyncGenerator[str, None]:
    """
    Stream OpenAI Chat Completion using GPT-4 and yield content chunks.
    """
    def create_completion():
        return client.chat.completions.create(
            model="gpt-4",
            messages=[
                {'role': 'system', 'content': prompt},
                {'role': 'user', 'content': user_input}
            ],
            temperature=0,
            stream=True
        )

   
    stream = await asyncio.to_thread(create_completion)

    
    for chunk in stream:
        content = getattr(chunk.choices[0].delta, "content", "")
        if content:
            yield content


async def run_query_extractor(client, user_input, flow_keyword, prompt) -> AsyncGenerator[str, None]:
    buffer = ""
    response_started = False

    logger.info(f"Running query extractor for: {flow_keyword}")

    
    async for chunk in query_extrator(client, user_input, flow_keyword, prompt):
        buffer += chunk
        try:
            data = json.loads(buffer)
            if not response_started and "response" in data:
                logger.info("Yielding initial response from parsed JSON.")
                yield json.dumps(data["response"])  
                response_started = True
        except json.JSONDecodeError:
            continue  

    logger.info("Finalizing query extractor response.")
    try:
        parsed = json.loads(buffer)
        if "response" in parsed:
            yield json.dumps(parsed["response"])  
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse full JSON response: {str(e)}")
        logger.debug(f"Buffer content:\n{buffer}")
        yield json.dumps({"error": "Partial or malformed response."})

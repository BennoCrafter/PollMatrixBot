from openai import AsyncOpenAI
from typing import Optional
import asyncio
from src.utils.logging_config import setup_logger

logger = setup_logger(__name__)


async def predict_pineapple(
    client: AsyncOpenAI, model: str, dish: str
) -> Optional[bool]:
    try:
        response = await client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Think about the ingredients usually found in the given dish. "
                        "Determine if pineapple (or in german ananas) is commonly included. "
                        "Reply only with '1' if yes, or '0' if no — no words, no punctuation, just the number."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Does the dish '{dish}' contain pineapple?",
                },
            ],
        )

        reply_content = response.choices[0].message.content
        if reply_content is None:
            return None

        reply = reply_content.strip()

        return True if "1" in reply else False if "0" in reply else None

    except Exception as e:
        logger.error(f"Error while trying to detect pineapple in '{dish}': {e}")
        return None

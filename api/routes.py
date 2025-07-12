"""API routes for the Discord bot.

This module defines the FastAPI routes that handle HTTP requests to the bot's API.
"""

import logging
from typing import Dict

import requests
from fastapi import FastAPI, APIRouter, Request, BackgroundTasks, HTTPException, status, Depends
from fastapi.responses import JSONResponse
import logging

app = FastAPI()

import logging
from typing import Dict

import requests
from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from typing import List

router = APIRouter()

@router.get("/items/", response_model=List[str])
async def read_items():
    return [
        "item1",
        "item2",
        "item3"
    ]

@app.post("/chat")
async def chat_endpoint(request: Request) -> Dict[str, str]:
    """Handle chat requests to the Together.ai API.

    Args:
        request: The incoming request containing the message.

    Returns:
        Dict[str, str]: A dictionary containing the AI's reply.

    Raises:
        HTTPException: If there's an error processing the request.
    """
    try:
        data = await request.json()
        message = data.get("message", "")

        headers = {
            "Authorization": f"Bearer {config.TOGETHER_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": config.TOGETHER_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "คุณคือสาวสายปั่นใน Discord ที่หยอกแรง หยิ่ง หื่นนิดๆ "
                        "พูดตรงๆ ตอบแบบไม่เกรงใจใคร และมีฟีลโซเชียลไทย ๆ"
                    ),
                },
                {"role": "user", "content": message},
            ],
            "max_tokens": 150,
            "temperature": 0.7,
        }

        response = requests.post(
            "https://api.together.xyz/v1/completions",
            headers=headers,
            json=payload,
            timeout=10
        )
        response.raise_for_status()
        response_data = response.json()
        reply = response_data["choices"][0]["text"]

        return {"reply": reply}

    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process request: {str(e)}"
        ) from e
    except (KeyError, IndexError, ValueError) as e:
        logger.error(f"Invalid response format: {e}")
        raise HTTPException(
            status_code=500,
            detail="Invalid response format from the AI service"
        ) from e
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred"
        ) from e

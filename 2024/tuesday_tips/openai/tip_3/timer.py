import functools
import logging
import time
from typing import Any, Callable

from openai import AsyncOpenAI

from models import OpenAIModels


def timer(func: Callable[[str, OpenAIModels, AsyncOpenAI], str]) -> Callable[[str, OpenAIModels, AsyncOpenAI], str]:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        try:
            result = await func(*args, **kwargs)
        except Exception:
            finish = time.time() - start
            logging.info('%s failed in %.2f', func, finish)
            raise
        else:
            finish = time.time() - start
            model: OpenAIModels = kwargs["model"]
            if model:
                logging.info(f'{func} with model: {model.name} succeeded in {finish:.2f}')
            else:
                logging.info(f'{func} succeeded in {finish:.2f}')


            return result            
        
    return wrapper

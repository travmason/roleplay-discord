import openai
import os
import re
import logging
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

LOGLEVEL = os.getenv("LOGLEVEL")
logging.basicConfig(level=logging.ERROR)

class Bot:
    author = ''
    conversation_text = list()

    openai.api_key = os.getenv("OPENAI_API_KEY")

    def gpt3_completion(self, prompt, engine='text-davinci-002', temp=0.95, top_p=1.0, tokens=400, freq_pen=1.5, pres_pen=0.0, stop=['Human:', 'Daniel:']):
        prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()
        try:
            response = openai.Completion.create(
                engine=engine,
                prompt=prompt,
                temperature=temp,
                max_tokens=tokens,
                top_p=top_p,
                frequency_penalty=freq_pen,
                presence_penalty=pres_pen,
                stop=stop)
            text = response['choices'][0]['text'].strip()
            text = re.sub('\s+', ' ', text)
            return text
        except Exception as oops:
            return "GPT3 error: %s" % oops

    def __init__(self):
        logging.info("Bot initialised")
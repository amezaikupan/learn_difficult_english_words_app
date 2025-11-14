
__generated_with = "0.17.6"

# %%
import llm 
from dotenv import load_dotenv
from pydantic import BaseModel 
import marimo as mo

# load_dotenv(".env")

# %%
from diskcache import Cache 

cache = Cache("difficult_word_list")

# %%
class DifficultWord(BaseModel):
    meaning: str
    origin: str 
    closest_emoji: str
    popularity_in_major_dialect: str
    connotation: str
    first_known_used_year: int 
    popularity: int 
    fields: dict[str, str]
    example_irl: str 
    example_phrase: str 

# %%
models = {
    "gpt-4": llm.get_model("gpt-4"), 
    "gpt-4o": llm.get_model("gpt-4o"), 
}

# %%
def difficult_word_prompt(diff_word, model):
    global cache 

    prompt = f"""
        (Write in markdown and note to decorate important keyword/text) Please tell me about this word: {diff_word}:

        - Meaning
        - Origin 
        - The emoji that best represent the word
        - Popularity in major dialect 
        - Connotation (Whether it is more negitive/positive.)
        - First known use (year)
        - Populartity (0-100)
        - Who/what fields use it? (top 3 (with emoji); each with example of how they use it)
        - Example in real document (quote the **specific** document)
        - Example in normal conversation
        """.strip()

    tup = (diff_word, prompt, model)
    if tup in cache:
        return cache[tup]

    resp = models[model].prompt(prompt, schema=DifficultWord).json()
    cache[tup] = resp 
    return resp
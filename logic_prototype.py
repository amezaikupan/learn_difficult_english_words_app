import marimo

__generated_with = "0.17.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import llm 
    from dotenv import load_dotenv
    from pydantic import BaseModel 
    import marimo as mo

    load_dotenv(".env")
    return BaseModel, llm


@app.cell
def _():
    from diskcache import Cache 

    cache = Cache("difficult_word_list")
    return (cache,)


@app.cell
def _(BaseModel):
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
    return (DifficultWord,)


@app.cell
def _(llm):
    models = {
        "gpt-4": llm.get_model("gpt-4"), 
        "gpt-4o": llm.get_model("gpt-4o"), 
    }
    return (models,)


@app.cell
def _(DifficultWord, cache, models):
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
        
        resp = models[model].prompt(prompt, schema=DifficultWord)
        cache[tup] = resp 
        return resp
    return (difficult_word_prompt,)


@app.cell
def _(difficult_word_prompt):
    print(difficult_word_prompt('laconic', 'gpt-4o'))
    return


@app.cell
def _(cache):
    for key in cache:
        value = cache.get(key)
        print(key, value)
        print()
    return


if __name__ == "__main__":
    app.run()

import marimo

__generated_with = "0.17.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    get_word, set_word = mo.state(None)
    get_word_list, set_word_list = mo.state([])
    def search_word(word):
        set_word(word)
        set_word_list(get_word_list() + [word])

    def word_history():
        buttons = []
        for f in get_word_list():
            # Use a default argument in lambda to capture the current value
            buttons.append(
                mo.ui.button(
                    label=f, 
                    value=f,
                    on_click=lambda value: search_word(value),  # capture current f
                    kind='warn',disabled=True
                )
            )

        search_history = mo.hstack([*buttons], justify='start')
        return search_history

    form = mo.ui.text_area(placeholder="What words to learn today...", full_width=True, rows=1).form(bordered=False, on_change=lambda w: search_word(w))
    return form, get_word, word_history


@app.cell
def _(form, mo, word_history):
    mo.vstack(
        [
            form,
            word_history()
        ]
    )
    return


@app.cell
def _(form, present_word):
    from logic_prototype_script import difficult_word_prompt
    import json
    diff_word = form.value      
    print(json.loads(difficult_word_prompt(diff_word=diff_word, model="gpt-4o")['content']))
    present_word(json.loads(difficult_word_prompt(diff_word=diff_word, model="gpt-4o")['content']))
    return


@app.cell
def _():
    word = 'Laconic'
    dummy_info = {"meaning":"**Laconic** refers to a style of speaking or writing that uses very few words, often conveying much in just a brief statement. This concise manner typically emphasizes brevity and being succinct.","origin":"The term originates from \"Laconia,\" a region in ancient Greece where the Spartans lived. Spartans were known for their clipped, blunt way of speaking, which gave rise to the term.","closest_emoji":"🗣️","popularity_in_major_dialect":"The term \"laconic\" is used in various English-speaking regions but is more commonly recognized in academic and literary contexts.","connotation":"🔵 **Neutral/Positive**: Often seen positively, as it indicates clarity and wit, but can sometimes be perceived as abrupt or terse.","first_known_used_year":1589,"popularity":60,"fields":{"Literature":"**Literature** uses the word \"laconic\" to describe characters or dialogues that convey significant meaning through the use of minimal words or deliberate silence.\n\n- Example: A novelist might write about a character with a \"laconic wit,\" highlighting their ability to say volumes with few words.","Journalism":"**Journalism** often values a laconic style in reporting, where clarity and brevity can communicate news effectively without embellishments. \n\n- Example: Headlines are crafted to be laconic to grab attention and convey information quickly.","Military":"**Military** settings value laconic communication to ensure direct orders, thereby minimizing any potential confusion during operations.\n\n- Example: A sergeant might give laconic orders during a mission for clarity and quick understanding by the troops."},"example_irl":"\"**He had a laconic wit that was often amusing to the aristocracy he observed in his writing.**\" - From \"The Life of Thomas Hardy\" by Florence Emily Hardy.","example_phrase":"**In a conversation**:\n\n- *Person A*: \"How was your day? Anything exciting happen?\"\n\n- *Person B*: \"Busy. Learned a lot.\" (This response gives a clear answer without any unnecessary detail)"}
    return


@app.cell
def _(get_word, mo):
    def metric_vstack(title, content):
        stack = mo.vstack([
        mo.md(text=f"####  <span style='color: grey';> **{title}** </span>"),
        mo.md(text=f"# {content}")
    ], justify='space-around')
        return stack 

    def title_and_content_vstack(title, content):    
        stack = mo.vstack([
        mo.md(text=f"#### <span style='color: grey';> **{title}**</span>"),
        mo.md(text=f"{content}")
    ], justify='space-around')
        return stack 


    def present_word(word_information):
        if get_word() is None:
            return mo.hstack([mo.md(f"##### Please input the word you want to learn!")], align='center', justify='center')

        else: 
            title = mo.md(text=f'# {get_word()} - {word_information['closest_emoji']}')
            meaning = mo.md(text=f'{word_information['meaning']}')

            first_used_year = metric_vstack("First known used year (not sure is true)", word_information['first_known_used_year'])
            origin = title_and_content_vstack("Origin", word_information['origin'])
            history_block = mo.hstack([
                first_used_year, origin
            ], widths=[0.2,1])
            history_block

            connotation = title_and_content_vstack("Connocation", word_information['connotation'])
            connotation

            populartiy_score = metric_vstack("Popularity score", word_information['popularity'])
            populartiy_in_major_dialect = title_and_content_vstack("Popularity in major dialect", word_information['popularity_in_major_dialect'])
            popularity_block = mo.hstack([
                populartiy_score,
                populartiy_in_major_dialect
            ], widths=[0.2, 1])

            field_list = []
            for key, value in word_information['fields'].items():
                field_list.append(title_and_content_vstack(key, value))
            field_block = mo.hstack([*field_list])

            example_irl = title_and_content_vstack("Example IRL", word_information['example_irl'])
            example_conv = title_and_content_vstack("Example in conversation", word_information['example_phrase'])
            example_block = mo.hstack([
                example_irl, example_conv
            ], justify='start')

            result_stack = mo.vstack([
                mo.md(text="------"),
                title,
                meaning,
                mo.md(text="------"),
                history_block,
                mo.md(text="------"),
                connotation,
                mo.md(text="------"),
                popularity_block,
                mo.md(text="------"),
                field_block,
                mo.md(text="------"),
                example_block
            ], gap=3, align='stretch')

            return result_stack       
    return (present_word,)


if __name__ == "__main__":
    app.run()

from .preprocessing import preprocess_text
import pandas as pd


def autocomplete(text):
    # if text is empty or contains only spaces, return an empty list
    try:
        if text == '':
            return {'words': []}
        words = preprocess_text(text)
        # with autocomplete.app_context():
        data = pd.read_csv('Auto_Complete/testless_autocomplete/ngram.csv')


        data.set_index('ngram', inplace=True)
        return {'words': data.loc[words[-1]]['next_word']} 
    except:
        print("Error")
        return {'words': []} 

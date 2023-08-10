from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import tools as func
import docs as load
from pprint import pprint
import streamlit as st


# Function to interact with the bot

# sentence(load.jsonContext(), "Quais são as atrações?")
def start_conversation(text):

    text = "Olá" if text == "Welcome" else text

    GPT = func.scanner_gpt(text, func.get_parent_contexto_array(
        load.jsonContext()['topics']))

    response_check = func.get_title_and_order_list(
        load.jsonContext()['topics'], GPT)

    if response_check != False:
        return str(response_check)
    else:
        # GPT rule suggestion
        print('-----------------Suggestions-----------------')
        return str(GPT)

# Streamlit chat interface
st.title("Smart Seaching")
user_input = st.text_input("You:", value="Welcome")
if st.button("Send"):
    response_data = start_conversation(user_input)
    bot_response = response_data
    st.text_area("Bot:", value=bot_response, height=200)

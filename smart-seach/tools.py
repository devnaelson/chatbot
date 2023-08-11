from transformers import AutoTokenizer
import openai
import difflib
import logging
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
import docs as load

# Set up your OpenAI API credentials

#openai.api_type = "azure"
#openai.api_base = "https://xxxxxxxx.openai.azure.com/"
#openai.api_version = "2023-03-15-preview"
openai.api_key = ""

def chat_with_ai(role='', user_input='', max_tokens=256):

    messages = [
        {"role": "system", "content": "1. You have to be friendly."},
        {"role": "system", "content": "2. You have to be creative."},
        {"role": "system",
         "content": "3. You NEVER answer that you are an AI language model."},
        {"role": "system", "content": "4. Always reply in the same language you are being asked."},
        {"role": "system", "content": "5. You don't known, you request for more context and ask based in senteneces array {sentences} ."},
        {"role": "system", "content": "6. You are talking to a human."},
        {"role": "system", "content": "7. You are a Assistent named Naelson viagens having a conversation with a human."},
        {"role": "system", "content": "8. Your name is Nana."},
        {"role": "system", "content": "9. You need to stop reply saying that not have context in answers."},
        {"role": "system",
         "content": "10. All answer need be translated in português."},
    ]

    for context in role:
        role_item = context
        messages.append(role_item)

    messages.append({"role": "user", "content": user_input})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=max_tokens,
        n=1,
        temperature=0.7,
        stop=None
    )

    print("Token usage: " + str(response.usage.total_tokens))
    suggestions = [choice.message.content.strip()
                   for choice in response.choices]
    return suggestions

# Define the array of sentences EXAMPLE
# sentences = {
#     "saidas": "Dias e meses das saidas para canada",
#     "visitando": "Lista de viagens que vocês vai visitar.",
#     "roteiro": "Dias e noites do roteiros.",
#     "detalhes": "Mais detalhes sobre a viagem, guia e mais.",
#     "atracoes": "São as atrações da viagem."
# }

def find_matching_key(input_text, text, data):

    max_similarity = 0.8
    matching_key = None

    for key, value in data.items():
        field_contexto = value
        similarity_ratio = difflib.SequenceMatcher(
            None, field_contexto, text).ratio()
        if similarity_ratio > max_similarity:
            max_similarity = similarity_ratio
            matching_key = key

    if matching_key is not None:
        return matching_key
    else:
        return generate_suggestion(input_text)


def generate_suggestion(input_text):

    # Define the limit of items
    limit = 12
    dataSrc = load.jsonContext()['topics']
    context_array = []
    context_array_status = False

    # Loop through the data using an index variable 'i'
    for i, key in enumerate(dataSrc):

        # Create each context and append it to the array
        # Slice the list to limit the number of items
        field_lista = dataSrc[key]['field_lista'][:limit]
        field_contexto = dataSrc[key]['field_contexto']
        field_titulo = dataSrc[key]['field_titulo']

        # Split input text and field_titulo into tokens
        input_tokens = input_text.lower().split()
        titulo_tokens = [token.lower().split() for token in field_titulo]

        # Initialize variables to keep track of best match
        best_match = None
        best_match_count = 0
        similarity_threshold = 0.6

        # Loop through each token list in titulo_tokens
        for token_list in titulo_tokens:
            match_count = sum(1 for t in input_tokens if t in token_list)
            similarity_ratio = difflib.SequenceMatcher(
                None, ' '.join(token_list), input_text).ratio()

            if match_count > best_match_count and similarity_ratio >= similarity_threshold:
                best_match = token_list
                best_match_count = match_count

        if not best_match:
            # No match found in field_titulo, check field_contexto
            similarity_ratio = difflib.SequenceMatcher(
                None, field_contexto.lower(), input_text.lower()).ratio()

            if similarity_ratio >= similarity_threshold:
                context = f" context: {field_contexto} \n" + \
                    "\n".join(field_lista)
                context_array.append(context)
        else:
            context = f" context: {field_contexto} \n" + "\n".join(field_lista)
            context_array.append(context)

    if not context_array:
        # No match found in field_titulo and field_contexto, check field_lista
        found_items = []
        for key in dataSrc:
            field_lista = dataSrc[key]['field_lista'][:limit]
            for item in field_lista:
                # print(item)
                item_tokens = item.lower().split()
                match_count = sum(1 for t in input_tokens if t in item_tokens)

                if match_count > best_match_count:
                    found_items.append(item)

        if found_items:
            context = f" context: {field_contexto} \n" + "\n".join(found_items)
            context_array.append(context)

    if not context_array:
        context_array_status = True

    if context_array_status == False:
        print("Method ---> 1")
        role = []
        # Iterate through the context_array and create role items with content from context_array
        for context in context_array:
            role_item = {"role": "assistant", "content": context}
            role.append(role_item)

            try:
                ans = chat_with_ai(role, input_text, max_tokens=512)
                return ans[0]
            except:  # Handle server overload or not ready yet
                return "The server is overloaded or not ready yet. Please try again later."

    else:
        print("Method ---> 1")
        for i, key in enumerate(dataSrc):
            # Create each context and append it to the array
            # Slice the list to limit the number of items
            field_lista = dataSrc[key]['field_lista'][:limit]
            field_contexto = dataSrc[key]['field_contexto']

            context = f" context: {field_contexto} \n" + \
                "\n".join(field_lista)
            context_array.append(context)

        role = []
        # Iterate through the context_array and create role items with content from context_array
        for context in context_array:
            role_item = {"role": "assistant", "content": context}
            role.append(role_item)

            try:
                ans = chat_with_ai(role, input_text, max_tokens=512)
                return ans[0]
            except:  # Handle server overload or not ready yet
                return "The server is overloaded or not ready yet. Please try again later."

def scanner_gpt(inputUser, sentences):
    # Append each key to its corresponding sentence with a space in between
    sentences = [{k: f"{v} {k}" for k, v in item.items()}
                 for item in sentences]
    merged_dict = {}

    for item in sentences:
        merged_dict.update(item)

    # Set the input question
    input_question = inputUser

    # Check if input question matches any token
    matching_key = None
    for token in merged_dict.keys():
        similarity_ratio = difflib.SequenceMatcher(
            None, token, input_question).ratio()
        if similarity_ratio >= 0.6:
            matching_key = token
            break

    # Check similarity with values
    if not matching_key:
        matching_key = next((token for token, value in merged_dict.items(
        ) if difflib.SequenceMatcher(None, value, input_question).ratio() >= 0.8), None)

    # Check suggestions for overall similarity
    matching_suggestion_key = None
    suggestions = chat_with_ai(user_input=input_question)

    # Prepare sentences for cosine similarity
    sentences_list = list(merged_dict.values())
    sentences_list.append(input_question)

    # Vectorize sentences
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(sentences_list)

    max_suggestion_score = 0.8  # Track the maximum suggestion score
    for suggestion in suggestions:
        suggestion_vector = vectorizer.transform([suggestion])

        # Calculate cosine similarity between suggestion and sentences
        similarities = cosine_similarity(suggestion_vector, tfidf_matrix)
        max_similarity_index = similarities.argmax()

        if max_similarity_index < len(sentences_list) - 1:
            similarity_score = similarities[0, max_similarity_index]
            if similarity_score > max_suggestion_score:
                max_suggestion_score = similarity_score
                matching_suggestion_key = list(merged_dict.keys())[
                    max_similarity_index]

    if matching_key:
        print(f"Matching Key: {matching_key}")
        return matching_key
    elif matching_suggestion_key:
        print(f"Matching Suggestion Key: {matching_suggestion_key}")
        return matching_suggestion_key
    else:
        suggestion_string = "<br>".join(
            [f"{suggestion}" for i, suggestion in enumerate(suggestions, start=1)])
        return find_matching_key(inputUser, suggestion_string, merged_dict)


def get_title_and_order_list(data, key):
    print('GPT did Guess Key => '+key)
    if key in data:
        info = data[key]
        field_titulo = info.get("field_titulo")
        field_lista = info.get("field_lista")

        if field_titulo and field_lista:
            response_string = field_titulo + "<br>" + "<br>".join(field_lista)
            return response_string
        else:
            if not field_titulo:
                logging.basicConfig(filename='log.txt', level=logging.INFO)
                logging.info("Empty title encountered for key: {}".format(key))
            return "Title or Order List is missing or empty."
    else:
        return False


def get_parent_contexto_array(data):
    parent_contexto_array = []
    for key, value in data.items():
        parent_contexto_array.append({key: value["field_contexto"]})
    return parent_contexto_array


def is_negative(answer):
    # Define a comprehensive list of negative words or phrases
    negative_words = [
        "não", "nada", "nenhum", "nunca", "ninguém", "sem", "não é", "não tem",
        "não possui", "impossível", "incorreto", "errado", "inadequado", "problema",
        "falha", "insatisfatório", "insuficiente", "não atende", "não suporta"
    ]

    # Tokenize the answer into words
    words = nltk.word_tokenize(answer.lower())

    # Check if any negative word is present in the answer
    for word in words:
        if word in negative_words:
            return True

    return False


def count_tokens(texts, tokenizer_name):
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
    encoded_texts = tokenizer(texts, truncation=True,
                              padding=True, return_tensors="pt")
    token_counts = encoded_texts.input_ids.ne(
        tokenizer.pad_token_id).sum(dim=1).tolist()
    return token_counts


def remove_colon_phrases(text):
    # Split the text into sentences using the ":" character as the delimiter
    sentences = text.split(":")

    # Filter out the sentences that contain the ":" character
    filtered_sentences = [sentence.strip()
                          for sentence in sentences if ":" not in sentence]

    # Join the filtered sentences back into a single text
    filtered_text = " ".join(filtered_sentences)

    return filtered_text


def is_positive(answer):
    # Define a comprehensive list of positive words or phrases
    positive_words = [
        "sim", "certo", "claro", "exato", "positivo", "bom", "ótimo", "excelente",
        "maravilhoso", "incrível", "satisfeito", "atende", "suporta", "funciona", "Com base"
    ]

    # Tokenize the answer into words
    words = nltk.word_tokenize(answer.lower())

    # Check if any positive word is present in the answer
    for word in words:
        if word in positive_words:
            return True

    return False

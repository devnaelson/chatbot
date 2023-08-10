context_array = [
    ' context: Bem vindo, é a frase mais preferida de quando se inicia uma conversa. \nSeja bem vindo, ao Chatbot',
    ' context: Saidas para o canada, Dias 19 periodo noturno. \n1. Mai. 11\n2. Jul. 27\n3. Set. 14'
]

role = [{"role": "user", "content": "sasas"}]
# Iterate through the context_array and create role items with content from context_array
for context in context_array:
    role_item = {"role": "assistant", "content": context}
    role.append(role_item)

# Print the updated role array
print(role)
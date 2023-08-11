###### Este sistema de pequeno porte foi concebido com base em princípios de aprendizado, buscando emular a eficácia do 'lanchain', com o propósito de minimizar os períodos de espera, enquanto aplicava conhecimentos técnicos avançados, como embedding, clusterização e análise de similaridade, entre outros.

Esta concepção pragmática demandou um período considerável de desenvolvimento, contudo, resultou na aquisição de novos insights e em uma compreensão mais abrangente das tecnologias subjacentes, tais como LLM, NTK e NLP, incluindo todas as suas metodologias associadas. Estou incluindo este projeto em meu portfólio, e adicionalmente, pretendo compartilhá-lo com a comunidade.

Installs, precisa instalar as libs. Algumas eu desativei, pois parei com o desenvolvimento por um tempo.
Em tools.py adiciona a sua chave openai.api_key = "" 
```
pip install streamlit
pip install -U scikit-learn
pip install tensorflow==2.2.0
pip install transformers
pip install nltk
python -m nltk.downloader punkt
```
Sobre o documento document.json, funciona assim: a chave, índex, key, seja o que você prefere chamar, está localizada abaixo com o nome 'ola'. Ela pode ser personalizada. As demais chaves, como field_contexto, field_titulo e field_lista, devem ser iguais.
```
    "ola": {
        "field_contexto": "Bem vindo, é a frase mais preferida de quando se inicia uma conversa.",
        "field_titulo": "Bem vindo ao Chat Bot do Naelson.",
        "field_lista": [
            "Seja bem vindo, ao Chatbot"
        ]
    }
```

<img src="./imagens/ola.png" alt="drawing" width="800"/><br>
- Conforme evidenciado na imagem acima e na estrutura do JSON, ocorreu uma correspondência (match) em que o título foi exibido junto com um item da lista.
  
<img src="./imagens/saida.png" alt="drawing" width="800"/><br>
- Uma das características interessantes, que procurei preservar, é que quando ele encontra a chave pai, ele exibe precisamente o conteúdo presente no array.

<img src="./imagens/saida-wihtouContext.png" alt="drawing" width="800"/><br>
- Como você pode observar aqui, realizei uma pesquisa sem contexto, resultando na resposta que me foi fornecida.
  
<img src="./imagens/saida-Contexted.png.png" alt="drawing" width="800"/><br>
- Logo em seguida, adicionei mais contexto para obter uma correspondência na similaridade com o campo "field_contexto
  
<img src="./imagens/terminal.png" alt="drawing" width="800"/><br>
- Uma das enormes vantagens desse pequeno protótipo é a economia de tokens, onde, quando comparado ao uso do langchain, o consumo é três vezes maior.
- 
### Perfil do LinkedIn
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/devnaelson/)

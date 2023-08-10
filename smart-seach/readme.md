Padroes para algorismo. 
Se 1 itém apenas for maior do que 80% de a resposta.
Se 1 itém apenas ser maior e tiver somente ele na casa dele, retorna resposta.
Se nao check first parameter keys similarity and começe novamente. 

Se muitas similaridades notas no mesmo range, joga para GPT porque ele ta sem contexto. Leva também as chaves topicos e descrição;  

Se 1 itém tiver mais de 2 similáriedade e tiver na mesma casa, exemplo 0.5200,0.5700 [
 	pergunta um contexto ao usuario e de essas duas chaves como sugestão
]

Se 2 item tive na proximo 1 casa a baixo do outro, leva para GPT esses dois templates para responder.
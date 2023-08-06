# BlipNlpTest

Essa é uma classe que permite o teste de mensagens em provedores integrados na plataforma, com o retorno do conteúdo cadastrado no Assistente de Conteudo.

## Instalação

Para instalar o pacote, basta executar o comando abaixo:

<pre><code>pip install blipnlptest</code></pre>

## Uso

Após a instalação do pacote, você terá acesso a classe que permitirá a execução do teste.

Os parâmetros necessários são:

df : dataframe de entrada, onde o cabeçalho com as mensagens devem ter como título "Text";
key  : chave do bot.


Exemplo do código:

<pre><code>

import blipnlptest as bnt


cc = bnt.contentchecker(df, key)
result = cc.test()
display(result)
</code></pre>

Com os parâmetros previamente atribuídos, rodando o código acima você terá como saída a exibição do resultado.

A saída contém:

- A mensagem de entrada;
- Resposta entregue pelo Assistente de Conteudo;
- Entidades reconhecidas;
- N intenções, onde N representa o número de colunas/intenções exibidas (onde a primeira é a que obteve maior confiança).

 
Para declarar N, insira o número desejado no método test().

<pre><code>
result = bnt.test(3)
</code></pre>

## Licença

Esse projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

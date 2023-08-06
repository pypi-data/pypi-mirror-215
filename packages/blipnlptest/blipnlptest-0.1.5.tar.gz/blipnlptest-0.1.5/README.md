# BlipNlpTest

Essa é uma classe que permite o teste de mensagens em provedores integrados na plataforma, com o retorno do conteúdo cadastrado no Assistente de Conteudo.

## Instalação

Para instalar o pacote, basta executar o comando abaixo:

<pre><code>pip install blipnlptest</code></pre>

## Uso

Após a instalação do pacote, você terá acesso a classe que permitirá a execução do teste.

Os parâmetros necessários são:

df : dataframe de entrada
key : chave do bot.

Exemplo do código:

<pre><code>

import blipnlptest as bnt

cc = bnt.contentchecker(df, key)
</code></pre>

A composição do df definirá qual método deverá ser utilizado.

Caso a análise seja de dados já analisados pelo provedor (envie um dataframe que tenha no mínimo as colunas Text, Intentions, Entities e Score), use:

<pre><code>

import blipnlptest as bnt

cc = bnt.contentchecker(df, key)
cc.identityanalysis()
</code></pre>

Se a análise for feita com dados que não foram analisados (envie um dataframe que a coluna de texto tenha o nome Text), use:

<pre><code>

import blipnlptest as bnt

cc = bnt.contentchecker(df, key)
cc.sentences()
</code></pre>

OBS: A divisão foi feita para que os dados já rotulados não realizem outra análise no provedor.

Com os parâmetros previamente atribuídos, rodando o código acima você terá como saída a exibição do resultado com:

- A mensagem de entrada;
- A resposta entregue pelo Assistente de Conteudo;
- As entidades reconhecidas;
- A intenção reconhecida;
- O score.

## Licença

Esse projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

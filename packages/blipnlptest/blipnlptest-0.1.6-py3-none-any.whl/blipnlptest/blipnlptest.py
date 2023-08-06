import requests
import json
import pandas as pd
import warnings

warnings.filterwarnings("ignore", category=pd.core.common.SettingWithCopyWarning)

class contentchecker:

  def __init__(self, data, key):
      self.data = data
      self.key = key
      self.url = 'https://http.msging.net/commands'
      self.header = {
            'content-type': 'application/json',
            'Authorization': self.key
            }

      if isinstance(data, pd.DataFrame) == False:
        print(f'Ao invés de "{data}", favor inserir um DataFrame. A coluna com o texto deve ter o cabeçalho com o nome "Text".')
      else:
        pass

  def identityanalysis(self):
    try:
      df = self.data[['Text', 'Intention', 'Entities', 'Score']]
      ent = []

      for i in range(len(df)):
        if df.Entities[i] != '[]':
          ent.append(pd.json_normalize(json.loads(df.Entities[i])).value.tolist())
        else:
          ent.append('')
      
      df.loc[:, 'Content'] = [self.test(model='n', intention=df.Intention[x], entities=ent[x]) for x in range(len(df.Entities))]
      
      df = df.sort_values(by='Content',ascending=False)
      return(df)
    
    except KeyError: 
      print("O seu dataframe deve conter as seguintes colunas ['Text', 'Intention', 'Entities', 'Score']. Você pode obtê-las pela tabela vwidentityanalysis.")


  def sentences(self):
    
    if any(col in ['intentions', 'intent', 'intention', 'score', 'entities', 'entity'] for col in self.data.columns.str.lower()):
      print("Ops, o método sentences não é melhor método para a sua operação. Que tal utilizar o identityanalysis?")

    else:

      df = self.data
      df = pd.DataFrame([self.test(model='y',text=t) for t in df.Text])

      df = df[['text','intentions','entities']]
      df['Score'] = df.intentions.apply(lambda s: s[0]['score'])
      df.intentions = df.intentions.apply(lambda i: i[0]['id'])
      df.columns = ['Text', 'Intention', 'Entities', 'Score']
      ent = [pd.json_normalize(df.Entities[i]).value.tolist() if df.Entities[i] != '[]' else '' for i in range(len(df.Text))]
      df.loc[:, 'Content'] = [self.test(model='n', intention=df.Intention[x], entities=ent[x]) for x in range(len(df.Entities))]
      df = df.sort_values(by='Content',ascending=False)

      return(df)


  def test(self, model, text=None, intention=None, entities=None):

    if model == 'y':

      body =  {
                "id": "{{$guid}}",
                "to": "postmaster@ai.msging.net",
                "method": "set",
                "uri": "/analysis",
                "type": "application/vnd.iris.ai.analysis-request+json",
                "resource": {
                  "text":f"{text}"
                }
              }
      
      tr = requests.post(self.url, json=body,headers=self.header).json()

      result = tr['resource']

    elif model == 'n':
        if isinstance(entities, str):
          result = self.test_content(intention,[entities])
        elif isinstance(entities, list):
          result = self.test_content(intention,entities)

    else:
      print('O parâmetro model deve ter o valor de y ou n.')

    return(result)

  def test_content(self, intention, entities):

    if isinstance(entities, str):
        entities = [entities]
    elif isinstance(entities, list):
        pass

    body =  {
              "id": "46544651",
              "to": "postmaster@ai.msging.net",
              "method": "set",
              "uri": "/content/analysis",
              "resource": {
                "intent": intention,
                "entities":entities,
                "minEntityMatch":1
                },
              "type": "application/vnd.iris.ai.content-combination+json"
            }
    try:        
      r = requests.post(self.url, json=body,headers=self.header).json()['resource']['result']['content']
    except KeyError:
      r = 'no_answer'
    return(r)

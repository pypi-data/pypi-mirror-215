import requests
import json
import pandas as pd

class ContentChecker:

  def __init__(self, data, key):
      self.data = data
      self.key = key

      if isinstance(data, pd.DataFrame) == False:
        print(f'Ao invés de "{data}", favor inserir um DataFrame. A coluna com o texto deve ter o cabeçalho com o nome "Text".')
      else:
        pass

  def normalize_data(self):
    phrases =  [{"sentence":str(self.data.Text.tolist()[x])} for x in range(len(self.data))]
    return(phrases)

  def test(self, n_intentions=1):
    
    url = f"https://nlp-assistant.cs.blip.ai/analyze?Intentions={n_intentions}"
    
    headers = {
        "accept": "text/plain",
        "X-Bot-Key": self.key,
        "X-Bot-Organization": 'blip',
        "Content-Type": "application/json-patch+json"
    }

    response = self.create_df(requests.post(url, headers=headers, data=json.dumps(self.normalize_data())))
    return(response)
  
  def create_df(self, response):

    if response.status_code == 200:
      df1 = pd.json_normalize(json.loads(response.content)['contentResults'])
      df2 = pd.json_normalize(df1.intentions.tolist())
      df = pd.concat([df1, df2], axis=1)
      df = df.drop('intentions', axis=1)
      return(df)
    else:
      print(response.text)
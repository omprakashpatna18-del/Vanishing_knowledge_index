import pandas as pd
import fastapi as FastAPI
data=pd.read_csv(https://github.com/omprakashpatna18-del/Vanishing_knowledge_index/blob/main/Vanishing_Knowledge_Index_Dataset%20(2).csv")
app=FastAPI()
#pulling out data
categories=list(data["category"].str.strip().unique())
practice
@app.post("/search")
def search_and_display(keywords):
    keywords=keywords.split()
  req_cat=None
  for cat in catgories:
    if any(word in keywords) in cat:
      print("category found")
      req_cat=cat
      break
  if req_cat not None:
    options=data[data["category"]==req_cat].practice_name
  for
             
     




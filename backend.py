import pandas as pd
import fastapi as FastAPI
data=pd.read_csv(https://github.com/omprakashpatna18-del/Vanishing_knowledge_index/blob/main/Vanishing_Knowledge_Index_Dataset%20(2).csv")
app=FastAPI()
#pulling out data
categories=list(data["category"].str.strip().unique())
practice=list(data['practice_name'].str.strip().unique())
@app.get("/search")
async def search_and_display(keywords):
  keywords=keywords.split()
  req_cat=None
  for cat in catgories:
    if any(word in keywords) in cat:
      print("category found")
      req_cat=cat
      break
  if req_cat not None:
    options=data[data["category"]==req_cat].practice_name
  for prac in practice:
    if any(word in keywords) in prac:
        print("Practice found")
        req_cat=prac
        break
  if req_cat not None:
    options=data["practice_name"]
  else:
    options=None
  return {"Options":options}
@app.get("/retrieval")
async def data_retrieval(selected):
    science_check=data["science_check"]
    if data["region"]:
      region=data["region"]
    proof=data["source_link"]
    info=data["info"]
    return { "Practice_name":selected,
        "Region":region,
        "Information":info,
        "Proof":data
        }
        
    
    


             
     




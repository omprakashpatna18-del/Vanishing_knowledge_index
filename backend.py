import pandas as pd
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
data=pd.read_csv("https://github.com/omprakashpatna18-del/Vanishing_knowledge_index/blob/da2cc3e9c110d69a84732251977338dc3d5243c2/Vanishing_Knowledge_Index_Dataset%20(2).csv")
app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#pulling out data
categories=list(ata["category"].str.strip().str.lower().unique())
practice=list(data['practice_name'].str.strip().str.lower().unique())
@app.get("/search")
async def search_and_display(keywords):
  keywords=keywords.lower().split()
  req_cat=None
  for cat in catgories:
    if any(word in keywords) in cat:
      print("category found")
      req_cat=cat
      break
  if req_cat not None:
    options=data[data["category"]==req_cat].practice_name
    return {"Options":options}
  for prac in practice:
    if any(word in keywords) in prac:
        print("Practice found")
        req_cat=prac
        break
  if req_cat not None:
    options=data["practice_name"]
    return {"Options":options}
 
  return {"Options":[]}
@app.get("/retrieval")
async def data_retrieval(selected):
    matched_data = data[data["practice_name"].str.lower() == selected.lower()]
    
    if matched_data.empty:
        raise HTTPException(status_code=404, detail="Selected practice information not found.")
        
    row = matched_data.iloc[0].to_dict()
    science_check=row.get("science_check")
    region=row.get("region","Unknown")
    proof=row.get("source_link","None")
    info=row.get("info")
    latitude=row.get("latitude")
    longitude=row.get("longitude")
    return { "Practice_name":selected,
        "Region":region,
        "Information":info,
        "Proof":data,
        "latitude":latitude,
        "longitude":longitude
        }
        
    
    


             
     




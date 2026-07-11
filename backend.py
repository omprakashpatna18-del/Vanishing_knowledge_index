import pandas as pd
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Query, UploadFile, File, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import pandas as pd
from werkzeug.utils import secure_filename
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
#_-------adding files-----------#
MEDIA_DIR = "./uploaded_media"
LIVE_CSV_PATH = "live_dataset.csv"
PENDING_CSV_PATH = "pending_submissions.csv"

for folder in [MEDIA_DIR]:
    os.makedirs(folder, exist_ok=True)
columns = ["category", "practice_name", "region", "info", "science_check", "source_link", "media_asset"]
for path in [LIVE_CSV_PATH,PENDING_CSV_PATH]:
    if not os.path.exists(path):
        pd.DataFrame(columns=columns).to_csv(path,index=False)

security = HTTPBearer()
ADMIN_TOKEN = "SuperSecretAdminKey123"
ALLOWED_MIME_TYPES = ["audio/mpeg", "audio/wav", "audio/x-wav", "audio/ogg", "video/mp4", "video/webm"]

def verify_admin(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if creditionals.creditionals!=ADMIN_TOKEN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Administrative Authentication Token"
        )
    return True
#-------Validation------------#
class Data(BaseModel):
    practice_name: str,
    category: str,
    region: str,
    info: str,
    source_link: file: UploadFile = File(...)
#--------User Submission------#
@app.post("/upload")
async def upload(data: Data):
    


        
    
    


             
     




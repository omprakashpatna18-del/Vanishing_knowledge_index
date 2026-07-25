import pandas as pd
import os
from pydantic import BaseModel
from geopy.geocoders import Nominatim
from fastapi import FastAPI, HTTPException, Query, UploadFile, File, Form, HTTPException, Depends,status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import pandas as pd
from werkzeug.utils import secure_filename
import joblib
data=pd.read_csv("Vanishing_Knowledge_Index_Dataset(2).csv")
model=joblib.load("search")
app=FastAPI(title="Vanishing knowledge index")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#--------searching--------#
categories=list(data["category"].str.strip().str.lower().unique())
practice=list(data['practice_name'].str.strip().str.lower().unique())
@app.get("/search")
async def search_and_display(keyword):
  keywords=keyword.lower().split()
  req_cat=None
  for cat in categories:
    if any(word in cat for word in keywords):
      print("category found")
      req_cat=cat
      break
  if req_cat:
    options=data[data["category"]==req_cat].practice_name
    return {"Options":options}
  for prac in practice:
    if any(word in prac for word in keywords):
        print("Practice found")
        req_cat=prac
        break
  if req_cat:
    options=data["practice_name"]
    return {"Options":[options]}
  word=pd.DataFrame(data=[keyword],columns=["practice_name"])
  if max(model.predict_proba(word)[0])>0.4:
      req_cat=model.predict(word)[0]
      options=data[data["category"]==req_cat].practice_name
      return {"Options":options}
  return {"Options":[]}
#------Retrieval-----#
@app.get("/retrieval")
async def data_retrieval(selected):
    matched_data = data[data["practice_name"].str.lower() == selected.lower()]
    
    if matched_data.empty:
        raise HTTPException(status_code=404, detail="Selected practice information not found.")
        
    row = matched_data.iloc[0].to_dict()
    science_check=row.get("science_check","")
    region=row.get("region","Unknown")
    proof=row.get("source_link","None")
    info=row.get("notes","")
    latitude=row.get("latitude",None)
    longitude=row.get("longitude",None)
    return { "Practice_name":selected,
        "Region":region,
        "Information":info,
        "Proof":proof,
        "latitude":latitude,
        "longitude":longitude
        }
#_-------adding files-----------#
MEDIA_DIR = "./uploaded_media"
LIVE_CSV_PATH = "Vanishing_Knowledge_Index_Dataset(2).csv"
PENDING_CSV_PATH = "pending_submissions.csv"

for folder in [MEDIA_DIR]:
    os.makedirs(folder, exist_ok=True)
columns = ["category", "practice_name", "region", "info", "science_check", "source_link", "media_file","latitude","longitude"]
for path in [LIVE_CSV_PATH,PENDING_CSV_PATH]:
    if not os.path.exists(path):
        pd.DataFrame(columns=columns).to_csv(path,index=False)

security = HTTPBearer()
ADMIN_TOKEN = "SuperSecretAdminKey123"
ALLOWED_MIME_TYPES = ["audio/mpeg", "audio/wav", "audio/x-wav", "audio/ogg", "video/mp4", "video/webm"]

def verify_admin(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials!=ADMIN_TOKEN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Administrative Authentication Token"
        )
    return True
#--------User Submission------#
geolocator = Nominatim(user_agent="my_unique_app_name_123")
@app.post("/upload")
async def upload(
    practice_name: str = Form(...),
    category: str = Form(...),
    region: str = Form(...),
    science_check: str = Form(""),
    notes: str = Form(...),
    source_link: str = Form(""),       
    latitude: float = Form(None),
    longitude: float = Form(None),
    media_file: UploadFile = File(...) ): 
    try:
        if not latitude or not longitude:
            location = geolocator.geocode(region)
            if location:
                latitude=location.latitude
                longitude=location.longitude
            else:
                latitude,longitude=None,None
        if media_file.content_type not in ALLOWED_MIME_TYPES:
            raise HTTPException(status_code=400, detail="Invalid media type. Standard Audio/Video files only.")
        safe_filename = secure_filename(media_file.filename)
        file_path = os.path.join(MEDIA_DIR, safe_filename)
        with open(file_path,'wb') as f:
            while chunk:=await media_file.read(1024*1024):
                f.write(chunk)
        new_row = {
            "category": category,
            "practice_name": practice_name,
            "region": region,
            "science_check": science_check,
            "info": notes if notes else "",
            "source_link": source_link if source_link else "",
            "latitude":latitude if latitude else "",
            "longitude":longitude if longitude else "",
            "media_file": safe_filename
        }
        pending_df = pd.read_csv(PENDING_CSV_PATH)
        pending_df = pd.concat([pending_df, pd.DataFrame([new_row])], ignore_index=True)
        pending_df.to_csv(PENDING_CSV_PATH, index=False)
       return {"message":"Upload Successful"}
  except Exception as e:
       print(e)
       raise HTTPException(status_code=500,detail="Failed to process files.")

#-----Authentication------#
ADMIN_USER = "admin123"
ADMIN_PASS = "securepassword"

@app.post("/login")
async def admin_login(username: str = Form(...), password: str = Form(...)):
    if username == ADMIN_USER and password == ADMIN_PASS:
        return {"status": "success", "token": ADMIN_TOKEN}
    else:
        raise HTTPException(status_code=400, detail="Invalid username or password")


@app.get("/admin/pending", dependencies=[Depends(verify_admin)])
async def check_submissioons():
    pending_df=pd.read_csv(PENDING_CSV_PATH)
    if not pending_df.empty:
        return{"Pending submissions":pending_df.to_dict(orient="records")}

@app.post("/admin/approve",dependencies=[Depends(verify_admin)])
async def approv():
    try:
      live_df=pd.read_csv(LIVE_CSV_PATH)
      pending_df=pd.read_csv(PENDING_CSV_PATH)
      live_df=pd.concat([live_df,pending_df], ignore_index=True)
      live_df.to_csv("Vanishing_Knowledge_Index_Dataset(2).csv")
      pending_df=pd.DataFrame(columns=columns)
      pd.DataFrame(columns=columns).to_csv(PENDING_CSV_PATH, index=False)
      return{"message":"Upload successful"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Upload not successful.")
        
    



    
    
    
    
    


        
    
    


             
     




from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class input(BaseModel):
    recipients: list[str]
    template:str

class BroadcastListCreate(BaseModel): 
    name:str
    template:str
    contacts:list[str]
    success:int
    failed:int
    status:str
    scheduled_time: Optional[datetime] = None  # Optional, as it could be null
    task_id: Optional[str] = None 
    

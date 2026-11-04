from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Term (BaseModel):
    id:                         int
    code:                       str
    beginDate:                  datetime
    endDate:                    datetime
    isOpenForMaintenance:       Optional[bool] = None
    isOpenForPublic:            Optional[bool] = None
    isOpenForReporting:         Optional[bool] = None

class Year (BaseModel):
    Id:                         int
    FallYear:                   int
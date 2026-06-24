from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AcademicYear (BaseModel):
    id:                         int
    code:                       str
    beginDate:                  datetime
    endDate:                    datetime
    isOpenForMaintenance:       Optional[bool] = None
    isOpenForPublic:            Optional[bool] = None
    isOpenForReporting:         Optional[bool] = None
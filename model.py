from sqlmodel import SQLModel, Field
from typing import Optional

class MOTDBase(SQLModel):
    content: str

class MOTD(MOTDBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

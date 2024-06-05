from pydantic import BaseModel
class MenuSearch(BaseModel):
    query: str
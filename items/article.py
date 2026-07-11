from pydantic import BaseModel, ConfigDict

# APIのレスポンス型
class Article(BaseModel):
    id: int
    title: str
    content: str
    model_config = ConfigDict(from_attributes=True)
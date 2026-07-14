from pydantic import BaseModel, ConfigDict


# APIのレスポンス型
class ArticleResponse(BaseModel):
    id: int
    title: str
    content: str
    model_config = ConfigDict(from_attributes=True)

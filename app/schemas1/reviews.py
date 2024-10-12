# from pydantic import BaseModel
# from datetime import datetime

# class ReviewCreate(BaseModel):
#     text: str
#     class Config:
#         orm_mode = True
#         from_attributes = True


# class Review(BaseModel):
#     id: int
#     user_id: int
#     gas_id: int
#     text: str
#     review_date: datetime

#     class Config:
#         orm_mode = True
#         from_attributes = True
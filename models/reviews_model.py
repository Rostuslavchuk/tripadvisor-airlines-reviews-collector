from datetime import date as Date, datetime
from pydantic import BaseModel, HttpUrl, TypeAdapter


class ReviewModel(BaseModel):
    rootdomain: str
    sku: str
    review_id: str
    title: str | None = None
    rating: int
    text: str | None = None
    author: str | None = None
    brand_response: str | None = None
    product_has_been_tried: bool = True
    url: HttpUrl
    date: datetime | None = None
    purchased_date: Date | None = None
    recommended_review: bool | None = None
    review_images_url: list[HttpUrl] | None = None
    product_name: str | None = None


ReviewsAdapter = TypeAdapter(list[ReviewModel])

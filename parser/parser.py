from lxml import html
import json
from operator import itemgetter
from models.reviews_model import ReviewsAdapter


class Parser:
    def get_reviews_object(self, data: list):
        review_object = data[0]["data"]["locations"][0]
        return review_object

    def parse_page_count(self, data: list) -> int:
        return int(self.get_reviews_object(data)["reviewListPage"]["totalCount"])

    def parse_reviews(self, data: list):
        reviews = self.get_reviews_object(data)["reviewListPage"]["reviews"]
        product = self.get_reviews_object(data)

        parsed_reviews = []
        for review in reviews:
            purchased_date = review.get("tripInfo", {}).get("stayDate")
            if purchased_date:
                purchased_date = f"{purchased_date[:7]}-01"

            photos = []
            for photo in review.get("photos", []):
                photo_params = photo.get("photoSizeDynamic", {})
                url_template = photo_params.get("urlTemplate")
                if not url_template:
                    continue
                clear_url, _, _ = url_template.partition("?")
                photos.append(clear_url)

            parsed_reviews.append(
                {
                    "rootdomain": "tripadvisor.com/airlines",
                    "sku": f"d{review['locationId']}",
                    "review_id": f"r{review['id']}",
                    "title": review.get("title"),
                    "rating": int(review["rating"]),
                    "text": review.get("text"),
                    "author": review.get("userProfile", {}).get("displayName"),
                    "brand_response": (
                        str(review["ownerResponse"])
                        if review.get("ownerResponse")
                        else None
                    ),
                    "product_has_been_tried": True,
                    "url": f"https://www.tripadvisor.com{review.get('route', {}).get('url') or review.get('url')}",
                    "date": review.get("createdDate", review.get("publishedDate")),
                    "purchased_date": purchased_date,
                    "recommended_review": (
                        True
                        if int(review["rating"]) >= 4
                        else False
                        if int(review["rating"]) <= 2
                        else None
                    ),
                    "review_images_url": photos,
                    "product_name": f"{product.get('name', '')} {product.get('placeType', '')}",
                }
            )

        validated_reviews = ReviewsAdapter.validate_python(parsed_reviews)
        return [review.model_dump(mode="json") for review in validated_reviews]

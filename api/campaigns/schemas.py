from datetime import datetime
from typing import List

from pydantic import BaseModel, field_serializer


class CampaignResponseSchema(BaseModel):
    campaign_name: str
    game: str
    start_date: datetime
    end_date: datetime
    rewards: List[str]

    @field_serializer('start_date', 'end_date')
    def serialize_datetime(self, dt: datetime, _info):
        return dt.strftime('%a, %b %d, %I:%M %p') if dt else None

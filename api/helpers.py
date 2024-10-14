import uuid

from django.db import models


class Helper:
    @staticmethod
    def generate_uuid() -> models.UUIDField:
        return models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

import uuid
from dataclasses import dataclass


@dataclass
class Order:
    order_id: uuid.UUID

    def __init__(self, order_id: uuid.UUID):
        self.order_id = order_id

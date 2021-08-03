"""Model of SHOWROOM Live."""
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Live:
    start: datetime
    end: datetime

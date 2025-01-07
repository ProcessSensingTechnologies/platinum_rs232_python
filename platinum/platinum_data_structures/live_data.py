from dataclasses import dataclass


@dataclass
class LiveDataV4:
    Version: int = 0
    StatusFlags: int = 0
    Reading: float = 0
    Temperature: float = 0
    Det1: int = 0
    Ref: int = 0
    Fa: float = 0
    Uptime: int = 0
    DetMin: int = 0
    DetMax: int = 0
    RefMin: int = 0
    RefMax: int = 0

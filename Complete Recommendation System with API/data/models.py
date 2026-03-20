from dataclasses import dataclass

@dataclass
class User:
    id: str
    name: str
    interests: str

@dataclass
class Content:
    id: str
    title: str
    category: str
    difficulty: str
    popularity: float

@dataclass
class Interaction:
    uid: str
    cid: str
    itype: str
    rating: float
from pydantic import BaseModel


class PhysiologicalNeeds(BaseModel):
    water: float
    food: float
    shelter: float
    sleep: float
    clothing: float


class SafetyNeeds(BaseModel):
    personal_security: float
    employment: float
    health: float
    property: float


class LoveBelongingNeeds(BaseModel):
    friendship: float
    intimacy: float
    family: float
    sense_of_connection: float


class EsteemNeeds(BaseModel):
    respect: float
    self_esteem: float
    status: float
    recognition: float
    strength: float


class AvatarNeeds(BaseModel):
    physiological: PhysiologicalNeeds
    safety: SafetyNeeds
    love_belonging: LoveBelongingNeeds
    esteem: EsteemNeeds


class User(BaseModel):
    username: str
    description: str
    location: str
    followers_count: int
    following_count: int
    tweet_count: int


class Comment(BaseModel):
    text: str
    timestamp: str
    user: User
    likes: int

class Post(BaseModel):
    text: str
    timestamp: str
    user: User
    likes: int
    comments: list[Comment]


class News(BaseModel):
    title: str
    description: str
    content: str
    timestamp: str
    source: str


class Narration(BaseModel):
    timestamp: str
    situation: str
    mood: str
    goals: list[str]
    skills: list[str]
    inventory: list[str]
    stress: float


class Acting(BaseModel):
    timestamp: str    
    needs: AvatarNeeds
    actions: list[str]
    thoughts: list[str]


class AvatarEnvironment(BaseModel):
    storyline_phase: str
    latest_posts: list[Post]
    latest_news: list[News]
    friends_list: list[User]
    enemy_list: list[User]
    avatar_latest_narrations: list[Narration]
    avatar_latest_acting: list[Acting]


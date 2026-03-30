from typing import TypedDict, NotRequired
from typing import List, Dict
from typing_extensions import TypedDict


class NumpyArrayJSON(TypedDict):
    __numpy__: str
    dtype: str
    shape: List[int]


class Regulation(TypedDict):
    regulation: NumpyArrayJSON


class Emotion(TypedDict):
    pride: Regulation  # dynamic emotion keys possible


class EnthusiasmBlock(TypedDict):
    motivation: NumpyArrayJSON
    inspiration: NumpyArrayJSON


class Priority(TypedDict):
    # keys are stringified ints like "1"
    # typing can't restrict literal numeric strings easily
    # so we use Dict[str, float]
    pass


class MindEntry(TypedDict):
    id: str
    content: str
    dominant_emotion: str
    emotion: Dict[str, Regulation]  # dynamic emotion names
    importance: float
    Enthusiasm: EnthusiasmBlock
    assoitation: Dict[str, object]
    priority: Dict[str, float]
    why_this_feeling: str
    timestamp: str  # ISO datetime


class NameBlock(TypedDict):
    name: str
    nickname: List[str]


class PersonalData(TypedDict):
    name: NameBlock
    firends: Dict[str, object]


class ScaleBlock(TypedDict):
    scale: NumpyArrayJSON
    details: str


class OverallEnthusiasm(TypedDict):
    inspiration: ScaleBlock
    motivation: ScaleBlock


class Existence(TypedDict):
    _date: str
    _exact_date: str


class _Brain_(TypedDict):
    id: str
    _personal_data: PersonalData
    mind: List[MindEntry]
    current_objective: List[object]
    main_goal: List[object]
    overall_Enthusiam: OverallEnthusiasm
    _existence: Existence
    decayed_memories: List[object]
class BrainDict(TypedDict):
    id: str
    ...
class BrainWrapper(TypedDict):
    brain: BrainDict

brains: list[BrainWrapper]
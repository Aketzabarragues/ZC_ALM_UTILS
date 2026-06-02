from enum import Enum
from typing import List, Optional, Dict
from pydantic import BaseModel, Field

class BlockType(str, Enum):
    FC = "FC"
    FB = "FB"
    DB = "DB"
    UDT = "UDT"

class VariableDef(BaseModel):
    name: str
    data_type: str
    default_value: str = "-"
    comment: Optional[str] = None
    is_retain: bool = False

class SystemInfo(BaseModel):
    hardware: str = "-"
    engineering: str = "-"

class DependencyDef(BaseModel):
    type: str
    elements: str

class SiemensBlock(BaseModel):
    name: str
    block_type: BlockType
    system_info: SystemInfo = Field(default_factory=SystemInfo)
    description: Optional[str] = None
    restrictions: Optional[str] = None
    dependencies: List[DependencyDef] = Field(default_factory=list)
    changelog_md: Optional[str] = None
    
    author: Optional[str] = None
    version: Optional[str] = None
    family: Optional[str] = None
    
    sections: Dict[str, List[VariableDef]] = Field(default_factory=dict)
    source_code: Optional[str] = None
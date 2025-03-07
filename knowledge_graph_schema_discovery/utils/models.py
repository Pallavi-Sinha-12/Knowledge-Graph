from pydantic import BaseModel
from typing import List, Optional

class EntityProperty(BaseModel):
    property: str
    is_key_property: bool
    mapping_table: str
    mapping_column: str


class Entity(BaseModel):
    entity: str
    properties: List[EntityProperty]


class EntityConfig(BaseModel):
    entities: List[Entity]


class Relationship(BaseModel):
    source_entity: str
    target_entity: str
    relationship: str
    source_property: str
    target_property: str
    source_mapping_table: str
    target_mapping_table: str
    source_mapping_column: str
    target_mapping_column: str
    joining_condition: Optional[str]

class RelationshipConfig(BaseModel):
    relationships: List[Relationship]

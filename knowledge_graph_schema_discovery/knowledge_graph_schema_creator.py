from utils.models import EntityConfig, RelationshipConfig
from utils.llm_initializer import LLMInitializer
from prompts import ENTITY_DISCOVERY_PROMPT, RELATIONSHIP_DISCOVERT_PROMPT

class KnowledgeGraphSchemaCreator:
    """
    A class to create and manage knowledge graph schemas based on table schemas.
    Attributes:
    -----------
    table_schema_list : str
        A string representation of the table schemas extracted from the data source.
    llm_intializer : LLMInitializer
        An instance of the LLMInitializer class used to interact with the language model.
    Methods:
    --------
    generate_entity_config() -> EntityConfig:
        Generates the entity creation configuration based on the table schemas.
    generate_relationship_schema(entity_config: EntityConfig) -> RelationshipConfig:
        Generates the relationship discovery configuration based on the table schemas and entity creation configurations.
    display_entity_config(entity_config: EntityConfig):
        Displays the entity configuration in a readable format.
    display_relationship_config(relationship_config: RelationshipConfig):
        Displays the relationship configuration in a readable format.
    """

    def __init__(self, table_schema_list : str):
        self.table_schema_list = table_schema_list
        self.llm_intializer = LLMInitializer()

    def generate_entity_config(self) -> EntityConfig:
        user_prompt = "The following are the table schemas extracted from the data source: \n" + self.table_schema_list + "\nPlease provide the entity creation config based on the table schemas."
        response = self.llm_intializer.get_response(
            system_prompt=ENTITY_DISCOVERY_PROMPT,
            user_prompt=user_prompt,
            response_format_pydantic_model=EntityConfig
        )

        return response

    def generate_relationship_schema(self, entity_config : EntityConfig) -> RelationshipConfig:
        entity_config_str = entity_config.model_dump_json()
        user_prompt = "The following are the table schemas extracted from the data source: \n" + self.table_schema_list + "\n. The following are the entity creation configurations: \n" + entity_config_str + "\nPlease provide the relationship discovery config based on the table schemas and entity creation configurations."
        response = self.llm_intializer.get_response(
            system_prompt=RELATIONSHIP_DISCOVERT_PROMPT,
            user_prompt=user_prompt,
            response_format_pydantic_model=RelationshipConfig
        )
        
        return response
    
    def display_entity_config(self, entity_config: EntityConfig):
        n = 0
        for config in entity_config.entities:
            n = n+1
            entity_name = config.entity
            print(f"{n} Entity - ", entity_name)
            print("Properties:")
            for property_config in config.properties:
                print("Property Name :-", property_config.property)
                print("Is Key Property :-", property_config.is_key_property)
                print("Mapping Table :-", property_config.mapping_table)
                print("Mapping Column :-", property_config.mapping_column)
                print("\n")
            print("\n")

    def display_relationship_config(self, relationship_config: RelationshipConfig):
        n = 0
        for config in relationship_config.relationships:
            n = n+1
            print(f"{n} Relationship - ")
            print("Source Entity :-", config.source_entity)
            print("Target Entity :-", config.target_entity)
            print("Relationship :-", config.relationship)
            print("Source Property :-", config.source_property)
            print("Target Property :-", config.target_property)
            print("Source Mapping Table :-", config.source_mapping_table)
            print("Target Mapping Table :-", config.target_mapping_table)
            print("Source Mapping Column :-", config.source_mapping_column)
            print("Target Mapping Column :-", config.target_mapping_column)
            print("Joining Condition :-", config.joining_condition)
            print("\n")
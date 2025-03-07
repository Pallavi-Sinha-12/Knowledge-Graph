from neo4j import GraphDatabase
from utils.models import EntityConfig, RelationshipConfig

def create_metagraph(uri, username, password, database_name, entity_config: EntityConfig, relationship_config: RelationshipConfig):
    """
    Creates a metagraph in a Neo4j database based on the provided entity and relationship configurations.
    Args:
        uri (str): The URI of the Neo4j database.
        username (str): The username for authentication.
        password (str): The password for authentication.
        database_name (str): The name of the database to connect to.
        entity_config (EntityConfig): Configuration object containing entities and their properties.
        relationship_config (RelationshipConfig): Configuration object containing relationships and their properties.
    Returns:
        None
    """
    with GraphDatabase.driver(uri, auth=(username, password), database=database_name) as driver, driver.session() as session:
        for entity in entity_config.entities:
            entity_query = f"""
                MERGE (e:ENTITY {{Name: '{entity.entity}'}})
                {''.join([f"MERGE (p{idx}:PROPERTY {{Name: '{prop.property}'}}) MERGE (e)-[:HAS_PROPERTY {{Is_Key_Property: {prop.is_key_property}, Source_Table: '{prop.mapping_table}', Source_Column: '{prop.mapping_column}'}}]->(p{idx}) " for idx, prop in enumerate(entity.properties, 1)])};
            """
            session.run(entity_query)
        
        for rel in relationship_config.relationships:
            relationship_query = f"""
                MATCH (s:ENTITY {{Name: '{rel.source_entity}'}}), (t:ENTITY {{Name: '{rel.target_entity}'}})
                MERGE (r:RELATIONSHIP {{Name: '{rel.relationship}', Joining_Condition: '{rel.joining_condition or ''}'}})
                MERGE (r)-[:CONNECTS_FROM {{Source_Property: '{rel.source_property}', Source_Table: '{rel.source_mapping_table}', Source_Column: '{rel.source_mapping_column}'}}]->(s)
                MERGE (r)-[:CONNECTS_TO {{Target_Property: '{rel.target_property}', Target_Table: '{rel.target_mapping_table}', Target_Column: '{rel.target_mapping_column}'}}]->(t);
            """
            session.run(relationship_query)
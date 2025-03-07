from knowledge_graph_schema_discovery.knowledge_graph_schema_creator import KnowledgeGraphSchemaCreator
from utils.table_schema_extractor import DataSchemaLoader
from metagraph import create_metagraph
from dotenv import load_dotenv
import os

load_dotenv()

data_schema_loader = DataSchemaLoader()
table_schema_list = data_schema_loader.load_schemas()
knowledge_graph_schema = KnowledgeGraphSchemaCreator(table_schema_list)

entity_config = knowledge_graph_schema.generate_entity_config()
relationship_config = knowledge_graph_schema.generate_relationship_schema(entity_config)
print(entity_config)
print('--------------\n')

knowledge_graph_schema.display_entity_config(entity_config)
print('--------------\n')
knowledge_graph_schema.display_relationship_config(relationship_config)

create_metagraph(
    uri=os.getenv('NEO4J_URI'),
    username=os.getenv('NEO4J_USERNAME'),
    password=os.getenv('NEO4J_PASSWORD'),
    database_name=os.getenv('NEO4J_DATABASE'),
    entity_config=entity_config,
    relationship_config=relationship_config
)



    

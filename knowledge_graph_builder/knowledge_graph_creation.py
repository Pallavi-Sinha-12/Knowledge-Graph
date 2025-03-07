from pyspark.sql import SparkSession
from knowledge_graph_schema_loader import KnowledgeGraphSchema

class KnowledgeGraphCreator:
    """
    A class used to create a knowledge graph using Apache Spark and Neo4j.
    Attributes
    ----------
    spark : SparkSession
        The Spark session used for data processing.
    knowledge_graph_schema : KnowledgeGraphSchema
        The schema of the knowledge graph, which includes entity and relationship configurations.
    Methods
    -------
    generate_entity_nodes_query(entity_name, property_column_map, key_property_name, entity_num)
        Generates a Cypher query to create or merge entity nodes in the knowledge graph.
    generate_relationship_query(source_entity, relationship, target_entity, source_property, target_property, source_column, target_column)
        Generates a Cypher query to create or merge relationships between entities in the knowledge graph.
    create_entity_nodes(tables_map)
        Creates entity nodes in the knowledge graph from the given tables.
    create_relationships(tables_map)
        Creates relationships between entities in the knowledge graph from the given tables.
    create(tables_map)
        Orchestrates the creation of entity nodes and relationships in the knowledge graph from the given tables.
    """

    def __init__(self, spark : SparkSession, knowledge_graph_schema : KnowledgeGraphSchema):
        self.spark = spark
        self.knowledge_graph_schema = knowledge_graph_schema

    def generate_entity_nodes_query(self, entity_name, property_column_map, key_property_name, entity_num):
        query = ""
        query = f"MERGE (n{entity_num}:{entity_name} {{{key_property_name}: event.{property_column_map[key_property_name]}}})\n"
        for property_name, property_column in property_column_map.items():
            if property_name != key_property_name:
                query += f"SET n{entity_num}.{property_name} = event.{property_column}\n"
        return query
    
    def generate_relationship_query(self, source_entity, relationship, target_entity, source_property, target_property, source_column, target_column):
        query = f"""MATCH (a:{source_entity} {{ {source_property}: event.{source_column} }}), (b:{target_entity} {{ {target_property}: event.{target_column} }})
        MERGE (a)-[:{relationship}]->(b)\n"""
        return query
    
    def create_entity_nodes(self, tables_map):
        for table_name, df in tables_map.items():
            entities_config_df = self.knowledge_graph_schema.get_entities_config_df_for_a_table(table_name)
            entity_num = 0
            entities_creation_query = ""
            for row in entities_config_df.collect():
                entity_num +=1
                query = self.generate_entity_nodes_query(row.Entity, row.Properties, row.Key_Property, entity_num)
                entities_creation_query += query

            print(entities_creation_query)
            df.write.format("org.neo4j.spark.DataSource").option("query", entities_creation_query).mode("Overwrite").save()

    
    def create_relationships(self, tables_map):
        relationships_config_df = self.knowledge_graph_schema.get_relationships_config_df()
        for row in relationships_config_df.collect():
            relationship_creation_query = self.generate_relationship_query(row.Source_Entity, row.Relationship, row.Target_Entity, row.Source_Property, row.Target_Property, row.Source_Column, row.Target_Column)
            print(relationship_creation_query)
            if row.Joining_Condition == "":
                df = tables_map[row.Source_Table]
            else:
                source_df = tables_map[row.Source_Table]
                target_df = tables_map[row.Target_Table]
                join_columns = list(set([row.Joining_Condition.split("==")[0].split(".")[1].strip(), row.Joining_Condition.split("==")[1].split(".")[1].strip()]))
                df = source_df.join(target_df, join_columns, "inner")

            df.write.format("org.neo4j.spark.DataSource").option("query", relationship_creation_query).mode("Overwrite").save()


    def create(self, tables_map):
        self.create_entity_nodes(tables_map)
        self.create_relationships(tables_map)
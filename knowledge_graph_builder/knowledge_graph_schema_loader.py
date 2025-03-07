from pyspark.sql.functions import collect_list, map_from_arrays, col, first, when

class KnowledgeGraphSchema:

    def __init__(self, spark):
        self.spark = spark

    def get_entities_config_df_for_a_table(self, table_name):
        """
        Retrieves a DataFrame containing the configuration of entities for a specified table.
        Args:
            table_name (str): The name of the table for which to retrieve the entities configuration.
        Returns:
            DataFrame: A DataFrame with the following columns:
                - Entity: The name of the entity.
                - Properties: A map of property names to source columns.
                - Key_Property: The key property of the entity, if any.
        """
        read_cypher_query = f"MATCH (n:ENTITY)-[p:HAS_PROPERTY {{Source_Table : '{table_name}'}}]->(k:PROPERTY) RETURN n.Name as Entity,  k.Name As Property,  p.Is_Key_Property as Is_Key_Property, p.Source_Column as Source_Column"
        entities_config_df = self.spark.read \
            .format("org.neo4j.spark.DataSource") \
            .option("query", read_cypher_query) \
            .load()
        
        entities_config_df = entities_config_df.groupBy("Entity").agg(
            map_from_arrays(collect_list("Property"), collect_list("Source_Column")).alias("Properties"),
            first(when(col("Is_Key_Property") == True, col("Property")), ignorenulls=True).alias("Key_Property")
        )
        return entities_config_df

    def get_relationships_config_df(self):
        read_cypher_query = f"""MATCH (n:ENTITY)<-[k:CONNECTS_FROM]-(r:RELATIONSHIP)<-[s:CONNECTS_TO]->(t:ENTITY)
        RETURN n.Name as Source_Entity, r.Name as Relationship, t.Name as Target_Entity,k.Source_Property as Source_Property,k.Source_Table as Source_Table, k.Source_Column as Source_Column,
        s.Target_Property as Target_Property, s.Target_Table as Target_Table, s.Target_Column as Target_Column, r.Joining_Condition as Joining_Condition
        """
        relationships_config_df = self.spark.read \
            .format("org.neo4j.spark.DataSource") \
            .option("query", read_cypher_query) \
            .load()
        return relationships_config_df
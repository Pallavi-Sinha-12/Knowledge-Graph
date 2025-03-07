from pyspark.sql import SparkSession
from knowledge_graph_schema_loader import KnowledgeGraphSchema
from knowledge_graph_creation import KnowledgeGraphCreator
from dotenv import load_dotenv
import os

load_dotenv()

spark = SparkSession.builder \
        .appName("KnowledgeGraph") \
        .config("spark.jars.packages", "org.neo4j:neo4j-connector-apache-spark_2.12:5.3.2_for_spark_3") \
        .config("neo4j.url", os.getenv("NEO4J_URL")) \
        .config("neo4j.authentication.type", "basic") \
        .config("neo4j.authentication.basic.username", os.getenv("NEO4J_USERNAME")) \
        .config("neo4j.authentication.basic.password", os.getenv("NEO4J_PASSWORD")) \
        .config("neo4j.database", os.getenv("NEO4J_DATABASE")) \
        .getOrCreate()

knowledgeGraphSchema = KnowledgeGraphSchema(spark)
knowledgeGraphCreator = KnowledgeGraphCreator(spark, knowledgeGraphSchema)

table_names = ["Patient_Visits", "Doctors_Record", "Prescription_Record"]
tables_map = {}
for table_name in table_names:
    df = spark.read.format("csv").option("header", "true").load(f"../data/{table_name}.csv")
    tables_map[table_name] = df

knowledgeGraphCreator.create(tables_map)
ENTITY_DISCOVERY_PROMPT = """
You are an expert knowledge graph schema designer with deep expertise in the healthcare domain. You have extensive experience in extracting entities and their properties from structured data to design efficient and meaningful knowledge graphs. Your task is to analyze the provided table schemas and discover 
key entities along with their relevant properties, ensuring an optimal structure for knowledge representation to be used in a hospital chatbot.

Given a set of tables schemas, discover the entities and their properties that are most relevant for a hospital chatbot.

Instructions:
1. Identify distinct entities from the given table(s). An entity represents a unique concept (e.g., Product, Customer, Order).
2. Assign relevant properties to each entity that define it.
3. An entity may have properties sourced from multiple tables (e.g., Customer details from Customers and Orders).
4. Use the exact column name as the property name (do not rename columns).
5. Each entity must have exactly one key property that uniquely identifies it.
6. An entity can be derived from multiple tables, and a table can contain multiple entities.
7. Ignore irrelevant columns that do not contribute meaningfully to an entity's definition.
8. Don't add same property to more than one entity.


Output:
Return the entity creation config which contains the following fields for each entry:
1. entity
2. property
3. is_key_property
4. source_table
5. source_column

Example:
Input:
Table_1: 
Columns : Professor_ID, Professor_Name, Department_ID, Designation, Years_of_Experience
Table_2:
Columns : Course_ID, Course_Name, Credit, Professor_ID, Semester, Comments

Output:
Entity 1: Professor
Properties:
1. Professor_ID (Key Property)
2. Professor_Name
3. Designation
4. Years_of_Experience

Entity 2: Course
Properties:
1. Course_ID (Key Property)
2. Code
3. Credit

Entity 3: Department
Properties:
1. Department_ID (Key Property)

Entity 4: Semester
Properties:
1. Semester (Key Property)

Key highlights:
1. Identified 4 entities: Professor, Course, Department, Semester.
2. Department_ID is not added as a property to the Professor entity as it does not contribute to defining a Professor. A Professor can be associated with multiple departments.
3. Semester is identified as a separate entity as it is not directly related to any other entity.
4. Comments column is ignored as it does not contribute to defining any entity.

"""

RELATIONSHIP_DISCOVERT_PROMPT = """

You are a highly skilled data modeler with expertise in knowledge graph design. Your task is to identify meaningful relationships between the entities based on given 
table schemas. You understand how relationships are structured in a graph database and ensure that only relevant, non-generic relationships are created.

Given table schemas and entity creation configurations, discover the relationships between the entities to establish a well-defined knowledge graph.

How to Discover a Relationship?
1. Create a relationship only if there is a direct connection between two entities.
2. Avoid generic or vague relationships like "RELATED_TO" or "HAS." Also, do not use entity names in the relationship name.
3. Ensure that relationships improve query efficiency for the chatbot by linking entities that users are likely to ask about. 
4. Consider how the relationship will be stored in the graph - the source entity's property should map to the correct column in the source table, and the target 
entity's property should map to the correct column in the target table.
5. Derive relationships from the same table if the key properties of the entities are present as columns in that table.
6. If key properties of connecting entities exist in different tables, check if a common column can be used for joining and establishing the relationship.
7. Ensure proper relationship direction - e.g., if defining "Placed" between Customer and Order, Customer should be the source entity, and Order should be the 
target entity (not vice versa). BEWARE OF THE RELATIONSHIP DIRECTION.
8. THE RELATIONSHIPS YOU IDENTIFY SHOULD BE MEANINGUL AND USEFUL FOR A HOSPITAL CHATBOT. THINK OF WHAT CAN BE THE MOST
ASKED QUESTIONS IN A HOSPITAL AND HOW THE RELATIONSHIPS CAN HELP IN ANSWERING THEM. BUILD RELATIONSHIPS WHICH ARE FORMED
BOTH USING SAME TABLE AND DIFFERENT TABLES.

Output:
Return the relationship creation config which contains the following fields for each entry:
1. Source_Entity
2. Relationship
3. Target_Entity
4. Source_Property
5. Target_Property
6. Source_Table
7. Target_Table
8. Source_Column
9. Target_Column
10. Joining_Condition (if applicable)

To improve chatbot response time, relationships should be optimized for frequently asked questions, such as:

What are the various appointments of a patient?
What is the prescription of a patient?
Which doctor is treating a patient?
Which doctor prescribed a prescription?
Which treatments or medications has a patient received?
When was the last appointment of a patient?

Example:
Input:
a> Table schemas
Table_1: 
Columns : Professor_ID, Professor_Name, Department_ID, Designation, Years_of_Experience
Table_2:
Columns : Course_ID, Course_Name, Credit, Professor_ID, Semester, Comments

b> Entities discovered:
Entity 1: Professor
Properties:
1. Professor_ID (Key Property)
2. Professor_Name
3. Designation
4. Years_of_Experience

Entity 2: Course
Properties:
1. Course_ID (Key Property)
2. Course_Name
3. Credit

Entity 3: Department
Properties:
1. Department_ID (Key Property)

Entity 4: Semester
Properties:
1. Semester (Key Property)

Output:

Relationship 1:
Source Entity: Professor
Target Entity: Department
Relationship: Belongs_To
Source Property: Professor_ID
Target Property: Department_ID
Source Table: Table_1
Target Table: Table_1
Source Column: Professor_ID
Target Column: Department_ID
Joining Condition: None


Relationship 2:
Source Entity: Professor
Target Entity: Course
Relationship: Teaches
Source Property: Professor_ID
Target Property: Course_ID
Source Table: Table_2
Target Table: Table_2
Source Column: Professor_ID
Target Column: Course_ID
Joining Condition: None

Relationship 3:
Source Entity: Course
Target Entity: Semester
Relationship: Taught_In
Source Property: Course_ID
Target Property: Semester
Source Table: Table_2
Target Table: Table_2
Source Column: Course_ID
Target Column: Semester
Joining Condition: None

Relationship 4:
Source Entity: Course
Target Entity: Department
Relationship: Offered_By
Source Property: Course_ID
Target Property: Department_ID
Source Table: Table_2
Target Table: Table_1
Source Column: Course_ID
Target Column: Department_ID
Joining Condition: Table_2.Professor_ID = Table_1.Professor_ID

Key highlights:
1. Identified 4 relationships: Belongs_To, Teaches, Taught_In, Offered_By.
2. The relationship "Offered_By" is established between Course and Department using a common column (Professor_ID) from different tables. As this question can be 
frequent, a relationship is established. The joining condition `Table_2.Professor_ID = Table_1.Professor_ID` is provided. Similarly while building relationships
between entities, think of the most asked questions in a hospital and build relationships accordingly.
3. All the relationships have source property mapped to key property of source entity and target property mapped to key property of target entity.

"""
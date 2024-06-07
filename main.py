# import streamlit as st
# from pymongo import MongoClient
# import urllib, io, json
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain

# # Initialize Google Generative AI model
# llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key="YOUR_API_KEY")

# llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key="AIzaSyCLJCDu07bJNOidbRgac2U65_B9osjFhPA")
# result = llm.invoke("Write a ballad about LangChain")
# # Mongo client
# username = "ronidas"
# pwd = "YFR85HiZLgqFtbPW"
# client = MongoClient("mongodb+srv://Hitesh:Ghjkl!123@cluster0.k22qi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
# db = client["e_commerce"]
# collection = db["users"]

# st.title("Talk to MongoDB")
# st.write("Ask anything and get an answer")
# input = st.text_area("Enter your question here")

# with io.open("sample.txt", "r", encoding="utf-8") as f1:
#     sample = f1.read()
#     f1.close()

# # Prompt template
# prompt = """
#     You are a very intelligent AI assistant who is an expert in identifying relevant questions from users
#     and converting them into MongoDB aggregation pipeline queries.
#     Please use the below schema to write the MongoDB queries, don't use any other queries.
#     Schema:
#     The mentioned MongoDB collection talks about listings for accommodations on Airbnb. 
#     Here's a breakdown of its schema with descriptions for each field:
#     (Schema description...)
    
#     Sample Example:
#     Below are several sample user questions related to the MongoDB document provided,
#     and the corresponding MongoDB aggregation pipeline queries that can be used to fetch the desired data.
#     Use them wisely.
#     Sample Question: {sample}
#     As an expert, you must use them whenever required.
#     Note: You have to just return the query, nothing else. Don't return any additional text with the query. Please follow this strictly.
#     Input: {question}
#     Output:
# """
# query_with_prompt = PromptTemplate(
#     template=prompt,
#     input_variables=["question", "sample"]
# )
# llmchain = LLMChain(llm=llm, prompt=query_with_prompt, verbose=True)

# if input is not None:
#     button = st.button("Submit")
#     if button:
#         response = llmchain.invoke({
#             "question": input,
#             "sample": sample
#         })
#         # query=json.loads(response["text"])
#         query = [
#             {
#                 "$lookup": {
#                     "from": "post",
#                     "localField": "_id",
#                     "foreignField": "user_id",
#                     "as": "posts"
#                 }
#             }
#         ]
#         results = collection.aggregate(query)
#         print(query)
#         for result in results:
#             st.write(result)


import streamlit as st
from pymongo import MongoClient
import mysql.connector
import psycopg2
import urllib, io, json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
import urllib.parse as up

# Initialize Google Generative AI model
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key="YOUR_API_KEY")

llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key="AIzaSyCLJCDu07bJNOidbRgac2U65_B9osjFhPA")
result = llm.invoke("Write a ballad about LangChain")

# MongoDB client
mongo_username = "ronidas"
mongo_pwd = "YFR85HiZLgqFtbPW"
mongo_client = MongoClient("mongodb+srv://Hitesh:Ghjkl!123@cluster0.k22qi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
mongo_db = mongo_client["e_commerce"]
mongo_collection = mongo_db["users"]

# MySQL client
mysql_conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sHj@6378#jw",
    database="newdata_schema"
)



mysql_cursor = mysql_conn.cursor(dictionary=True)

print(mysql_cursor)

st.title("Talk to MongoDB/SQL/PostgreSQL")
st.write("Ask anything and get an answer")

# Select database type
db_type = st.selectbox("Select database type", ["MongoDB", "MySQL", "PostgreSQL"])

input = st.text_area("Enter your question here")

with io.open("sample.txt", "r", encoding="utf-8") as f1:
    sample = f1.read()
    f1.close()

# Prompt template
prompt = """
    You are a very intelligent AI assistant who is an expert in identifying relevant questions from users
    and converting them into database queries.
    Please use the below schema to write the queries, don't use any other queries.
    Schema:
    The mentioned collection talks about listings for accommodations on Airbnb.
    Here's a breakdown of its schema with descriptions for each field:
    (Schema description...)

    Sample Example:
    Below are several sample user questions related to the provided document,
    and the corresponding queries that can be used to fetch the desired data.
    Use them wisely.
    Sample Question: {sample}
    As an expert, you must use them whenever required.
    Note: You have to just return the query, nothing else. Don't return any additional text with the query. Please follow this strictly.
    Input: {question}
    Output:
"""
query_with_prompt = PromptTemplate(
    template=prompt,
    input_variables=["question", "sample"]
)
llmchain = LLMChain(llm=llm, prompt=query_with_prompt, verbose=True)

if input:
    button = st.button("Submit")
    if button:
        response = llmchain.invoke({
            "question": input,
            "sample": sample
        })
        query = response["text"].strip()

        if db_type == "MongoDB":
            query = json.loads(query)
            results = mongo_collection.aggregate(query)
            for result in results:
                st.write(result)
        elif db_type == "MySQL":
            mysql_cursor.execute(query)
            results = mysql_cursor.fetchall()
            for result in results:
                st.write(result)
    

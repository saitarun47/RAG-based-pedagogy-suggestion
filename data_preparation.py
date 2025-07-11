import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec
import os
from dotenv import load_dotenv


load_dotenv()


df = pd.read_csv('data/pedagogy.csv')


df = df.dropna().reset_index(drop=True)  
df.columns = df.columns.str.strip()

df['combined_text'] = (
    df['Course Name'].astype(str) + ' ' +
    df['Pedagogies used'].astype(str) + ' ' +
    df['Average Student Marks'].astype(str) + ' ' +
    df['Student Feedback'].astype(str)
)


model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(df['combined_text'].tolist())


assert len(embeddings) == len(df), "Embeddings and DataFrame rows do not match!"


pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))


index_name = 'updated-pedagogy-suggestion'
dimension = 384  # Dimension of 'all-MiniLM-L6-v2'


if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=dimension,
        metric='cosine',
        spec=ServerlessSpec(
            cloud='aws', 
            region='us-east-1'  
        )
    )


index = pc.Index(index_name)


for i, row in df.iterrows():
    index.upsert([(str(i), embeddings[i].tolist(), {
        'Course Name': row['Course Name'],
        'Pedagogies used': row['Pedagogies used'],
        'Average Student Marks': row['Average Student Marks'],
        'Student Feedback': row['Student Feedback']
    })])

print("Data preparation and indexing complete!")
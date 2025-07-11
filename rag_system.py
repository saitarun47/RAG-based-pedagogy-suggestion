import os
import pinecone
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from groq import Client  

load_dotenv()

class RAGSystem:
    def __init__(self):
        
        self.client = Client(api_key=os.getenv('GROQ_API_KEY'))
        
    
        self.pc = pinecone.Pinecone(api_key=os.getenv('PINECONE_API_KEY'))

        self.index_name = 'updated-pedagogy-suggestion'
        self.index = self.pc.Index(self.index_name)  
        
        
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def generate_suggestion(self, course_name):
       
        query = f"{course_name} "
        query_embedding = self.model.encode(query).tolist()

        
        results = self.index.query(vector=query_embedding, top_k=5, include_metadata=True)

        
        context = ""
        for match in results['matches']:
            context += f"Course: {match['metadata']['Course Name']}\n"
            context += f"Pedagogies: {match['metadata']['Pedagogies used']}\n"
            context += f"Student Feedback: {match['metadata']['Student Feedback']}\n"
            context += f"Marks: {match['metadata']['Average Student Marks']}\n\n"

        
        prompt = f"""With the given information for the course "{course_name}":

{context}

Identify and suggest the top 3 teaching pedagogies that would be most impactful for this course. Justify your choices using insights from average student marks and feedback to show why these methods would yield the best learning results.Make sure to not print the calculations of average student marks and student feedback."""
       
        chat_completion = self.client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": prompt,
            }],
            model="llama-3.3-70b-versatile",  
            temperature=0.8,
            max_tokens=2000,
        )

      
        return chat_completion.choices[0].message.content
    


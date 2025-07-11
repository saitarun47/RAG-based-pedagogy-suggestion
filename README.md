# Pedagogy Suggestion Using RAG (Retrieval Augmented Generation)

## Overview

**Pedagogy Suggestion System** is an AI-driven tool that helps educators choose suitable teaching methods for university-level courses. It uses machine learning, semantic search, and large language models to provide data-informed recommendations aimed at improving student engagement and learning outcomes.

---
<img width="1892" height="913" alt="Screenshot 2025-07-11 124515" src="https://github.com/user-attachments/assets/a2ae813f-88f7-4f3d-a029-126318448f82" />

## Why This Project Matters

### The Problem
- **Educators** often rely on intuition or limited experience to choose teaching methods, leading to inconsistent student outcomes.
- **Institutions** lack a scalable, data-driven way to optimize pedagogy across diverse courses and student populations.

### The Solution
- **Pedagogy Suggestion System** bridges this gap by analyzing historical course data, student performance, and feedback to recommend the most effective teaching strategies for any given course.
- It empowers educators to make evidence-based decisions, improving student success and institutional teaching quality at scale.

---

## Key Features & Impact

- **AI-Driven Recommendations:** Uses Retrieval-Augmented Generation (RAG) to combine semantic search with LLM-based reasoning (Groq Llama 3) for context-aware suggestions.
- **Data-Backed Insights:** Trained on a rich dataset of 300+ real course records, including pedagogies used, student marks, and feedback.
- **Web App:** Simple, intuitive frontend (Flask) for educators to get instant recommendations.
- **Scalable & Deployable:** Fully containerized with Docker for easy deployment in any environment.

### Real-World Impact
- **Boosts Student Performance:** Helps educators select methods proven to increase marks and satisfaction.
- **Standardizes Best Practices:** Enables institutions to scale up what works, reducing trial-and-error in teaching.
- **Saves Time:** Instantly surfaces the best strategies, freeing educators to focus on teaching, not research.
- **Data-Driven Culture:** Fosters a culture of continuous improvement and evidence-based pedagogy.

---

## Technical Stack

- **Machine Learning:**
  - Sentence Transformers for semantic embeddings
  - Pinecone for vector search
  - Groq Llama 3 LLM for generative recommendations
- **Data Engineering:**
  - Pandas, NumPy for data cleaning and preparation
  - Real-world dataset
- **Backend:**
  - Python (Flask)
- **Frontend:**
  - Minimal, user-friendly web interface
- **MLOps:**
  - Docker for containerization and reproducibility



---

## How It Works

1. **User enters a course name** (e.g., "Machine Learning").
2. **Semantic search** finds similar courses in the dataset using vector embeddings.
3. **LLM generates** a ranked list of the most effective pedagogies, with justifications based on historical marks and feedback.
4. **User receives actionable, data-driven recommendations**.

---



## Why This Project

- **Bridges ML and Education:** Real-world application of NLP, vector search, and LLMs to solve a high-impact problem in education.
- **Demonstrates Innovation:** Shows initiative in using state-of-the-art AI to drive measurable improvements in teaching and learning.


---





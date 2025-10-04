"""
Query the ChromaDB vector database with improved retrieval and prompts.

This script:
1. Accepts a query from command line
2. Retrieves relevant chunks (k=5, lower threshold)
3. Uses improved prompts for synthesis
4. Returns formatted response with sources
"""

import argparse
from typing import List, Tuple
from dotenv import load_dotenv

from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import Document

# Load environment variables
load_dotenv()

# Configuration
CHROMA_PATH = "chroma"
DEFAULT_K = 10  # Increased to get more diverse results
DEFAULT_THRESHOLD = 0.4  # Lowered to cast wider net

# Improved prompt template that encourages synthesis and pattern recognition
PROMPT_TEMPLATE = """
You are analyzing entrepreneur biographies and podcast transcripts. Answer the question using ONLY the context provided below.

Context from {num_sources} source(s):
{context}

Question: {question}

CRITICAL INSTRUCTIONS:
- Use only information explicitly stated in the context
- Synthesize insights across multiple sources when present
- Compare and contrast different approaches between entrepreneurs
- Provide specific examples and quotes
- If the context lacks information to answer fully, acknowledge what's missing

⚠️ CRITICAL: DO NOT ADD ANY SOURCE REFERENCES, CITATIONS, OR SOURCES SECTIONS IN YOUR ANSWER. 
- Do not write [Source: Name] or any similar citations
- Do not include a "Sources:" section or list
- Do not mention sources at all in your response
- Sources are provided separately below your response

Answer:
"""


def main():
    """Main function to handle command line queries."""
    parser = argparse.ArgumentParser(description="Query the entrepreneur biography database")
    parser.add_argument("query_text", type=str, help="The query text")
    parser.add_argument("--k", type=int, default=DEFAULT_K, help="Number of chunks to retrieve")
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD, help="Similarity threshold")
    parser.add_argument("--filter", type=str, help="Filter by metadata field (e.g., 'subject:Elon Musk')")
    
    args = parser.parse_args()
    
    # Process the query
    response, sources = query_database(
        args.query_text,
        k=args.k,
        threshold=args.threshold,
        filter_str=args.filter
    )
    
    print(response)


def query_database(query_text: str, k: int = DEFAULT_K, threshold: float = DEFAULT_THRESHOLD, filter_str: str = None) -> str:
    """
    Query the database and return formatted response.
    
    Args:
        query_text: The query string
        k: Number of chunks to retrieve
        threshold: Similarity threshold
        filter_str: Optional metadata filter (e.g., "subject:Elon Musk")
    
    Returns:
        Formatted response with sources
    """
    # Prepare embedding function
    embedding_function = OpenAIEmbeddings()
    
    # Load the database
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
    
    # Parse filter if provided
    filter_dict = None
    if filter_str:
        try:
            key, value = filter_str.split(":", 1)
            filter_dict = {key: value}
            print(f"Applying filter: {filter_dict}")
        except ValueError:
            print(f"Warning: Invalid filter format '{filter_str}'. Use 'key:value' format.")
    
    # Search with relevance scores
    if filter_dict:
        results = db.similarity_search_with_relevance_scores(
            query_text,
            k=k,
            filter=filter_dict
        )
    else:
        results = db.similarity_search_with_relevance_scores(query_text, k=k)
    
    # Check if we have results above threshold
    if len(results) == 0:
        return "No results found."
    
    # Filter by threshold and show what we're using
    filtered_results = [(doc, score) for doc, score in results if score >= threshold]
    
    print(f"\n--- Retrieval Info ---")
    print(f"Total results: {len(results)}")
    print(f"Results above threshold ({threshold}): {len(filtered_results)}")
    
    if len(filtered_results) == 0:
        # Show best score even if below threshold
        best_score = max(score for _, score in results)
        return f"No results above threshold {threshold}. Best score was {best_score:.3f}. Try lowering the threshold with --threshold flag."
    
    # Use filtered results
    results = filtered_results
    
    # Display relevance scores
    print("\nRelevance scores:")
    for i, (doc, score) in enumerate(results):
        subject = doc.metadata.get("subject", "Unknown")
        source = doc.metadata.get("source", "Unknown")
        print(f"  {i+1}. {subject} ({source}): {score:.3f}")
    print("---\n")
    
    # Prepare context
    context_parts = []
    sources_info = []
    
    for doc, score in results:
        # Create context entry with metadata
        subject = doc.metadata.get("subject", "Unknown")
        themes = doc.metadata.get("themes", "")
        
        # If themes is a string (from ChromaDB), keep it; if it's a list, join it
        if isinstance(themes, list):
            themes_str = ", ".join(themes[:3])
        else:
            # It's already a string (comma-separated from our metadata conversion)
            themes_str = themes
        
        # Simple context entry without inline source citations
        context_entry = f"{doc.page_content}\n"
        
        context_parts.append(context_entry)
        
        # Collect source info WITH chunk content
        source_info = {
            "subject": subject,
            "company": doc.metadata.get("company", "Unknown"),
            "themes": themes_str,  # Use the string version
            "score": score,
            "chunk_text": doc.page_content,  # ADD chunk content
            "chunk_index": doc.metadata.get("chunk_index", "?"),
            "source_file": doc.metadata.get("source", "Unknown")
        }
        sources_info.append(source_info)
    
    context_text = "\n---\n".join(context_parts)
    
    # Create prompt
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(
        context=context_text,
        question=query_text,
        num_sources=len(results)
    )
    
    # Get response from model
    model = ChatOpenAI(temperature=0)
    response_text = model.predict(prompt)
    
    # Format final response without sources (sources are handled by web UI)
    formatted_response = response_text
    
    return formatted_response, sources_info


if __name__ == "__main__":
    main()

"""
Web UI for testing MotivateAI prompts and queries.

This FastAPI application provides a web interface for:
1. Testing different queries against the entrepreneur database
2. Adjusting parameters (k, threshold, filters)
3. Viewing formatted responses with sources
4. Query history tracking
"""

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from typing import Optional, List
from datetime import datetime
import os
import sys

# Add the current directory to Python path to import query_data
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from query_data import query_database

app = FastAPI(title="MotivateAI Query Interface", description="Web UI for testing entrepreneur RAG queries")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Query history storage
query_history = []

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the main query interface."""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "history": query_history[-10:]  # Show last 10 queries
    })

@app.post("/query")
async def process_query(
    request: Request,
    query: str = Form(...),
    k: int = Form(5),
    threshold: float = Form(0.5),
    filter_str: Optional[str] = Form(None)
):
    """Process a query and return results."""
    if not query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    if not 1 <= k <= 10:
        raise HTTPException(status_code=400, detail="k must be between 1 and 10")

    if not 0.1 <= threshold <= 1.0:
        raise HTTPException(status_code=400, detail="threshold must be between 0.1 and 1.0")

    try:
        # Query the database using existing function
        result = query_database(query, k=k, threshold=threshold, filter_str=filter_str)

        # Add to history
        query_history.append({
            "query": query,
            "k": k,
            "threshold": threshold,
            "filter": filter_str,
            "result": result,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        # Keep only last 50 queries
        if len(query_history) > 50:
            query_history.pop(0)

        return templates.TemplateResponse("result.html", {
            "request": request,
            "query": query,
            "result": result,
            "k": k,
            "threshold": threshold,
            "filter": filter_str,
            "history": query_history[-5:]  # Show last 5 for context
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")

@app.get("/history")
async def view_history(request: Request):
    """View query history."""
    return templates.TemplateResponse("history.html", {
        "request": request,
        "history": query_history
    })

@app.get("/clear-history")
async def clear_history():
    """Clear query history."""
    query_history.clear()
    return {"message": "Query history cleared"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

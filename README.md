# Entrepreneur Biography RAG System

A Retrieval Augmented Generation (RAG) system for analyzing entrepreneur biographies and podcast transcripts from the Founders podcast.

## Features

- **Improved Chunking**: 1200 character chunks with 250 character overlap
- **Rich Metadata**: Manual tagging of themes, concepts, time periods, and company stages
- **Better Retrieval**: Retrieves 5 chunks by default with lower similarity threshold (0.5)
- **Synthesis Prompts**: Encourages pattern recognition across multiple entrepreneurs
- **Web Interface**: Interactive web UI for easy querying with parameter adjustment and query history

## Setup

⚠️ **See [SETUP.md](SETUP.md) for detailed setup instructions.**

**Quick start:**
1. Create `.env` file with your OpenAI API key
2. Install dependencies: `pip install -r requirements.txt`
3. Create database: `python create_database.py`
4. Run web interface: `python app.py` (available at http://localhost:8000)

## Web Interface

The web interface provides an intuitive way to interact with the entrepreneur database:

- **Query Interface**: Enter natural language questions about entrepreneurs and business strategies
- **Parameter Tuning**: Adjust retrieval parameters (k values, similarity thresholds) in real-time
- **Rich Responses**: View formatted responses with source citations from the transcripts
- **Query History**: Track and revisit previous queries with their parameters and results
- **Responsive Design**: Clean, modern interface styled with Tailwind CSS

### Using the Web Interface

1. Start the server: `python app.py`
2. Open `http://localhost:8000` in your browser
3. Enter your query in the search box
4. Adjust parameters as needed (number of results, similarity threshold)
5. Click "Search" to get results with source citations
6. View query history or clear it as needed

## Command Line Usage

Query the database:
```bash
python query_data.py "How did Elon Musk approach hiring at SpaceX?"
```

With custom parameters:
```bash
python query_data.py "What are examples of perseverance?" --k 8 --threshold 0.4
```

Filter by metadata:
```bash
python query_data.py "product design philosophy" --filter "subject:Steve Jobs"
```

## Example Queries

1. **Pattern Recognition**:
   - "Compare the hiring strategies of different founders"
   - "What are common themes in how entrepreneurs handle failure?"

2. **Specific Examples**:
   - "Give me examples of first principles thinking from the transcripts"
   - "How did James Dyson's 5127 prototypes demonstrate perseverance?"

3. **Cross-Entrepreneur Analysis**:
   - "Compare Elon Musk and Steve Jobs' approach to product design"
   - "What manufacturing insights appear across different entrepreneurs?"

4. **Time-Based Queries**:
   - "What strategies did entrepreneurs use in early-stage companies?"
   - "How did approaches change from the 1970s to 2020s?"

## Document Metadata

Each document is tagged with:
- **Subject**: The entrepreneur's name
- **Company**: Primary company discussed
- **Industry**: Business sector
- **Themes**: High-level concepts (perseverance, product_design, etc.)
- **Key Concepts**: Specific ideas (5127_prototypes, reality_distortion_field)
- **Time Period**: Era covered in the transcript
- **Stage**: Company lifecycle stage (early, growth, mature, full_lifecycle)

## Files

- `metadata_config.py`: Document metadata configuration
- `create_database.py`: Build the vector database
- `query_data.py`: Command-line query interface
- `app.py`: FastAPI web application
- `test_embeddings.py`: Test embedding functionality
- `requirements.txt`: Python dependencies
- `templates/`: HTML templates for the web interface (index.html, result.html, history.html)
- `static/`: CSS and static assets for the web interface

## Troubleshooting

1. **No results found**: Lower the similarity threshold with `--threshold 0.4`
2. **API key errors**: Ensure your `.env` file has a valid OpenAI API key
3. **Import errors**: Run `pip install -r requirements.txt` again
4. **Web interface not loading**: Ensure the database has been created with `python create_database.py`

## Future Enhancements

- Add more sophisticated filtering by multiple metadata fields
- Implement theme-based clustering
- Export insights to a knowledge graph
- Add user authentication for the web interface


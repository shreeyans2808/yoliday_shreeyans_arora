# Groq Chatbot with Dual Summaries

This Streamlit application uses Groq's powerful language models to generate both casual and formal summaries of user queries, with PostgreSQL database storage on Render.

## Features

- Interactive web interface using Streamlit
- Uses Groq's Llama 4 model for high-quality text generation
- Provides both casual and formal summaries
- Stores all summaries in PostgreSQL database
- View recent summaries history
- Clean and responsive UI
- Fast and efficient inference

## Setup

1. Get your Groq API key:
   - Sign up at https://console.groq.com
   - Create a new API key from your dashboard

2. Set up PostgreSQL database on Render:
   - Create a new PostgreSQL database on Render
   - Note down the database credentials (host, name, user, password)

3. Create a `.env` file in the project root and add your credentials:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   DB_HOST=your_render_db_host
   DB_NAME=your_db_name
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_PORT=5432
   ```

4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

## Usage

1. Enter your query or text in the input area
2. Click the "Generate Summaries" button
3. View both casual and formal summaries side by side
4. Check the "Recent Summaries" tab to view your history

## Database Schema

The application uses a PostgreSQL database with the following schema:

```sql
CREATE TABLE summaries (
    id SERIAL PRIMARY KEY,
    original_text TEXT NOT NULL,
    casual_summary TEXT NOT NULL,
    formal_summary TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

## Note

The application uses Groq's Llama 4 model, which provides high-quality, contextually aware summaries. The summaries are generated in real-time using Groq's fast inference engine and stored in a PostgreSQL database for future reference. 
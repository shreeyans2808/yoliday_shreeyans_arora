# Groq Chatbot with Dual Summaries

This Streamlit application uses Groq's powerful language models to generate both casual and formal summaries of user queries, with PostgreSQL database storage on Neon DB.

## Features

- Interactive web interface using Streamlit
- Uses Groq's Llama 4 model for high-quality text generation
- Provides both casual and formal summaries simultaneously
- Stores all summaries in Neon PostgreSQL database
- View recent summaries history with user-specific tracking
- Clean and responsive UI
- Fast and efficient inference
- User ID-based history tracking

## Technical Approach

The application follows a multi-layered architecture:

1. **Frontend Layer (Streamlit)**
   - Clean, responsive UI with tabs for generation and history
   - Real-time summary generation with loading spinners
   - User ID validation and enforcement
   - Side-by-side display of casual and formal summaries

2. **AI Layer (Groq)**
   - Utilizes Groq's Llama 4 model for high-quality text generation
   - Two distinct prompt templates:
     - Casual: Conversational, friendly tone
     - Formal: Professional, academic tone
   - Parallel processing of both summary types

3. **Database Layer (Neon PostgreSQL)**
   - Efficient connection pooling for database operations
   - Two main tables:
     - `users`: Tracks unique user IDs
     - `summaries`: Stores original text and both summary types
   - Automatic timestamp tracking for history

## Setup

1. Get your Groq API key:
   - Sign up at https://console.groq.com
   - Create a new API key from your dashboard

2. Set up Neon PostgreSQL database:
   - Create a new project on Neon (https://neon.tech)
   - Note down the database credentials (host, name, user, password)
   - The database will be automatically initialized with required tables

3. Create a `.env` file in the project root and add your credentials:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   DB_HOST=your_neon_db_host
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

1. **User ID Requirement**
   - The application requires a User ID to function
   - Without a User ID, the application will not proceed
   - This ensures proper tracking and history management
   - Example User IDs:
     - "shreeyans" (pre-configured with history)
     - Create your own unique User ID

2. **Generating Summaries**
   - Enter your User ID in the input field
   - Enter your query or text in the input area
   - Click the "Generate Summaries" button
   - View both casual and formal summaries side by side
   - Summaries are automatically saved to your user history

3. **Viewing History**
   - Switch to the "Recent Summaries" tab
   - View your last 5 summaries
   - Each summary entry shows:
     - Original text
     - Casual summary
     - Formal summary
     - Timestamp

## Database Schema

The application uses a Neon PostgreSQL database with the following schema:

```sql
CREATE TABLE users (
    user_id VARCHAR(50) PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE summaries (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    original_text TEXT NOT NULL,
    casual_summary TEXT NOT NULL,
    formal_summary TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
```

## Security Features

- User ID validation and enforcement
- Secure database connection pooling
- Environment variable protection
- API key management through Streamlit secrets

## Performance Considerations

- Connection pooling for efficient database operations
- Parallel processing of summaries
- Optimized database queries with proper indexing
- Efficient memory management through Streamlit session state

## Testing

The application includes a comprehensive test suite located in the `tests/` directory. The tests cover various aspects of the application:

### Test Structure

1. **Unit Tests**
   - `test_prompt_formatting.py`: Tests the prompt formatting logic
   - `test_ai_generation.py`: Tests AI generation with mocked responses
   - `test_integration.py`: Tests complete application flow

2. **Test Fixtures** (`conftest.py`)
   - `mock_streamlit`: Mocks Streamlit session state and client
   - `mock_db_connection`: Mocks database connection and cursor with proper context management

### Running Tests

To run the tests, use the following commands:

```bash
# Install test dependencies
pip install -r requirements.txt

# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run tests with coverage report
pytest --cov=.

# Run specific test file
pytest tests/test_prompt_formatting.py
```

### Test Coverage

The test suite includes:

1. **Prompt Formatting Tests** (`test_prompt_formatting.py`)
   - Casual prompt formatting
   - Formal prompt formatting
   - Empty input handling
   - Invalid style handling
   - API error handling

2. **AI Generation Tests** (`test_ai_generation.py`)
   - Casual summary generation with mocked API responses
   - Formal summary generation with mocked API responses
   - API error handling with proper exception testing

3. **Integration Tests** (`test_integration.py`)
   - Complete application flow from input to database storage
   - Database operations with proper connection management
   - Error handling for database operations
   - Connection release verification

### Test Dependencies

The following testing packages are included:
- `pytest`: Main testing framework
- `pytest-cov`: Coverage reporting
- `pytest-mock`: Mocking capabilities

### Test Best Practices

1. **Mocking Strategy**
   - Streamlit session state is mocked for all tests
   - Database connections are properly mocked with context management
   - API responses are mocked to ensure consistent testing

2. **Error Handling**
   - All error cases are properly tested
   - Database errors are handled and verified
   - API errors are caught and tested

3. **Connection Management**
   - Database connections are properly released
   - Connection pooling is mocked and verified
   - Context managers are properly tested

## Note

The application uses Groq's Llama 4 model, which provides high-quality, contextually aware summaries. The summaries are generated in real-time using Groq's fast inference engine and stored in a Neon PostgreSQL database for future reference. The User ID system ensures that each user can access their own history while maintaining data separation and privacy. 
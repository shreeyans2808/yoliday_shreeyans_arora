import pytest
from unittest.mock import patch, MagicMock
from app import generate_summaries, save_to_db, get_recent_summaries

def test_complete_flow(mock_streamlit, mock_db_connection):
    """Test complete application flow from input to database storage"""
    mock_conn, mock_cursor = mock_db_connection
    
    # Mock the database operations
    mock_cursor.fetchone.return_value = [1]  # Mock the summary_id return
    mock_cursor.fetchall.return_value = [(1, "test", "casual", "formal", "2024-01-01")]
    
    with patch('app.st.session_state.client.chat.completions.create') as mock_create:
        # Mock Groq API response
        mock_response = mock_create.return_value
        mock_response.choices = [type('obj', (object,), {'message': type('obj', (object,), {'content': 'Test summary'})})]

        # Test data
        user_id = "test_user"
        test_text = "This is a test text"

        # Generate summaries
        casual_summary = generate_summaries(test_text, "casual")
        formal_summary = generate_summaries(test_text, "formal")

        # Save to database
        summary_id = save_to_db(user_id, test_text, casual_summary, formal_summary)
        assert summary_id == mock_cursor.fetchone()[0]  # Check against the mocked value

        # Retrieve recent summaries
        recent_summaries = get_recent_summaries(user_id)
        assert recent_summaries == mock_cursor.fetchall()  # Check against mocked data

        # Verify database operations
        mock_cursor.execute.assert_called()
        mock_conn.commit.assert_called()

def test_database_error_handling(mock_streamlit, mock_db_connection):
    """Test database error handling"""
    mock_conn, mock_cursor = mock_db_connection
    mock_cursor.execute.side_effect = Exception("Database Error")

    result = save_to_db("test_user", "test", "casual", "formal")
    assert result is None  # The function returns None on error
    mock_conn.rollback.assert_called()  # Verify rollback was called 
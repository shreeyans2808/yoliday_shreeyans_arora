import pytest
from unittest.mock import patch
from app import generate_summaries

def test_casual_summary_generation(mock_streamlit):
    """Test casual summary generation with mocked API response"""
    with patch('app.st.session_state.client.chat.completions.create') as mock_create:
        # Mock the Groq API response
        mock_response = mock_create.return_value
        mock_response.choices = [type('obj', (object,), {'message': type('obj', (object,), {'content': 'This is a casual summary'})})]

        result = generate_summaries("test text", "casual")
        assert result == "This is a casual summary"
        mock_create.assert_called_once()

def test_formal_summary_generation(mock_streamlit):
    """Test formal summary generation with mocked API response"""
    with patch('app.st.session_state.client.chat.completions.create') as mock_create:
        # Mock the Groq API response
        mock_response = mock_create.return_value
        mock_response.choices = [type('obj', (object,), {'message': type('obj', (object,), {'content': 'This is a formal summary'})})]

        result = generate_summaries("test text", "formal")
        assert result == "This is a formal summary"
        mock_create.assert_called_once()

def test_api_error_handling(mock_streamlit):
    """Test API error handling"""
    with patch('app.st.session_state.client.chat.completions.create') as mock_create:
        mock_create.side_effect = Exception("API Error")
        with pytest.raises(Exception) as exc_info:
            generate_summaries("test text", "casual")
        assert str(exc_info.value) == "API Error" 
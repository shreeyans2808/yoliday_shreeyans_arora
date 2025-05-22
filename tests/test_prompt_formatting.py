import pytest
from unittest.mock import patch
from app import generate_summaries

def test_casual_prompt_formatting(mock_streamlit):
    """Test casual prompt formatting"""
    with patch('app.st.session_state.client.chat.completions.create') as mock_create:
        mock_response = mock_create.return_value
        mock_response.choices = [type('obj', (object,), {'message': type('obj', (object,), {'content': 'Test casual summary'})})]
        
        test_text = "This is a test text"
        result = generate_summaries(test_text, "casual")
        assert result == 'Test casual summary'
        mock_create.assert_called_once()

def test_formal_prompt_formatting(mock_streamlit):
    """Test formal prompt formatting"""
    with patch('app.st.session_state.client.chat.completions.create') as mock_create:
        mock_response = mock_create.return_value
        mock_response.choices = [type('obj', (object,), {'message': type('obj', (object,), {'content': 'Test formal summary'})})]
        
        test_text = "This is a test text"
        result = generate_summaries(test_text, "formal")
        assert result == 'Test formal summary'
        mock_create.assert_called_once()

def test_empty_input(mock_streamlit):
    """Test handling of empty input"""
    with pytest.raises(ValueError, match="Empty input"):
        generate_summaries("", "casual")

def test_invalid_style(mock_streamlit):
    """Test handling of invalid style"""
    with pytest.raises(ValueError, match="Invalid style"):
        generate_summaries("test", "invalid_style")

def test_api_error_handling(mock_streamlit):
    """Test API error handling"""
    with patch('app.st.session_state.client.chat.completions.create') as mock_create:
        mock_create.side_effect = Exception("API Error")
        with pytest.raises(Exception, match="API Error"):
            generate_summaries("test", "casual") 
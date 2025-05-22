import pytest
import streamlit as st
from unittest.mock import MagicMock, patch

@pytest.fixture(autouse=True)
def mock_streamlit():
    """Mock Streamlit session state for all tests"""
    st.session_state = MagicMock()
    st.session_state.client = MagicMock()
    return st.session_state

@pytest.fixture
def mock_db_connection():
    """Mock database connection for tests"""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    
    # Set up the cursor context manager
    mock_cursor.__enter__.return_value = mock_cursor
    mock_cursor.__exit__.return_value = None
    mock_conn.cursor.return_value = mock_cursor
    
    # Mock the connection pool and release function
    with patch('db_config.connection_pool') as mock_pool, \
         patch('db_config.release_db_connection') as mock_release:
        mock_pool.getconn.return_value = mock_conn
        yield mock_conn, mock_cursor 
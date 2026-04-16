import json
import pytest
from unittest.mock import patch, mock_open
from pathlib import Path
from src.save_raw import save_raw_to_json  # Change this to your actual filename

@patch("src.save_raw.Path.mkdir")
@patch("src.save_raw.open", new_callable=mock_open) # Mocks the file writing
def test_save_raw_to_json_success(mock_file, mock_mkdir):
    # Arrange
  test_data = {"key": "value"}
    
    # Act
  save_raw_to_json(test_data)
    
    # Assert
    # Check if storage.mkdir was called
  mock_mkdir.assert_called()
    
    # Check if the file was opened for writing
  mock_file.assert_called_once()
    
    # Capture the data passed to json.dump
    # We check if the write handle was used
  handle = mock_file()
    
    # Combine all write calls to see the final string
  written_data = "".join(call.args[0] for call in handle.write.call_args_list)
    
    # Verify the content is correct
  assert "key" in written_data
  assert "value" in written_data

@patch("src.save_raw.open", side_effect=Exception("Disk Full"))
def test_save_raw_to_json_error(mock_file):
    # This ensures that even if writing fails, the script doesn't crash 
    # (because of your try/except block)
  test_data = {"key": "value"}
  save_raw_to_json(test_data)

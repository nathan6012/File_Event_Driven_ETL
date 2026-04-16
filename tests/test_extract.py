import pytest
from pathlib import Path
from unittest.mock import patch, mock_open,MagicMock

from src.extract_file import fetch_csv_data


@patch("pathlib.Path.exists", return_value=False)
def test_no_storage_folder(mock_exists):
  result = fetch_csv_data()
  assert result == []


#est 2: storage exists but no CSV files
@patch("pathlib.Path.exists", return_value=True)
@patch("pathlib.Path.glob", return_value=[])
def test_no_csv_files(mock_glob, mock_exists):
  result = fetch_csv_data()
  assert result == []


# est 3: successful CSV read (FIXED)
@patch("pathlib.Path.exists", return_value=True)
@patch("pathlib.Path.glob")
@patch("pathlib.Path.stat")
@patch("builtins.open", new_callable=mock_open, read_data="name,age\nJohn,30\nJane,25")
def test_read_csv_success(mock_file, mock_stat, mock_glob, mock_exists):

  fake_file = MagicMock(spec=Path)
    
    # mock stat() return value
  mock_stat.return_value = type("stat", (), {"st_mtime": 123456})()

  mock_glob.return_value = [fake_file]

  result = fetch_csv_data()

  assert len(result) == 2
  assert result[0]["name"] == "John"
  assert result[1]["age"] == "25"
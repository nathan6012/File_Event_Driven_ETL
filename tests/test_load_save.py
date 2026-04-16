import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from unittest.mock import patch, AsyncMock, MagicMock

from src.load_save_data import load_to_postgres


# =========================
# Test: load_to_postgres
# =========================
@pytest.mark.asyncio
@patch("src.load_save_data.create_async_engine")
@patch("src.load_save_data.os.getenv", return_value="postgresql+asyncpg://user:pass@localhost/db")
async def test_load_to_postgres(mock_env, mock_engine):
    
    # -------------------------
    # Mock connection + engine
    # -------------------------
  mock_conn = AsyncMock()
  mock_conn.run_sync = AsyncMock()
  mock_conn.execute = AsyncMock()

  mock_engine_instance = MagicMock()
  mock_engine_instance.begin.return_value.__aenter__.return_value = mock_conn
  mock_engine_instance.begin.return_value.__aexit__.return_value = None
  
  mock_engine_instance.dispose = AsyncMock()
  mock_engine.return_value = mock_engine_instance

    # -------------------------
    # Sample input data
    # -------------------------
  data = [
        {
            "customer_name": "John",
            "age": 30,
            "email": "john@mail.com",
            "purchase_amount": 100.50,
            "purchase_quantity": 2,
            "discount": 5.0,
            "purchase_date": "2024-01-01"
        }
    ]

    # -------------------------
    # Call function
    # -------------------------
  await load_to_postgres(data)

    # -------------------------
    # Assertions
    # -------------------------
  mock_engine.assert_called_once()
  mock_conn.run_sync.assert_called_once()
  mock_conn.execute.assert_called_once()


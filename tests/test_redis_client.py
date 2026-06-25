import json
from unittest.mock import patch, MagicMock

import connectors.redis_client as rc


# =========================
# TEST ENQUEUE
# =========================

@patch("connectors.redis_client.redis_client")
def test_enqueue_job(mock_redis):

    job = {"job_id": "123", "type": "test"}

    rc.enqueue_job(job)

    mock_redis.lpush.assert_called_once()

    args, _ = mock_redis.lpush.call_args

    assert args[0] == rc.QUEUE_NAME
    assert json.loads(args[1]) == job


# =========================
# TEST DEQUEUE (SUCCESS)
# =========================

@patch("connectors.redis_client.redis_client")
def test_dequeue_job(mock_redis):

    job = {"job_id": "123"}

    mock_redis.brpop.return_value = ("etl_jobs", json.dumps(job))

    result = rc.dequeue_job()

    mock_redis.brpop.assert_called_once_with(rc.QUEUE_NAME, timeout=5)

    assert result == job


# =========================
# TEST DEQUEUE (EMPTY)
# =========================

@patch("connectors.redis_client.redis_client")
def test_dequeue_empty(mock_redis):

    mock_redis.brpop.return_value = None

    result = rc.dequeue_job()

    assert result is None


# =========================
# TEST SET STATUS
# =========================

@patch("connectors.redis_client.redis_client")
def test_set_job_status(mock_redis):

    rc.set_job_status("job123", "queued")

    mock_redis.set.assert_called_once_with(
        "job:job123:status",
        "queued"
    )


# =========================
# TEST GET STATUS
# =========================

@patch("connectors.redis_client.redis_client")
def test_get_job_status(mock_redis):

    mock_redis.get.return_value = "done"

    result = rc.get_job_status("job123")

    mock_redis.get.assert_called_once_with("job:job123:status")

    assert result == "done"
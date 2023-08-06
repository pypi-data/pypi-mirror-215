import time

import pytest

from cmon.logging.predefined import default_logger
from cmon.logging.profile import profiling


@pytest.fixture
def default_logger_propagate():
    default_logger.logger.propagate = True
    yield
    default_logger.logger.propagate = False


def test_logging_profile_profiling(caplog, default_logger_propagate):
    @profiling
    def foo():
        time.sleep(1)

    foo()
    # profiling format: CMON@79684[I]: foo time: 0.00042528799999996814s memory Δ 376.0 KB 47.3 MB -> 47.7 MB
    assert 'time' in caplog.text

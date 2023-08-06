import pytest
from reactivex.testing import ReactiveTest, TestScheduler

@pytest.fixture
def test_scheduler():
    return TestScheduler()
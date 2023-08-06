from reactivex.testing.recorded import Recorded

def assert_equal_messages(messages: list[Recorded], expected_messages: list[Recorded]):
    for i, (actual, expected) in enumerate(zip(messages, expected_messages)):
        actual_timestamp, actual_content = actual.time, actual.value
        expected_timestamp, expected_content = expected.time, expected.value

        assert actual_timestamp == expected_timestamp
        if actual_content.has_value:
            assert actual_content.value == expected_content.value
        else:
            assert actual_content.exception == expected_content.exception
        assert actual_content == expected_content
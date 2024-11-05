import datetime
from copy import deepcopy

import pytest

from social_credit import SOCIAL_CREDIT_FILE_PATH, CreditManager
from transaction import Transaction

TEST_SCORES = {
    "user1": {
        "total": 100,
        "history": [
            {
                "amount": 50,
                "reason": "good behavior",
                "timestamp": "2021-08-02T14:22:27.774",
                "author": "test",
            },
            {
                "amount": 50,
                "reason": "helping others",
                "timestamp": "2021-08-03T14:22:27.774",
                "author": "test",
            },
        ],
    },
    "user2": {
        "total": 200,
        "history": [
            {
                "amount": 110,
                "reason": "good behavior2",
                "timestamp": "2021-08-02T14:22:27.774",
                "author": "test",
            },
            {
                "amount": 90,
                "reason": "helping others2",
                "timestamp": "2021-08-03T14:22:27.774",
                "author": "test",
            },
        ],
    },
}

TEST_TRANSACTION = Transaction(
    "test", datetime.datetime.now().isoformat(), "+ 10 test_user test reason"
)

TEST_CREDIT_MANAGER = CreditManager()
TEST_CREDIT_MANAGER._social_credit_scores = TEST_SCORES


def test_get_user_score():
    assert TEST_CREDIT_MANAGER.get_user_score("user1") == 100


def test_get_user_score_user_not_found():
    with pytest.raises(ValueError, match="User not found"):
        TEST_CREDIT_MANAGER.get_user_score("user69")


def test_get_formated_user_history():
    expected_history = (
        "By test at 2021-08-02T14:22:27.774: +50 good behavior\n"
        "By test at 2021-08-03T14:22:27.774: +50 helping others\n"
    )
    assert TEST_CREDIT_MANAGER.get_formated_user_history("user1") == expected_history


def test_get_formated_all_scores():
    expected_scores = "user1: 100\nuser2: 200\n"
    assert TEST_CREDIT_MANAGER.get_formated_all_scores() == expected_scores


def test_process_transaction_message():
    original_scores = deepcopy(TEST_CREDIT_MANAGER._social_credit_scores)
    message = "+10 user1 test reason"
    try:
        response = TEST_CREDIT_MANAGER.process_transaction_message("test", message)
        assert response == "user1 is now at 110 social credit points"
    finally:
        TEST_CREDIT_MANAGER._social_credit_scores = original_scores


def test_process_transaction_message2():
    original_scores = deepcopy(TEST_CREDIT_MANAGER._social_credit_scores)
    message = "+10 user1 test reason2"
    try:
        response = TEST_CREDIT_MANAGER.process_transaction_message("test", message)
        assert response == "user1 is now at 110 social credit points"
    finally:
        TEST_CREDIT_MANAGER._social_credit_scores = original_scores


def test_process_transaction_message_invalid_transaction():
    message = "blah balh"
    response = TEST_CREDIT_MANAGER.process_transaction_message("test", message)
    assert response == "Invalid transaction message"


def test_perform_transaction():
    TEST_CREDIT_MANAGER._perform_transaction(TEST_TRANSACTION)
    assert TEST_CREDIT_MANAGER.get_user_score("user1") == 110


# def test_perform_transaction_user_not_found():
#     transaction = TEST_TRANSACTION(
#         "test_user", datetime.datetime.now().isoformat(), "+10 user2 test reason"
#     )

#     with pytest.raises(ValueError, match="User not found"):
#         TEST_CREDIT_MANAGER._perform_transaction(transaction)

from datetime import datetime

import pytest

from transaction import Transaction


def test_transaction_valid():
    author = "test_author"
    time = datetime.now()
    transaction_str = "+ 100 user1 for services"

    transaction = Transaction(author, time, transaction_str)

    assert transaction.author == author
    assert transaction.time == time
    assert transaction.sign == "+"
    assert transaction.amount == 100
    assert transaction.user == "user1"
    assert transaction.reason == "for services"


def test_transaction_invalid_message():
    author = "test_author"
    time = datetime.now()
    transaction_str = "blah balh"

    with pytest.raises(ValueError, match="Invalid transaction message"):
        Transaction(author, time, transaction_str)


def test_transaction_missing_reason():
    author = "test_author"
    time = datetime.now()
    transaction_str = "+ 100 user1"

    with pytest.raises(ValueError, match="Reason is required"):
        Transaction(author, time, transaction_str)

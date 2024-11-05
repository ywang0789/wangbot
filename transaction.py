import datetime
import re

REGEX_PATTERN = r"([+-])\s*(\d+)\s+(\w+)\W?(.*)?"  # group 1: sign, group 2: amount, group 3: user, group 4: reason


class Transaction:
    def __init__(self, author, time, sign, amount, user, reason):
        self.author = author
        self.time = time
        self.sign = sign
        self.amount = amount
        self.user = user
        self.reason = reason

    def __init__(self, author: str, time: datetime, transaction_str: str):
        """extracts transaction details from message and creates transaction object"""

        self.author = author
        self.time = time

        matches = re.match(REGEX_PATTERN, transaction_str)

        self.sign, self.amount, self.user, self.reason = None, None, None, None

        if matches:
            self.sign = matches.group(1)
            self.amount = int(matches.group(2))
            self.user = matches.group(3)
            self.reason = matches.group(4)

        if not self.sign or not self.amount or not self.user:
            raise ValueError("Invalid transaction message")

        if not self.reason:
            raise ValueError("Reason is required")

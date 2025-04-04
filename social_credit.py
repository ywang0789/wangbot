import datetime
import json
from pprint import pprint

from secret.secret import ID_TO_NAME_MAP
from transaction import Transaction

SOCIAL_CREDIT_FILE_PATH = "./secret/credit_score.json"


"""
social scores dict format:
{
    "user1": 
    {
        "total": 123,
        "history": 
        [
            {
                "amount": 123,
                "reason": "because cool",
                "timestamp": "2021-08-02T14:22:27.774"
                "author": "user2"   
            }
        ]
    }
}
"""


class CreditManager:
    def __init__(self):
        self._social_credit_scores = {}
        self._load_scores(SOCIAL_CREDIT_FILE_PATH)

    def process_transaction_message(self, author_id: str, message: str) -> str:
        """Processes a transaction message and returns a confirmation message (ENTIRE PROCESS)"""
        time = datetime.datetime.now().isoformat()

        # find arthor name from ID MAP
        if author_id not in ID_TO_NAME_MAP:
            raise ValueError(f"User ID not registered in ID_TO_NAME_MAP: {author_id}")

        author_name = ID_TO_NAME_MAP[author_id]

        try:
            transaction = Transaction(author_name, time, message)
        except ValueError as e:
            return str(e)

        # cannot perform transaction on self
        if author_name == transaction.user:
            raise ValueError(f"Cannot perform transaction on yourself {author_name}")

        try:
            self._perform_transaction(transaction)
        except ValueError as e:
            return str(e)

        try:
            total = self.get_user_score(transaction.user)
        except ValueError as e:
            return str(e)

        confirmation_str = f"{transaction.user} is now at {total} social credit points"

        return confirmation_str

    def get_user_score(self, user: str) -> int:
        """returns the total score of a user"""
        user = user.lower()
        if user not in self._social_credit_scores:
            raise ValueError("User not found")
        return self._social_credit_scores[user]["total"]

    def get_formated_user_history(self, user: str) -> str:
        """returns the transaction history of a user in a formatted string"""
        user = user.lower()
        history = self._get_user_history(user)
        formatted_history_str = ""
        for transaction in history:
            # if amount is possitive, add a plus sign
            if transaction["amount"] > 0:
                amount = f"+{transaction['amount']}"
            reason = transaction["reason"]
            time = transaction["timestamp"]

            # if no author, set to "N/A" ***because author was implemented later***
            if "author" in transaction:
                author = transaction["author"]
            else:
                author = "N/A"

            formatted_history_str += f"By {author} at {time}: {amount} {reason}\n"
        return formatted_history_str

    def get_formated_all_scores(self) -> str:
        """returns the total scores of all users in a formatted string"""
        scores = self._get_all_scores()
        formatted_scores = ""
        for user in scores:
            formatted_scores += f"{user}: {scores[user]}\n"
        return formatted_scores

    def _perform_transaction(self, transaction: Transaction) -> None:
        """Performs a transaction on a user from values AND updates file"""

        # fk off justin
        if transaction.amount > 42069:
            raise ValueError("Justin please stahp")

        if transaction.user not in self._social_credit_scores:
            raise ValueError(f"User not found: {transaction.user}")

        if transaction.sign == "+":
            signed_amount = transaction.amount
        elif transaction.sign == "-":
            signed_amount = -transaction.amount
        else:
            raise ValueError("Invalid sign")

        self._social_credit_scores[transaction.user]["total"] += signed_amount

        transaction_dict = {
            "amount": signed_amount,
            "reason": transaction.reason,
            "timestamp": transaction.time,
            "author": transaction.author,
        }

        self._social_credit_scores[transaction.user]["history"].append(transaction_dict)

        self._sort_scores()
        self._save_scores(SOCIAL_CREDIT_FILE_PATH)

    def _get_user_history(self, user: str) -> list[dict]:
        """returns the transaction history of a user"""
        if user not in self._social_credit_scores:
            raise ValueError("User not found")
        return self._social_credit_scores[user]["history"]

    def _get_all_scores(self) -> dict:
        """returns the total scores of all users"""
        scores = {}
        for user in self._social_credit_scores:
            scores[user] = self._social_credit_scores[user]["total"]

        return scores

    def _load_scores(self, score_file_path: str) -> None:
        """reads and loads social credit scores from file"""
        try:
            with open(score_file_path, "r") as file:
                self._social_credit_scores = json.load(file)
        except Exception as e:
            print(f"Failed to load scores: {e}")

    def _save_scores(self, score_file_path: str) -> None:
        """writes current scores to file"""
        try:
            with open(score_file_path, "w") as file:
                json.dump(self._social_credit_scores, file)
        except Exception as e:
            print(f"Failed to save scores: {e}")

    def _sort_scores(self):
        """sorte scores by total score from highest to lowest"""
        self._social_credit_scores = dict(
            sorted(
                self._social_credit_scores.items(),
                key=lambda item: item[1]["total"],
                reverse=True,
            )
        )

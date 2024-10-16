import datetime
import json
import re

SOCIAL_CREDIT_FILE_PATH = "./secret/credit_score.json"

REGEX_PATTERN = r"([+-])\s*(\d+)\s+(\w+)\W(.*)"


class CreditManager:
    def __init__(self):
        self.social_credit_scores = {}
        self.load_scores()

    def process_transaction_message(self, message: str) -> str:
        """Processes a transaction message and returns a confirmation message (ENTIRE PROCESS)"""
        sign, amount, user, reason = self.__parse_transaction_message(message)
        time = datetime.datetime.now().isoformat()
        self.__perform_transaction(sign, amount, user, reason, time)

        try:
            total = self.get_user_score(user)
        except ValueError as e:
            return str(e)

        confirmation = f"{user} is now at {total} social credit points"
        return confirmation

    def __perform_transaction(
        self, sign: str, amount: int, user: str, reason: str, time: str
    ) -> None:
        """Performs a transaction on a user from values AND updates file"""
        # fk off justin
        if amount > 42069:
            raise ValueError("Justin please stahp")

        if user not in self.social_credit_scores:
            raise ValueError("User not found")
        if sign == "+":
            signed_amount = amount
        elif sign == "-":
            signed_amount = -amount
        else:
            raise ValueError("Invalid sign")

        self.social_credit_scores[user]["total"] += signed_amount

        transaction = {"amount": signed_amount, "reason": reason, "timestamp": time}

        self.social_credit_scores[user]["history"].append(transaction)

        self.save_scores()

    def __parse_transaction_message(self, message: str) -> tuple[str, int, str, str]:
        """extracts transaction details from message"""
        matches = re.match(REGEX_PATTERN, message)
        sign, amount, user, reason = None, None, None, None
        if matches:
            sign = matches.group(1)
            amount = int(matches.group(2))
            user = matches.group(3)
            reason = matches.group(4)

        if not sign or not amount or not user:
            raise ValueError("Invalid transaction message")

        return sign, amount, user, reason

    def get_user_score(self, user: str) -> int:
        """returns the total score of a user"""
        if user not in self.social_credit_scores:
            raise ValueError("User not found")
        return self.social_credit_scores[user]["total"]

    def __get_user_history(self, user: str) -> list[dict]:
        """returns the transaction history of a user"""
        if user not in self.social_credit_scores:
            raise ValueError("User not found")
        return self.social_credit_scores[user]["history"]

    def get_formated_user_history(self, user: str) -> str:
        """returns the transaction history of a user in a formatted string"""
        history = self.__get_user_history(user)
        formatted_history = ""
        for transaction in history:
            # if amount is possitive, add a plus sign
            if transaction["amount"] > 0:
                amount = f"+{transaction['amount']}"
            reason = transaction["reason"]
            time = transaction["timestamp"]
            formatted_history += f"{time}: {amount} {reason}\n"
        return formatted_history

    def __get_all_scores(self) -> dict:
        """returns the total scores of all users"""
        scores = {}
        for user in self.social_credit_scores:
            scores[user] = self.social_credit_scores[user]["total"]

        return scores

    def get_formated_all_scores(self) -> str:
        """returns the total scores of all users in a formatted string"""
        scores = self.__get_all_scores()
        formatted_scores = ""
        for user in scores:
            formatted_scores += f"{user}: {scores[user]}\n"
        return formatted_scores

    def load_scores(self) -> None:
        """reads and loads social credit scores from file"""
        try:
            with open(SOCIAL_CREDIT_FILE_PATH, "r") as file:
                self.social_credit_scores = json.load(file)
        except Exception as e:
            print(f"Failed to load scores: {e}")

    def save_scores(self) -> None:
        """writes current scores to file"""
        try:
            with open(SOCIAL_CREDIT_FILE_PATH, "w") as file:
                json.dump(self.social_credit_scores, file)
        except Exception as e:
            print(f"Failed to save scores: {e}")


if __name__ == "__main__":
    cm = CreditManager()
    cm.load_scores()
    # print(cm.social_credit_scores)

    # string = "+1 yao because cool"

    # text = cm.process_transaction_message(string)

    # print(text)

    print(cm.get_formated_all_scores())

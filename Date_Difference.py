# Authors: Mitchell Walker, Jeff Ananias
# Course: CS361
# Assignment: 9 - Big Pool Implementation
# Microservice: Date Difference

import time
from datetime import date, datetime

REQUEST_FILE = "date_diff.txt"


def main() -> None:
    """Start microservice as continuous process."""
    greet()
    last_file_text = ""
    while True:
        file_text = get_file_text()
        last_file_text = process_request(file_text, last_file_text)
        time.sleep(0.5)


def greet() -> None:
    """Greet user and advise request-response format."""
    print("\nDate Difference Microservice is running.")
    print("Waiting for date request in date_diff.txt.")
    print("Please use date request format: YYYY-MM-DD\n")


def get_file_text() -> str:
    """
    Return text from REQUEST FILE if exists; else create empty file and
    return empty string.
    """
    try:
        with open(REQUEST_FILE, "r") as f:
            file_text = f.read().strip()
    except FileNotFoundError:
        with open(REQUEST_FILE, "w") as f:
            f.write("")
        file_text = ""
    return file_text


def process_request(file_text: str, last_file_text: str) -> str:
    """Return response based on request and write file text if new."""
    if file_text != "" and file_text != last_file_text:
        # Ignore file that already has a response in it
        if is_response_message(file_text):
            return file_text
        # Else, treat the file contents as a new request
        else:
            print("Request Received: " + file_text)
            response = calculate_date_difference(file_text)
            with open(REQUEST_FILE, "w") as f:
                f.write(response)
            print("Response Sent:" + response + "\n")
            return response
    return last_file_text


def is_response_message(file_text: str) -> bool:
    """
    Return True if file_text is response instead of request;
    else return False.
    """
    res_type_1 = bool(file_text.startswith("DAYS_REMAINING:"))
    res_type_2 = bool(file_text.startswith("OVERDUE:"))
    res_type_3 = bool(file_text.startswith("DUE_TODAY:"))
    res_type_4 = bool(file_text.startswith("DATE_DIFF_ERROR:"))
    return bool(res_type_1 or res_type_2 or res_type_3 or res_type_4)


def calculate_date_difference(given_date_text: str) -> str:
    """
    Return message showing if input date in YYYY-MM-DD format is
    future, past, or today.
    """
    # Validate format
    try:
        given_date = datetime.strptime(given_date_text, "%Y-%m-%d").date()
    except ValueError:
        return "DATE_DIFF_ERROR: Invalid date format. Use YYYY-MM-DD."

    # Positive diff is future date; negative diff is past date
    date_difference = (given_date - date.today()).days

    if date_difference > 0:
        return "DAYS_REMAINING: " + str(date_difference)
    elif date_difference < 0:
        return "OVERDUE: " + str(abs(date_difference))
    else:
        return "DUE_TODAY: 0"


if __name__ == "__main__":
    main()

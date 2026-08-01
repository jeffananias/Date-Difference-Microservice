import time

REQUEST_FILE = "date_diff.txt"


def response_is_ready(response):
    """Checks if the text file contains a completed microservice response"""

    if response.startswith("DAYS_REMAINING:"):
        return True
    elif response.startswith("OVERDUE:"):
        return True
    elif response.startswith("DUE_TODAY:"):
        return True
    elif response.startswith("DATE_DIFF_ERROR:"):
        return True
    else: 
        return False


def request_date_difference(given_date):
    # Write the request date into the text file
    with open(REQUEST_FILE, "w") as file:
        file.write(given_date)

    print("Request sent: " + given_date)

    # Wait for microservice to replace the request with a response
    while True:
        with open(REQUEST_FILE, "r") as file:
            response = file.read().strip()

        if response_is_ready(response):
            return response

        time.sleep(0.5)


def main():
    print("Date Difference Test Program")
    print("============================")

    test_dates = [
        "2026-08-03",
        "2020-01-01",
        "bad-date"
    ]

    for test_date in test_dates:
        response = request_date_difference(test_date)
        print(f"Response received: {response}")
        print()


if __name__ == "__main__":
    main()
from datetime import date, datetime
import time

REQUEST_FILE = 'date_diff.txt'


def calculate_date_difference(given_date_text: str) -> None:
    """
    Take a date string in YYYY-MM-DD format and compare it to today's date.
    Return a message showing if the date is in the future, past, or today.
    """
    # Validate format
    try:
        given_date = datetime.strptime(given_date_text, '%Y-%m-%d').date()
    except ValueError:
        return 'DATE_DIFF_ERROR: Invalid date format. Use YYYY-MM-DD.'

    # Get today's date
    current_date = date.today()

    # Subtract today's date from given date
    # Positive diff is future date; negative diff is past date
    date_difference = given_date - current_date
    days_difference = date_difference.days

    if days_difference > 0:
        response = 'DAYS_REMAINING: ' + str(days_difference)
    elif days_difference < 0:
        response = 'OVERDUE: ' + str(abs(days_difference))
    else:
        response = 'DUE_TODAY: 0'

    return response


def is_response_message(file_text: str) -> None:
    """
    Check response to avoid reading Date_Difference response as new request.
    """
    if file_text.startswith('DAYS_REMAINING:'):
        return True
    elif file_text.startswith('OVERDUE:'):
        return True
    elif file_text.startswith('DUE_TODAY:'):
        return True
    elif file_text.startswith('DATE_DIFF_ERROR:'):
        return True
    else:
        return False


def run_microservice() -> None:
    """
    Run Date_Difference microservice as continuous process.
    """
    print('Date Difference Microservice is running ')
    print('\nWaiting for date request in date_diff.txt ')
    print('\nPlease use date request format: YYYY-MM-DD')
    print()

    last_file_text = ''

    while True:
        try:
            with open(REQUEST_FILE, 'r') as file:
                file_text = file.read().strip()
        except FileNotFoundError:
            with open(REQUEST_FILE, 'w') as file:
                file.write('')
            file_text = ''

        # Only start working if the file has text and it is different from the
        # last thing read
        if file_text != '' and file_text != last_file_text:

            # Ignore file that already has a response in it
            if is_response_message(file_text):
                last_file_text = file_text

            # Else, treat the file contents as a new request
            else:
                print('Request Received: ' + file_text)

                response = calculate_date_difference(file_text)

                with open(REQUEST_FILE, 'w') as file:
                    file.write(response)

                print('Response Sent: ' + response)
                print()

                last_file_text = response

        time.sleep(0.5)


if __name__ == '__main__':
    run_microservice()
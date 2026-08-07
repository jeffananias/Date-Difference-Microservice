from datetime import date, datetime
import time

REQUEST_FILE = 'date_diff.txt'


def calculate_date_difference(given_date_text: str) -> str:
    """
    Take a date string in YYYY-MM-DD format and compare it to today's date.
    Return a message showing if the date is in the future, past, or today.
    """
    # Validate format
    try:
        given_date = datetime.strptime(given_date_text, '%Y-%m-%d').date()
    except ValueError:
        return 'DATE_DIFF_ERROR: Invalid date format. Use YYYY-MM-DD.'

    # Positive diff is future date; negative diff is past date
    date_difference = (given_date - date.today()).days

    if date_difference > 0:
        return 'DAYS_REMAINING: ' + str(days_difference)
    elif date_difference < 0:
        return 'OVERDUE: ' + str(abs(days_difference))
    else:
        return 'DUE_TODAY: 0'


def is_response_message(file_text: str) -> bool:
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


def greet() -> None:
    """
    Greet user and advise date format.
    """
    print('Date Difference Microservice is running.\n')
    print('Waiting for date request in date_diff.txt.\n')
    print('Please use date request format: YYYY-MM-DD\n')


def process_request(file_text: str, last_file_text: str) -> str:
    """
    Return response based on request and print and write file text if new.
    """
    if file_text != '' and file_text != last_file_text:
        
        # Ignore file that already has a response in it
        if is_response_message(file_text):
            return file_text

        # Else, treat the file contents as a new request
        else:
            print('Request Received: ' + file_text)

            response = calculate_date_difference(file_text)

            with open(REQUEST_FILE, 'w') as file:
                file.write(response)

            print('Response Sent: ' + response)
            print()

            return response

def run_microservice() -> None:
    """
    Run Date_Difference microservice as continuous process.
    """
    greet()

    last_file_text = ''
    while True:
        try:
            with open(REQUEST_FILE, 'r') as file:
                file_text = file.read().strip()
        except FileNotFoundError:
            with open(REQUEST_FILE, 'w') as file:
                file.write('')
            file_text = ''

        last_file_text = process_request(file_text, last_file_text)

        time.sleep(0.5)


if __name__ == '__main__':
    run_microservice()
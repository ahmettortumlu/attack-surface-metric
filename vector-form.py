import requests
from bs4 import BeautifulSoup

def check_for_form():
    url = input("Enter the URL: ")
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Check if there is at least one form element
        form_elements = soup.find_all('form')

        return len(form_elements) > 0
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return False

# Example usage
has_form = check_for_form()

if has_form:
    print("The ", url, " contains a form.")
else:
    print("No form found on the page.")

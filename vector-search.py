import requests
from bs4 import BeautifulSoup

def check_search_bar(url):
    try:
        # Send a GET request to the specified URL
        response = requests.get(url)
        response.raise_for_status()

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Check for the presence of input elements with type="search"
        search_inputs = soup.find_all('input', {'type': 'search'})

        # Check for the presence of form elements
        form_elements = soup.find_all('form')

        # Determine if there is a search bar
        has_search_bar = len(search_inputs) > 0 or len(form_elements) > 0

        return has_search_bar

    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return False

# Get the URL from the user
user_url = input("Enter the URL: ")

# Call the function and get the result
has_search_bar = check_search_bar(user_url)

# Print the result
if has_search_bar:
    print("The page has a search bar.")
else:
    print("No search bar found on the page.")

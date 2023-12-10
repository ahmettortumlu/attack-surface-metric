import requests
from bs4 import BeautifulSoup

def check_webpage_features(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Check for the presence of input elements with type="file"
        file_input_elements = soup.find_all('input', {'type': 'file'})
        has_file_upload = len(file_input_elements) > 0

        # Check for hidden elements
        hidden_elements = soup.find_all(lambda tag: 'hidden' in tag.attrs)
        has_hidden_elements = len(hidden_elements) > 0

        # Check for form elements
        form_elements = soup.find_all('form')
        has_form = len(form_elements) > 0

        # Check for search bar
        search_inputs = soup.find_all('input', {'type': 'search'})
        has_search_bar = len(search_inputs) > 0 or len(form_elements) > 0

        return {
            "has_hidden_elements": has_hidden_elements,
            "has_form": has_form,
            "has_search_bar": has_search_bar,
            "has_file_upload": has_file_upload
        }

    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return {
            "has_hidden_elements": False,
            "has_form": False,
            "has_search_bar": False,
            "has_file_upload": False
        }

# Function to check features for a list of URLs
def check_features_for_url_list(url_list):
    feature_results = {
        "has_hidden_elements": False,
        "has_form": False,
        "has_search_bar": False,
        "has_file_upload": False
    }

    for url in url_list:
        url_features = check_webpage_features(url)

        # Update feature flags if any URL has the corresponding feature
        for feature in feature_results:
            feature_results[feature] = feature_results[feature] or url_features[feature]

    return feature_results

# Example usage
user_urls_input = input("Enter a list of URLs separated by commas: ")
user_urls = [url.strip() for url in user_urls_input.split(',')]

result = check_features_for_url_list(user_urls)

print("\nAggregate Feature Results:")
print(f"Has Hidden Elements: {result['has_hidden_elements']}")
print(f"Has Form: {result['has_form']}")
print(f"Has Search Bar: {result['has_search_bar']}")
print(f"Has File Upload: {result['has_file_upload']}")

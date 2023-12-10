import requests
from bs4 import BeautifulSoup
import re

def check_page_features(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # AJAX Kontrolü
        ajax_used = soup.find('script', {'src': True, 'type': 'text/javascript'}) is not None

        # Java Kontrolü
        java_used = soup.find('applet') is not None or soup.find('object') is not None

        # Feed Kontrolü
        feed_links = soup.find_all('link', {'rel': ['alternate', 'feed'], 'type': ['application/rss+xml', 'application/atom+xml']})
        feed_used = len(feed_links) > 0

        # JavaScript Kontrolü
        javascript_used = soup.find('script') is not None

        # Server Side Script Kontrolü
        server_side_code = soup.find('script', {'src': True})
        server_side_used = server_side_code is not None

        # Dışarıdan çağrılan JavaScript Dosyalarını Tespit Et
        js_script_pattern = re.compile(r'https?://[^\s]+\.js')
        script_tags = soup.find_all('script', {'src': js_script_pattern})
        external_js_scripts = [script['src'] for script in script_tags]

        return {
            'AJAX Used': ajax_used,
            'Java Used': java_used,
            'Feed Used': feed_used,
            'JavaScript Used': javascript_used,
            'Server Side Script Used': server_side_used,
            'External JavaScript Scripts': external_js_scripts
        }
    except requests.exceptions.RequestException as e:
        return {
            'Error': f"Error making request: {e}"
        }

# Function to check features for a list of URLs
def check_features_for_url_list(url_list):
    aggregate_results = {
        'AJAX Used': False,
        'Java Used': False,
        'Feed Used': False,
        'JavaScript Used': False,
        'Server Side Script Used': False,
        'External JavaScript Scripts': []
    }

    for url in url_list:
        result = check_page_features(url)
        features = result  # Fix: Use 'result' directly instead of 'result['Features']'

        # Update aggregate results based on current URL's features
        for feature in aggregate_results:
            aggregate_results[feature] = aggregate_results[feature] or features[feature]

    return aggregate_results

# Example usage
user_urls_input = input("Enter a list of URLs separated by commas: ")
user_urls = [url.strip() for url in user_urls_input.split(',')]

results = check_features_for_url_list(user_urls)

# Print the results
print("\nAggregate Results:")
for feature, value in results.items():
    print(f"{feature}: {value}")

import requests

def list_cookies():
    # Get the URL from the user
    url = input("Enter the URL: ")

    try:
        # Send a GET request to the specified URL
        response = requests.get(url)
        response.raise_for_status()

        # Extract and print the cookies from the response
        cookies = response.cookies
        if cookies:
            print("Cookies:")
            for cookie in cookies:
                print(f"{cookie.name}: {cookie.value}")
        else:
            print("No cookies found.")

    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")

# Call the function
list_cookies()

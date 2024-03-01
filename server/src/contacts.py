import requests

def search_contacts(access_token, query):
    """Search for a contact by query using the Google People API."""
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    
    # Attempt to search in saved contacts first
    saved_contacts_url = 'https://people.googleapis.com/v1/people:searchContacts'
    other_contacts_url = 'https://people.googleapis.com/v1/otherContacts:search'
    
    # Common params
    params = {
        'query': query,
        'pageSize': 1,  # We only need the first matching contact
        'readMask': 'names,emailAddresses',
    }

    # Search saved contacts
    response = requests.get(saved_contacts_url, headers=headers, params=params)
    if response.status_code == 200 and response.json().get('results'):
        return extract_contact_info(response.json()['results'][0])

    # If no match found, search other contacts
    response = requests.get(other_contacts_url, headers=headers, params=params)
    if response.status_code == 200 and response.json().get('results'):
        return extract_contact_info(response.json()['results'][0])

    # If no match in both, return None or an empty dict
    return {}

def extract_contact_info(result):
    """Extract and format contact info from search result."""
    person = result.get('person', {})
    names = person.get('names', [])
    emailAddresses = person.get('emailAddresses', [])
    
    contact_info = {
        'name': names[0].get('displayName', 'Unknown') if names else 'Unknown',
        'email': emailAddresses[0].get('value', 'No email') if emailAddresses else 'No email',
    }
    return contact_info


def get_names_from_emails(access_token, emails):
    """
    Searches for contacts based on email addresses and returns a string
    of comma-separated names.
    """
    names_list = []

    for email in emails:
        email = email.strip()  # Remove any leading/trailing whitespace
        if email:  # Ensure email is not empty
            contact_info = search_contacts(access_token, email)
            name = contact_info.get('name')
            if name == 'Unknown' or name == None:
                # Parse the name from the email address if API returns 'Unknown'
                name_part = email.split('@')[0]
                name = name_part.replace('.', ' ').replace('_', ' ').title()
            names_list.append(name)
    return ', '.join(names_list) if names_list else "<name not available>"

# # Example usage
# access_token = "ya29.a0AfB_byDldnEaDi-XxB7pynWRikwMIa1HvVK5ndKwvwnPgByJbiJY-GmkTgX7T95SRFABHTwbVe02vCgWvxtX6KbO6fGmlh5F6cwMKRteMsWn6wiwA06yD9mgsFpQfGkZv0suDwNPx4m_VN6eYBM05BxXCAegn--xB2f5aCgYKASMSARISFQHGX2MisegZ5fXlto1PNOspPXdUqw0171"
# query = 'ryan@farpointhq.com'
# # contact_info = search_contacts(access_token, query)
# # print(contact_info)
# emails = ['ryan@farpointhq.com', 'raoof@farpointhq.com']
# get_names_from_emails(access_token, emails)

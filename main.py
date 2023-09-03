import re
import datetime
import requests
from bs4 import BeautifulSoup

# URL of the webpage to scrape
url = 'https://icodethis.com/app'

# File to append URLs to
urls_only_file = 'iCodeThisMockupURLs.txt'
markdown_file = 'iCodeThisMockupURLs.md'

try:
  # Send an HTTP GET request to the URL
  response = requests.get(url)

  # Check if the request was successful (status code 200)
  if response.status_code == 200:
    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all <img> tags on the page associated with challenge
    img_tags = soup.find_all('img', {'alt': 'Challenge Image'})

    # Loop through the <img> tags
    for img_tag in img_tags:
      src_attribute = img_tag.get('src', '')
      alt_attribute = img_tag.get('alt', '')

      # two images match our query, the first
      # is a base64 img unrelated to the daily challenge
      if 'base64' not in src_attribute.lower():
        print('Found <img> tag without "base64" in src attribute')
        image_url = img_tag.get('src')
        full_url = f'https://www.icodethis.com{image_url}'
        print(f'Image URL: {full_url}')

        # Send an HTTP GET request to the image URL
        res = requests.get(full_url)
        # Get the content of the image
        image_content = res.content

        # Regular expression pattern to find 'Daily Challenge Name'
        pattern = r'image\?url=%2Fimages%2Fprojects%2F(.*?)\.jpg'

        # Use re.search to find the match in the input string
        match = re.search(pattern, image_url)

        challenge_name = ''
        timestamp = ''

        # Check if a match was found
        if match:
          challenge_name = match.group(1)  # Extract the matched substring
          print(f'challenge_name: {challenge_name}\n')

          # Get the current date and time
          current_datetime = datetime.datetime.now()

          # Format the timestamp as a string
          timestamp = current_datetime.strftime("%Y-%m-%d")
        else:
          print("No match found")

        # Specify the file path where you want to save the image
        new_image_file_path = f'./mockups/{timestamp}-{challenge_name}.jpg'

        # DOWNLOAD IMAGE
        with open(new_image_file_path, 'wb') as image_file:
            image_file.write(image_content)

        # SAVE IMAGE URL
        with open(urls_only_file, 'a') as urlFile:
          # Append the URL to the file
          urlFile.write(full_url + '\n')

        # MARKDOWN DOC
        with open(markdown_file, 'a') as mdFile:
          challenge_name = challenge_name.replace(
              '_', ' ').title()
          mdFile.write(f'[{timestamp}: {challenge_name}]({full_url})  \n')
        break

      # print their attributes
      # attributes = img_tag.attrs
      # print('Attributes for the current image tag:')
      # for attr_name, attr_value in attributes.items():
      #     print(f'{attr_name}: {attr_value}')
      # print('\n')
  else:
    print('Failed to retrieve the webpage. Status code:', response.status_code)

except requests.exceptions.RequestException as e:
  print('An error occurred:', e)

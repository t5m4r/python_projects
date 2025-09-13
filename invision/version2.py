import pprint
import webbrowser
import os

# Install google-api-python-client
from googleapiclient.discovery import build 

# This function uses a minimal/bare bones HTML 
# For each item in the results, use them following keys: 
# title, snippet, link for high level summar
# For image preview, check if pagemap->metatags->og:image is present first. If not, then use pagemap->cse_thumbnail->src as the image element/thumbail link with default size of the image to be picked from  pagemap->cse_thumbnail->height and  pagemap->cse_thumbnail->width
# pagemap->metatags if present, then use og:image as the image URL, og:image:height, and og:image:width as the dimensions of the img element. 

def makeHtml(res):
    html = "<html><body>"

    html += "<h1>Tushar's AI project</h1>"
    for item in res['items']:
        html += f"<h2>{item['title']}</h2>"
        html += f"<p>{item['snippet']}</p>"
        html += f"<a href='{item['link']}'>{item['link']}</a><br><br>"
        if 'metatags' in item['pagemap']:
            html += f"<img src='{item['pagemap']['metatags'][0]['og:image']}' height='200'><br><br>"
        else:
            html += f"<img src='{item['pagemap']['cse_thumbnail'][0]['src']}' height='200'><br><br>"
        # Add a new paragraph element with text "This is the theme colour", and inline CSS style the value of pagemap->metatags->theme-color
        if 'metatags' in item['pagemap'] and 'theme-color' in item['pagemap']['metatags'][0]:
            html += f"<p style='color: {item['pagemap']['metatags'][0]['theme-color']}'>This is the theme colour</p>"
        else:
            html += f"<p style='background-color: pink'>This is Tushar's brand colour ;) </p>"
    html += "</body></html>"
    return html

def main():
    # Build a service object for interacting with the API. Visit
    # the Google APIs Console <http://code.google.com/apis/console>
    # to get an API key for your own application.
    service = build(
        "customsearch", "v1", developerKey=os.environ.get('GOOGLE_SEARCH_API_SECRET_KEY')
    )

    # This is setting up the query API using Google's Python library. 
    res = (
        service.cse()
        .list(
            q="Lionel Messi",
            cx="464fb427999714d0e", # Search Engine ID previously configured on Google Developer's website user profile
            num=3,
            hl="en"
        )
        .execute()
    )
    # Print the type of the res obect
    print(type(res))
    pprint.pprint(res)
    # Loop over all the elements in res and show the keys available. 
    print('⬇️ Keys available to read in Google Results are ⬇️')
    for key in res.keys():
        print(key)
    print('⬆️ Keys available to read in Google Results are ⬆️')
    # Loop over all 'items` key values , and show the keys within each of them
    print('⬇️ Keys available to read in Google Results items are ⬇️')
    for item in res['items']:
        for key in item.keys():
            print(key)
    print('⬆️ Keys available to read in Google Results items are ⬆️')

    # Now we pretty-print the contents of the items keys. We only pick title, snippet, and link attributes (keys). Put the search result's index number
    # at the front of the print statement or display them tabbed appropropriately.
    for i, item in enumerate(res['items']):
        print(f"{i+1}. {item['title']}")
        print(f"   {item['snippet']}")
        print(f"   {item['link']}\n")

    # Call the function to pick out the important keys from the results map 
    # and write their values into the corresponding elements on the HTML text (markup)
    html = makeHtml(res)
    # Writing the HTML file to disk as output.html
    with open("output.html", "w") as f:
        f.write(html)
    # Launch the OS-default browser to open the output.html file
    try:
        browser = webbrowser.get("safari")  # Or "firefox", "safari"
        # Get the current working directory of this process from OS
        current_dir = os.getcwd()
        browser.open(f"file://{current_dir}/output.html")
    except webbrowser.Error as e:
        print(f"Error opening browser: {e}")

if __name__ == "__main__":
    main()

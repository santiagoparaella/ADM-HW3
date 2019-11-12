def crawl(url, path):

    if type(path) != str: # To be sure that the path is a string
        raise Exception('input path must be a string! Not a {}'.format(type(path)))
    request = req.get(url) # Get the url contents
    soup = BeautifulSoup(request.text, 'html.parser') # read the content of the url as html (it will shows the html file)
    ftableS = str(soup.find_all('table')) # The link are placed in a table, we must access in it
    table = BeautifulSoup(ftableS, 'html.parser') # Now we can read (in html format) the table
    urls = table.find_all('a') # search url is between <a> and <\a>
    i = 11420 # I get links form 20000 to 30000 (we start count from 0)

# Let's wotk with each link:

    for link in urls[1420:]:
        with open(''.join([path, 'article_', str(i), '.html']), 'w') as f: # We want to save each content of the url
            text = req.get(link.get('href')) # "href" is part of the html code that allows us to go to the website

            if text.status_code == 429: # Too many request status
                time.sleep(20*60) # The time we have to wait in seconds before a new request
                text = req.get(link.get('href')) # Try again to get the page
                f.write(text.text) # Save he file
            elif text.status_code == 404: # Not found page
                text = "Page not Found" # Print in the file not found
                f.write(text) # Save he file
            elif text.status_code == 200: # Everything has gone well
                f.write(text.text) # Save he file
            else:
                f.write("Some error occured")


        if i % 100 == 0:
            time.sleep(random.randrange(10, 30)) # Wait few seconds between each request
            i += 1
        else:
            i += 1 # Increase the number of file (for the name of th efile)

    print('finish crwaling') # Let em know when the process is finished

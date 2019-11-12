def find_intro(site):

    # Deal with Page not FOund:
    if "Page not Found" in site.text: # If the isn't the page we return -1 it takes less time to find it later
        return -1

    # Deal with Disanbiguation page:

    disanbiguation = site.find("a", {"title": "Category:Disambiguation pages"})
    if disanbiguation: # Disanbiguation page = a page that sends you to other pages (we decide to skip them, we add only the title)
        return "NA"

    # Leet's start to find intro:

    intro_lst = [] # A list which will contain each paragraph
    par_before_intro = site.find("table", {"class": "infobox vevent"}) # It is the element before the paragrphs we need

    if par_before_intro:
        el = par_before_intro.find_next_sibling()  # The element changes everytime the cycle ends (at the beginning we start from the line after table tag
    else:  # If there isn't the info box, we can find the intro right after the following tag (but it is a child of this)
        el = site.find("div", {"class": "mw-parser-output"}).findChild()

    while True:

        try:
            el_name = el.name
        except:
            el_name = "" # In case we don't get the tag

        if el_name != "p": # We stop when we found the first tag different from p
            intro = "\n".join(intro_lst) # So we create a string with the whole text
            break # And stop the cycle
        else:
            intro_lst.append(el.text) # We append that part as text in our list
            el = el.find_next_sibling() # And we switch to the next element

    return intro


def find_plot(site):

    # Deal with page not found

    if site.text == "Page not Found": # If the isn't the page we return -1 it takes less time to find it later
        return -1

    # Deal with disanbiguation page:

    disanbiguation = site.find("a", {"title": "Category:Disambiguation pages"})
    if disanbiguation: # Disanbiguation page = a page that sends the user to other pages (we decide to skip them, we add only the title)
        return "NA"

    # Let's start to find the plot

    plot_lst = [] # A list which will contain each paragraph
    paragraphs = site.find_all("h2") # All elements in site that have the tag "h2"
    plot_par = [i for i in paragraphs if (i.find("span", {"id": "Plot"}) or i.find("span", {"id": "Plot_summary"})
                                          or i.find("span", {"id": "Premise"}) or i.find("span", {"id": "Premise"}))]

    if not plot_par: # If there isn't the plot paragraph
        return "NA"

    el = plot_par[0].find_next_sibling() # The element changes everytime the cycle ends (at the beginning we start from the line after h2 tag)
    while True:

        try:
            el_name = el.name
        except:
            el_name = "" # In case we don't get the tag

        if el_name != "p": # When occurs the first tag different from p we stop the loop
            plot = "\n".join(plot_lst) # So we create a string with the whole text
            break # And stop the cycle
        else:
            plot_lst.append(el.text) # We append that part as text in our list
            el = el.find_next_sibling() # And we switch to the next element

    return plot


def find_info(site):

# Let's create a dictionary whith the neeed information

    info_dict = {"Title": "NA",
                "Directed by": "NA",
                "Produced by": "NA",
                "Written by": "NA",
                "Starring": "NA",
                "Music by": "NA",
                "Release date": "NA",
                "Country": "NA",
                "Language": "NA",
                "Budget": "NA"
                }

    # Deal with Page not found:

    if site.text == "Page not Found": # If the isn't the page we return -1 it takes less time to find it later
        for key, _ in info_dict.items():
            info_dict[key] = -1
        return info_dict

    # Deal with disanbiguation page:

    disanbiguation = site.find("a", {"title": "Category:Disambiguation pages"})
    if disanbiguation: # Disanbiguation page = a page that sends you to other pages (we decide to skip them, we add only the title)
        info_dict["Title"] = site.find("h1").text
        return info_dict

    # Let's loop:

    table = site.find('table', {"class" : "infobox vevent"}) # Let's get the table where the infobox is palced

    if not table: # It can happen that there isn't the infobox
        return info_dict

    rows = table.find_all("tr") # It represents the table records

    for el in rows:

        try:
            key = el.find("th").get_text(strip=True) # They are the Titles (Ex. "Prodced by")
        except:
            key = "NA"

        try:
            values = el.find("td").get_text(strip=True) # The attributes of each title
        except:
            values = "NA"

        if values == "NA": # It seems title is the only one that has values == "NA"

            info_dict["Title"] = key

        elif key == "Directed by":

            info_dict[key] = values

        elif key == "Produced by":

            info_dict[key] = values

        elif key == "Written by":

            info_dict[key] = values

        elif key == "Starring":

            info_dict[key] = values

        elif key == "Music by":

            info_dict[key] = values

        elif key == "Release date":

            info_dict[key] = values

        elif key == "Running time":

            info_dict[key] = values

        elif key == "Country":

            info_dict[key] = values

        elif key == "Language":

            info_dict[key] = values

        elif key == "Budget":

            info_dict[key] = values

    return info_dict


def clean_all(site):

    raw_intro = find_intro(site)
    raw_plot = find_plot(site)
    raw_info = find_info(site)

    # Let's clean the text from any html symhols and to wikipedia lables ("[n]") for intro an dplot:

    if type(raw_intro) is int: # It is page noy found, so we can skip it
        intro = raw_intro
        plot = raw_plot
        info_dict = raw_info

    else:

        intro_not_clean = re.sub('(?<=\w|\.|\s)((\\\'s)|(\\n){,10}|(\\\'))', "", raw_intro) # We Remove all html symbols ("\'s, \n")
        intro = re.sub(r'(?<=\w|\.|\s)(\[\d+\]){,10}', "", intro_not_clean) # Remove any notes (in Wikipedia it links to another page)

        plot = re.sub('(?<=\w|\.|\s)((\\\'s)|(\\n){,10}|(\\\'))', "", raw_plot) # We all Remove html symbols ("\'s, \n")

        # Let's clean the infobox:

        info_dict = {}

        for key, value in raw_info.items():

            if key == "Title":

                if value != "NA":
                    if re.search(r'(?<=\w|\.|\s)(\[\d+\]){,10}', value): # Delet any reference (ex. [1]), We'll do for each variable and put always as first if
                        clean = re.sub(r'(?<=\w|\.|\s)(\[\d+\]){,10}', "", value)
                        info_dict[key] = clean
                    else:
                        info_dict[key] = value
                else:
                    info_dict[key] = value

            elif key == "Directed by":

                if value != "NA":
                    if re.search(r'(?<=\w|\.|\s)(\[\d+\]){,10}', value): # Delet any reference (ex. [1])
                        clean = re.sub(r'(?<=\w|\.|\s)(\[\d+\]){,10}', "", value)
                        info_dict[key] = clean
                    else:
                        info_dict[key] = value
                else:
                    info_dict[key] = value

            elif key == "Produced by":

                if value != "NA":
                    if re.search(r'(?<=\w|\.|\s)(\[\d+\]){,10}', value): # Delet any reference (ex. [1])
                        clean = re.sub(r'(?<=\w|\.|\s)(\[\d+\]){,10}', "", value)

                        if re.search(r'(?<!\s|\-|\_|\/)(?=[A-Z])', clean):
                            split = re.split(r'(?<!\s|\-|\_|\/)(?=[A-Z])', clean) # Divide joint name (ex. Radish CamuJohn Snow)
                            info_dict[key] = ", ".join([i for i in split if i != ""]) # transform the split list a string (don't add empty stings)
                        else:
                            info_dict[key] = clean
                    else:

                        info_dict[key] = value
                else:

                    info_dict[key] = value

            elif key == "Written by":

                if value != "NA":
                    if re.search(r'(?<=\w|\.|\s)(\[\d+\]){,10}', value): # Delet any reference (ex. [1])
                        clean = re.sub(r'(?<=\w|\.|\s)(\[\d+\]){,10}', "", value)
                        info_dict[key] = clean

                        if re.search(r'(?<=\w)\((.*?)\)', clean):
                            split = re.sub('(?<=\w)\((.*?)\)', "", clean) # Remove the parentesis with the role of each person
                            info_dict[key] = split
                        elif re.search(r'(?<!\s|\-|\_|\/)(?=[A-Z])', clean):
                            split = re.split(r'(?<!\s|\-|\_|\/)(?=[A-Z])', clean) # Divide joint name (ex. Radish CamuJohn Snow)
                            info_dict[key] = ", ".join([i for i in split if i != ""]) # transform the split list a string (don't add empty stings)
                        else:
                            info_dict[key] = value
                    else:
                        info_dict[key] = value
                else:
                    info_dict[key] = value


            elif key == "Starring":

                if value != "NA":
                    if re.search(r'(?<=\w|\.|\s)(\[\d+\]){,10}', value): # Delet any reference (ex. [1])
                        clean = re.sub(r'(?<=\w|\.|\s)(\[\d+\]){,10}', "", value)
                        info_dict[key] = clean

                        if re.search(r'(?<!\s|\-|\_|\/)(?=[A-Z])', clean):
                            split = re.split(r'(?<!\s|\-|\_|\/)(?=[A-Z])', clean) # Divide joint name (ex. Radish CamuJohn Snow)
                            info_dict[key] = ", ".join([i for i in split if i != ""]) # transform the split list a string (don't add empty stings)
                        else:
                            info_dict[key] = value
                    else:
                        info_dict[key] = value
                else:
                    info_dict[key] = value

            elif key == "Music by":

                if value != "NA":
                    if re.search(r'(?<=\w|\.|\s)(\[\d+\]){,10}', value): # Delet any reference (ex. [1]), We'll do for each variable and put always as first if
                        clean = re.sub(r'(?<=\w|\.|\s)(\[\d+\]){,10}', "", value)
                        info_dict[key] = clean
                    else:
                        info_dict[key] = value
                else:
                    info_dict[key] = value

            elif key == "Release date":

                if value != "NA":
                    if re.search(r'(?<=\w|\.|\s)(\[\d+\]){,10}', value): # Delet any reference (ex. [1])
                        clean = re.sub(r'(?<=\w|\.|\s)(\[\d+\]){,10}', "", value)
                        info_dict[key] = clean

                        if re.search(r'(\(\d+\))', clean):
                            year = re.sub('(\(\d+\))', "", clean) # Get only the year (ex. 2005(2005))
                            info_dict[key] = year
                        elif re.search(r'(?<=\()(\d{4})', clean):
                            year = re.search('(?<=\()(\d{4})', clean) # Get only the year when (random characters(yyyy-mm-dd))
                            info_dict[key] = year.group()
                        else:
                            info_dict[key] = value
                    else:
                        info_dict[key] = value
                else:
                    info_dict[key] = value

            elif key == "Running time":

                if value != "NA":
                    if re.search(r'(?<=\w|\.|\s)(\[\d+\]){,10}', value): # Delet any reference (ex. [1]), We'll do for each variable and put always as first if
                        clean = re.sub(r'(?<=\w|\.|\s)(\[\d+\]){,10}', "", value)
                        info_dict[key] = clean
                    else:
                        info_dict[key] = value
                else:
                    info_dict[key] = value

            elif key == "Country":

                if value != "NA":
                    if re.search(r'(?<=\w|\.|\s)(\[\d+\]){,10}', value): # Delet any reference (ex. [1]), We'll do for each variable and put always as first if
                        clean = re.sub(r'(?<=\w|\.|\s)(\[\d+\]){,10}', "", value)
                        info_dict[key] = clean

                        if re.search(r'(?<!\s|\-|\_|\/)(?=[A-Z])', clean):
                            split = re.split(r'(?<!\s|\-|\_|\/)(?=[A-Z])', clean) # Divide joint name (ex. Radish CamuJohn Snow)
                            info_dict[key] = ", ".join([i for i in split if i != ""]) # transform the split list a string (don't add empty stings)
                        else:
                            info_dict[key] = clean
                    else:
                        info_dict[key] = value
                else:
                    info_dict[key] = value

            elif key == "Language":

                if value != "NA":
                    if re.search(r'(?<=\w|\.|\s)(\[\d+\]){,10}', value): # Delet any reference (ex. [1]), We'll do for each variable and put always as first if
                        clean = re.sub(r'(?<=\w|\.|\s)(\[\d+\]){,10}', "", value)
                        info_dict[key] = clean

                        if re.search(r'(?<!\s|\-|\_|\/)(?=[A-Z])', clean):
                            split = re.split(r'(?<!\s|\-|\_|\/)(?=[A-Z])', clean) # Divide joint name (ex. Radish CamuJohn Snow)
                            info_dict[key] = ", ".join([i for i in split if i != ""]) # transform the split list a string (don't add empty stings)
                        else:
                            info_dict[key] = clean
                    else:
                        info_dict[key] = value
                else:
                    info_dict[key] = value

            elif key == "Budget":

                if value != "NA":
                    if re.search(r'(?<=\w|\.|\s)(\[\d+\]){,10}', value): # Delet any reference (ex. [1]), We'll do for each variable and put always as first if
                        clean = re.sub(r'(?<=\w|\.|\s)(\[\d+\]){,10}', "", value)
                        info_dict[key] = clean
                    else:
                        info_dict[key] = value
                else:
                    info_dict[key] = value

    return [intro, plot, info_dict]

def save_as_tsv():

    path = "/home/tiago/Scrivania/Libri Magistrale/1st semester/ADM/HomeWork3/PagineMovie1/" # Where the .html file have been saved
    save_in = "/home/tiago/Scrivania/Libri Magistrale/1st semester/ADM/HomeWork3/fileTsv_movie1/" # Where you want to save the .tsv file
    log_path = "/home/tiago/Scrivania/Libri Magistrale/1st semester/ADM/HomeWork3/LogFile.txt" # Where you want to save the log file
## se è un pat magari non è un file haahaha
    log = open(log_path, "w")# A log file:  In case the some error occur we can see at which point it ccured

    i = 0 # Change with 0 if you are working with all 30000 files or with the starting number of your file
    for file in sorted(os.listdir(path)):

        if file.startswith('article_'): # there is a hidden file whith another name, in this way we avoid to open it
            site = BeautifulSoup(open("".join([path, str(file)])), "html.parser") # Let's open each page

            log.write("".join([path, str(file)]) + "\n")

            try:
                with open("".join([save_in, "article_", str(i), ".tsv"]), "w") as file:
                    tsv_output = csv.writer(file, delimiter = '\t')
                    clean_el = clean_all(site) # Let's call the function that clean our data from "impurities"
                    intro_plot = [clean_el[0], clean_el[1]]
                    info_box = [info for _, info in clean_el[2].items()]
                    elements = [info_box[0]] + intro_plot + info_box[1:] # Add as first element the title
                    tsv_output.writerow(elements)

            except Exception: # Let's see what is went wrong and break the cycle
                log.close()
                with open(log_path, "r") as log:
                    lines = log.read().splitlines() # Read only the last line of the log (it contains the article with the error)
                    last_line = lines[-1]
                    print("The error is in: ", last_line, traceback.print_exc())
                break

            i += 1

    log.close()
    print("Finish!")

 

import requests, re, PyPDF2, io
from bs4 import BeautifulSoup
import pandas as pd
from nltk import sent_tokenize, word_tokenize
from parameters import features, revues, headers

def get_content(url):
    r = requests.get(url, timeout =10, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

def parse_erudit_site(revues):
    for revue in revues:
        r = requests.get(f"https://www.erudit.org/fr/revues/{revue}/#back-issues")
        soup = BeautifulSoup(r.content, 'html.parser')
        issues = soup.find_all("li", {"class":"issue-list__item"})
        for issue in issues:
            year = re.findall(r"(?:(?:18|19|20|21)[0-9]{2})", issue.text)
            if int(year[0])>2002:
                publication = issue.find("a")["href"]
                pub_soup = get_content(f"https://www.erudit.org{publication}") #transfer the url to a soup
                htmls = parse_erudit_volume(pub_soup)
                for html in htmls:
                    text_soup = get_content(f"https://www.erudit.org{html}")
                    try:
                        parse_erudit_text(text_soup)
                    except:
                        f"https://www.erudit.org{html} generated an exception"

def parse_erudit_volume(pub_soup):
    htmls = pub_soup.find_all("a", {"class":"tool-btn", "title":"Lire l'article en texte intégral"})
    htmls = [html["href"] for html in htmls]
    return htmls

def parse_erudit_text(text_soup):
    """
    soup, csv >>> new rows in the csv
    Parse a soup on Erudit and save it in the csv file
    """
    df = pd.read_csv("data_files//erudit.csv", index_col="Unnamed: 0", encoding="utf-8", dtype=features)

    #metadata
    title = text_soup.find("span", {"class":"titre"}).text
    if len(df[df["Title"]==title])>0:
        return print(f"""{title} is already in df""")
    print(f"{title} not in df: adding")
    author = text_soup.find("ul", {"class":"grauteur doc-head__authors"}).text
    infos = text_soup.find_all("div", {"class":"col-sm-6 doc-head__metadata"})[1]
    revue = infos.find("a").text
    try:
        annee = infos.find_all("span")[1].text[-4:]
    except:
        try:
            annee = re.findall(r"(?:(?:18|19|20|21)[0-9]{2})", infos.text)[0]
        except:
            annee = "0000"


    obj_meta = {
        "Title": title,
        "Author": author,
        "Journal": revue,
        "Year": annee
    }

    #text and sections
    try:    #sometimes there is no abstract
        resume = text_soup.find("section", {"id":"resume-fr"}).find("p").text
    except:
        resume = ""
    all_sections = text_soup.find("section", {"id":"corps"}).find_all("section")

    #sentences in resume
    for idx, sentence in enumerate(sent_tokenize(resume)):
        obj_dict = {
            "section_rank": 0,
            "par_rank": 0,
            "sent_rank": idx,
            "text": sentence
        }
        obj_dict.update(obj_meta)
        df = df.append(obj_dict, ignore_index=True)

    #sentences in sections
    for no, section in enumerate(all_sections):
        for par, paragraph in enumerate(section):
            for idx, sentence in enumerate(sent_tokenize(paragraph.text)):
                obj_dict = {
                    "section_rank": no,
                    "par_rank": par,
                    "sent_rank": idx,
                    "text": sentence
                }
                obj_dict.update(obj_meta)
                df = df.append(obj_dict, ignore_index=True)

    df.to_csv("data_files//erudit.csv")
    

def generate_nietzsche():
    #Function used to generate and save the entirety of "Thus spoke Zarathustra".
    url_Nietzsche = "https://www.gutenberg.org/files/1998/1998-h/1998-h.htm"
    soup = get_content(url_Nietzsche)
    text = soup.text
    tokenized = word_tokenize(text)
    textComplete = tokenized[6334:-21215]
    with open("nietzsche.txt", "w", encoding="utf-8") as f:
        f.write(" ".join(textComplete))

def generate_fr():
    get_content_PDF("http://www.philotextes.info/spip/IMG/pdf/zarathoustra.pdf", "nietzsche_fr")

def get_content(url):
    url = url
    res = requests.get(url)
    html_page = res.text

    # Parse the source code using BeautifulSoup
    soup = BeautifulSoup(html_page, 'html.parser')

    # Extract the plain text content
    text = soup.get_text()
    return text

def get_content_PDF(url, name):
    
    r = requests.get(url)
    f = io.BytesIO(r.content)
    pdfreader = PyPDF2.PdfFileReader(f)
    x=pdfreader.numPages
    fullText = ""
    for page in range(0, x-1):
        pageobj=pdfreader.getPage(page)
        text=pageobj.extractText()
        fullText += text

    file1=open(f"{name}.txt","w")
    file1.writelines(fullText)
    return text

def parse_aristotle():
    """Unused and unfinished functions. 
    """
    url_Aristotle = "http://classics.mit.edu/Browse/browse-Aristotle.html"
    content = get_content(url_Aristotle)
    links = content.find_all('a', attrs = {"href": True})
    book_links = [link for link in links if link['href'].startswith("/Aristotl")]
    all_texts = []
    for link in book_links:
        get_content(link)
        book = content.find_all('a', attrs = {"href": True})
        book_text = [link for link in book if link['href'].endswith(".txt")]
        content = get_content(book_text)
        all_texts.append(content)

    all_texts = " ".join(all_texts.text())
    with open("aristotle.txt", "w") as f:
        f.write(all_texts)

if __name__ == "__main__":  #Starts the script if opened directly
    parse_erudit_site(revues)
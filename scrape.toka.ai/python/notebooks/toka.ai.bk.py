
# coding: utf-8

# In[13]:

from bs4 import BeautifulSoup
import requests
import os


# In[62]:

src_url = "http://www.justice.gov.za/legislation/constitution/pdf.html"
req = requests.get(src_url)
html_doc = req.text
bs = BeautifulSoup(html_doc, "lxml")


# In[74]:

def download_from_link(downlink, dst_file):
    print("        - Downloading", downlink + "...")
    downfile = requests.get(downlink)
    with open(dst_file, 'wb') as dst:
        print("        - Please wait while writing", dst_file)
        dst.write(downfile.content) 


# In[66]:

doc_url = "http://www.justice.gov.za/legislation/constitution/"

for link in bs.find_all("a"):
    if "eng" in link.get("href"):
        doc = link.get("href")
        downlink = doc_url + doc
        dst_file = "../../corpus/za_consti/" + doc
        download_from_link(downlink, dst_file)


# In[87]:

def create_dir(directory):
    if not os.path.exists(directory):
        print("Creating directory: ", directory)
        os.makedirs(directory)


# In[89]:

cases_url = "http://www.saflii.org/za/cases/"
cases_dir = '../../corpus/cases/'
create_dir(cases_dir)
dirs = []

src_url = "http://www.saflii.org/content/south-africa-index"
req = requests.get(src_url)
html_doc = req.text
bs = BeautifulSoup(html_doc, "lxml")

for link in bs.find_all("a"):
    href = link.get("href")
    unwanted = "/za/cases/"
    if href.startswith(unwanted):
        directory = href.replace(unwanted, "")
        dirs.append(directory)

for directory in dirs[1:]:
    create_dir(cases_dir + directory.replace("/", ""))
    print(directory.replace("/","") + " cases:")
    
    src_url = cases_url + directory
    req = requests.get(src_url)
    html_doc = req.text
    bs = BeautifulSoup(html_doc, "lxml")
    
    for link in bs.find_all("a"):
        href = link.get("href")
        if href.endswith("/") and len(href) == 5:
            # Create year directory if it doesn't exist
            year = href.replace("/","")
            year_dir = cases_dir + directory + year + "/"
            create_dir(year_dir)
            year_url = cases_url + directory + year
            req = requests.get(year_url)
            html_doc = req.text
            bs = BeautifulSoup(html_doc, "lxml")
            print("* " + year_url)

            for link1 in bs.find_all("a"):
                href1 = link1.get("href")

                if href1.endswith('html') and href1.startswith("../"):
                    doc_link = cases_url + directory + href1.replace("../", "")
                    print("    + "+doc_link)
                    req = requests.get(doc_link)
                    html_doc = req.text
                    bs = BeautifulSoup(html_doc, "lxml")

                    for link2 in bs.find_all("a"):
                        href2 = link2.get("href")
                        if href2 is not None:
                            if href2.endswith("pdf") or href2.endswith("rtf"):
                                name = href2.replace("/za/cases/"+directory,"")
                                doc_url = cases_url + directory + name
                                #print("        - " + doc_url)
                                dest_file = year_dir + (directory+name).replace("/", "_")
                                download_from_link(doc_url, dest_file)


# In[ ]:




"""
This module fetch the PDF url links from the README file
download them, and store them in content folders
"""
 
import os, re, requests, codecs
import PyPDF2
from tika import parser
from tqdm import tqdm 
import math

__author__ = "Ioannis Katsikavelas"
__copyright__ = "2019"
__credits__ =[]
__version__ = "0.0.1"
__email__ = "ioankats93@gmail.com"

MYDIR = os.path.dirname(__file__)
directory = 'papers'
if not os.path.exists(directory):
    os.makedirs(directory)

papers = []
n = 0
with codecs.open('README.md', encoding="utf-8", errors='strict') as f:
    lines = f.read().split('\n')
    folder_heading, section_path = '', ''
    for line in lines:
        if('###' in line):
            folder_heading = line.strip().split('###')[1]
            win_restricted_chars = re.compile(r'[\^\/\\\:\*\?\"<>\|]')
            folder_heading = folder_heading.strip(" ")
            section_path = os.path.join(directory, folder_heading)
            if not os.path.exists(section_path):
               os.makedirs(section_path)
        if('[[pdf]]' in line):  
            url = line.strip('()').split('[[pdf]]')[1]
            url = url.strip('()')
            paper = win_restricted_chars.sub("", url)
            if (not os.path.exists(os.path.join(section_path, paper + '.pdf'))):
                print("Fetching...", paper)
                try:
                    response = requests.get(url, stream=True)

                    # Total size in bytes.
                    total_size = int(response.headers.get('content-length', 0));
                    block_size = 1024
                    wrote = 0 
                    with open(os.path.join(section_path, str(paper)).encode("utf-8"),'wb') as f:
                        for data in tqdm(response.iter_content(block_size), total=math.ceil(total_size//block_size) , unit='KB', unit_scale=True):
                            wrote = wrote + len(data)
                            f.write(data)
                        raw = parser.from_file(os.path.join(section_path, paper))
                        #Set title to PDF file
                        title = 0
                        while len((raw['content'].strip().split('\n'))[title]) < 30 :
                            title += 1
                        pdf_title = raw['content'].strip().split('\n')[title]
                        fetched_file = os.path.join(section_path, paper)
                        new_title_file = os.path.join(section_path, pdf_title)
                        print("Renaming file from : {} ==> {}".format(paper, pdf_title))
                        print("\n")
                        os.rename(fetched_file, new_title_file)
                        # f.write(response.content)
                except (requests.exceptions.ReadTimeout, requests.exceptions.RequestException) as e:
                    print("ERROR: {}".format(e)) 


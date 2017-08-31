#ARTICLE-GATHER-DOWNLOAD-ANALYZE
#Run from root directory
#todo -> Change txt output to MySQL database writes
from __future__ import print_function
import newspaper
import datetime
import os
import nltk

from newspaper import news_pool
from nltk.tokenize import RegexpTokenizer
from collections import Counter

#nltk.download('words')

def main():
    scrape(); #download articles from various news sites into corresponding text files
    analyze(); #analyze text files for word count

def scrape():
    current_folder = str(datetime.datetime.now())
    os.makedirs('application/COUNTS/'+current_folder)
    os.chdir('application/COUNTS/'+current_folder) #create directory for current time, and enter #CF: app/COUNTS/"current Folder"

    yahoo_paper = newspaper.build('http://news.yahoo.com',verbose=True,fetch_images=False)
    washpost_paper = newspaper.build('https://www.washingtonpost.com/',verbose=True,fetch_images=False)
    cnn_paper = newspaper.build('http://cnn.com',verbose=True,fetch_images=False)
    google_paper = newspaper.build('http://news.google.com',verbose=True,fetch_images=False)
    fox_paper = newspaper.build('http://foxnews.com',verbose=True,fetch_images=False)
    nytimes_paper = newspaper.build('http://nytimes.com',verbose=True,fetch_images=False)
    aol_paper = newspaper.build('http://news.aol.com',verbose=True,fetch_images=False)
    guardian_paper = newspaper.build('https://www.theguardian.com/us',verbose=True,fetch_images=False)
    drudge_paper = newspaper.build('http://drudgereport.com/',verbose=True,fetch_images=False)
    usatoday_paper = newspaper.build('http://usatoday.com',verbose=True,fetch_images=False)
    print("URLS COMPILED")

    papers = [yahoo_paper, washpost_paper,cnn_paper,google_paper,fox_paper,nytimes_paper,aol_paper,guardian_paper,drudge_paper,usatoday_paper]
    news_pool.set(papers, threads_per_source=2) # (3*2) = 6 threads total
    news_pool.join()
    print("ARTICLES DOWNLOADED")

    for paper in papers:
        for article in paper.articles:
            article.parse()
    print("ARTICLES PARSED")

    for paper in papers:
        for article in paper.articles:
            try:
                print(article.title, file=open(paper.brand+".txt", "a"))
            except:
                pass
    print("PAPERS SEPARATED")

    os.chdir('..')#CF: app/COUNTS/
    os.chdir('..')#CF: app/
    ##DATABASE WRITE CURRENT_FOLDER##                          *****
    print(current_folder, file=open("master_count.txt", "a"))
    ##
    os.chdir("COUNTS/"+current_folder)#CF: app/COUNTS/"current Folder"

def analyze():#CF: app/COUNTS/"current Folder"
    print("NOW ANALYZING")
    owd = os.getcwd();
    for filename in os.listdir('.'):
        os.chdir('..')#CF: app/COUNTS/
        os.chdir('..')#CF: app/
        ##DATABASE WRITE PAPER##                                *****
        print(filename, file=open("master_count.txt", "a"))
        ##
        os.chdir(owd)#CF: app/COUNTS/"current Folder"
        file = open(filename)
        wordCount(file)

def wordCount(file):#CF: app/COUNTS/"current Folder"
    owd = os.getcwd();
    toAnalyze = file.read();
    wordArray = filterCommon(toAnalyze)
    count = Counter(wordArray).most_common(10)
    os.chdir('..')#CF: app/COUNTS/
    os.chdir('..')#CF: app/
    for word in count:
        ##DATABASE WRITE WORD##                                 *****
        print(word, file=open("master_count.txt", "a"))
        ##
    os.chdir(owd)#CF: app/COUNTS/"current Folder"

def removeAll(x, l): #taken from a random stackoverflow post
    t = [y for y in l if y != x]
    del l[:]
    l.extend(t)
    return l

def filterCommon(string):
    tokenizer = RegexpTokenizer(r'[A-Za-z]+')
    nouns = tokenizer.tokenize(string) #remove non alpha-numeric
    string_nouns = ""
    for item in nouns:
        string_nouns+=item
        string_nouns+=" "
    text=' '.join(string_nouns.split()).lower()
    tokens = nltk.word_tokenize(text)
    tags = nltk.pos_tag(tokens)
    words = set(nltk.corpus.words.words())
    nouns = [word for word,pos in tags if (pos == 'NNP' or pos == 'NNPS' or pos =='NN' or pos == 'NNS' 
             and word.lower() in words or not word.isalpha())] #remove non-nouns, non-english
    for item in nouns: 
        if(len(item) < 3): #safety check for non alpha-numeric, non-nouns
            nouns = removeAll(item,nouns) 
    return nouns

if __name__ == '__main__':
    main() # this calls your main function

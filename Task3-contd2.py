# -*- coding: utf-8 -*-
"""
Created on Thu Apr 7 15:57:31 2022

@author: NWANDU KELECHUKWU
"""

import pywikibot
from bs4 import BeautifulSoup
import urllib.request
import re

#function to get the cordinal number of author strings p2093

def print_authorstring_info(list_item):
    
    site = pywikibot.Site("wikidata", "wikidata")
    repo = site.data_repository()
    
    o_list = []
    for data_item in list_item:
        item = pywikibot.ItemPage(repo, data_item) 
        item_dict = item.get()
    
        for claim in item_dict['claims']: # Loop through items
            if claim == 'P2093':
                
                for source in item.claims[claim]:
                        
                    stat = list(source.qualifiers.items())
                    
                    for key, value in stat:
                        num = value[0].getTarget()
                        o_list.append(num)
    return o_list
                    
print_authorstring_info(['Q56603084'])
#%%

#function to get the cordinal number of authors p50

def print_author_info(list_item):
    
    site = pywikibot.Site("wikidata", "wikidata")
    repo = site.data_repository()
    
    q = []
    for data_item in list_item:
        item = pywikibot.ItemPage(repo, data_item) 
        item_dict = item.get()
    
        for claim in item_dict['claims']: # Loop through items
            if claim == 'P50':
                for source in item.claims[claim]:
                    
                    tt = list(source.qualifiers.items())
                    for key, value in tt:
                        if key == 'P1545':
                            no1 = value[0].getTarget()
                            q.append(no1)
                                
                            
    return q

print_author_info(['Q56603084'])
#%%
#function to concatenate the list of cordinal number of authors and author strings 
def all_authors():
    
    f = print_author_info(['Q56603084'])
    j = print_authorstring_info(['Q56603084'])
    k = j + f
    return k
    
all_authors()
#%%

#function to get the author names present in the citation 

def citation(url):
    
    p = []
    with urllib.request.urlopen(url) as response:
        html = response.read()
        soup = BeautifulSoup(html, "html.parser")
        text3 = soup.findAll(attrs={'property' : re.compile('article:author')})
        for text in text3:
            tip = text['content']
            
            p.append(tip)
        
    return p
       
citation('https://ui.adsabs.harvard.edu/abs/2018ApJ...852...97H/exportcitation')
#%%

#function to firstly, use the cordinal number of all the authors to get their names in the citation

def match_citation_names():
    authorname_list = all_authors()
    
    b1 = citation('https://ui.adsabs.harvard.edu/abs/2018ApJ...852...97H/exportcitation')

    u1 = [b1[int(i) - 1] for i in authorname_list]

    return u1

match_citation_names()
#%%

#function to join the claims of authors and author strings which will be useful to add the qualifier

def join_names():
    
    
    site = pywikibot.Site("wikidata", "wikidata")
    repo = site.data_repository()
    item = pywikibot.ItemPage(repo, 'Q56603084') 
    item_dict = item.get()
    
    pli = []
    pli1 = []
    for claim in item_dict['claims']['P50']: # Loop through items
            pli.append(claim)
    #print(pli)
    #for ID in pli:
        #nue = pli.index(ID)   
        #authors_list = listt[nue]
        #print(ID)
    for t_claim in item_dict['claims']['P2093']: # Loop through items
            pli1.append(t_claim)
    #for ID1 in pli1:
        #nue1 = pli1.index(ID1) 
        #x1 = re.split(", ", authors_list)
        #pli1.append(x1)
            joined = pli + pli1
   
    return joined

join_names()
#%%

#function to split the names now got from the citation into family and given names 

def split():
    listt = match_citation_names()
    pli2 = []
    joined = join_names()
    for ID in joined:
        nue = joined.index(ID)
        authors_list = listt[nue]
        x1 = re.split(", ", authors_list)
        
        pli2.append(x1)
    print(pli2)
    
split()
#%%

#function to add the p9688 and p9687 qualifiers using the claims list and their respective index 

def add_qualifiernames(data_item):
    
    site = pywikibot.Site("wikidata", "wikidata")
    repo = site.data_repository()
    
    listt = match_citation_names()
    dateCre = split() 
    #print(listt)
    for te, tea in zip(listt, dateCre):
        
        if listt.index(te) == dateCre.index(tea):
        
            qualifier = pywikibot.Claim(repo, u'P9688')
            qualifier.setTarget(tea[0])
            te.addQualifier(qualifier, summary=u'Adding a qualifier.')
            print('New Qualifier for P9688!')
            
            
            qualifier = pywikibot.Claim(repo, u'P9687')
            qualifier.setTarget(tea[1])
            te.addQualifier(qualifier, summary=u'Adding a qualifier.')
            print('New Qualifier for P9687!')

add_qualifiernames('Q56603084')
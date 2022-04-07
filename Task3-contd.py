# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 23:21:20 2022

@author: NWANDU KELECHUKWU
"""

#this function overall gets the list of the authors in the wikidata item from the citation
import pywikibot
from bs4 import BeautifulSoup
import urllib.request
import re


def authorname_list():
    
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
                        
                        
    a = print_author_info(['Q56603084']) 
    
    
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
           
    b = citation('https://ui.adsabs.harvard.edu/abs/2018ApJ...852...97H/exportcitation')
    
    u = [b[int(i) - 1] for i in a]
    return u 
    
authorname_list()


#%%
#This gets the first and last name of the author from the citation list
def authorname_seperated():
    listt = authorname_list()
    
    site = pywikibot.Site("wikidata", "wikidata")
    repo = site.data_repository()
    item = pywikibot.ItemPage(repo, 'Q56603084') 
    item_dict = item.get()
    
    pli = []
    for claim in item_dict['claims']['P50']: # Loop through items
            t_claim = claim.getTarget().title()
            pli.append(t_claim)
    nue = pli.index('Q104918685')        
    x1 = re.split(", ", listt[nue])
    return x1
  
authorname_seperated() 


#%%

def author_qualifier():
    site = pywikibot.Site("wikidata", "wikidata")
    repo = site.data_repository()
    
    
    wkID = authorname_seperated()
    claim = pywikibot.Claim(repo, u'P50') 
    qualifier = pywikibot.Claim(repo, u'P9688')
    qualifier.setTarget(wkID[0])
    claim.addQualifier(qualifier, summary=u'Adding a qualifier.')
    print('New Qualifier!')

    claim = pywikibot.Claim(repo, u'P50') 
    qualifier1 = pywikibot.Claim(repo, u'P9687')
    qualifier1.setTarget(wkID[1])
    claim.addQualifier(qualifier1, summary=u'Adding a qualifier.')
    print('New Qualifier!!')
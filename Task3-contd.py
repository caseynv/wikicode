# -*- coding: utf-8 -*-
"""
Created on Sat Apr  9 07:17:03 2022

@author: NWANDU KELECHUKWU
"""

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


def authorname_seperated():
    listt = authorname_list()
    
    site = pywikibot.Site("wikidata", "wikidata")
    repo = site.data_repository()
    item = pywikibot.ItemPage(repo, 'Q56603084') 
    item_dict = item.get()
    
    pli = []
    pli1 = []
    for claim in item_dict['claims']['P50']: # Loop through items
            t_claim = claim.getTarget().title()
            pli.append(t_claim)
    #print(pli)
    for ID in pli:
        nue = pli.index(ID)   
        authors_list = listt[nue]
        #print(authors_list)
        x1 = re.split(", ", authors_list)
        pli1.append(x1)
    return pli1
    
    #print(x1)
    #return x1
  
authorname_seperated() 

#%%


def add_qualifier(data_item):
    site = pywikibot.Site("wikidata", "wikidata")
    repo = site.data_repository()
    item = pywikibot.ItemPage(repo, data_item) 
    item_dict = item.get()
    listt = []
    dateCre = authorname_seperated() 
    for claim in item_dict['claims']['P31']: # Loop through items
        
        listt.append(claim)
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

add_qualifier('Q56603084')
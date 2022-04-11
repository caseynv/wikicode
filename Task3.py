# -*- coding: utf-8 -*-

import pywikibot
from bs4 import BeautifulSoup
import urllib.request
import re
# Connect to enwiki
enwiki = pywikibot.Site('en', 'wikipedia')
# and then to wikidata
enwiki_repo = enwiki.data_repository()


#%%

def print_authorname(list_item):
    
    site = pywikibot.Site("wikidata", "wikidata")
    repo = site.data_repository()
    
    i_list = []
    for data_item in list_item:
        item = pywikibot.ItemPage(repo, data_item) 
        item_dict = item.get()
    
        for claim in item_dict['claims']: # Loop through items
            if claim == 'P50':
                for source in item.claims[claim]:
                    QID = source.target.getID()
                
                    item1 = pywikibot.ItemPage(repo, QID) 
                    item_dict1 = item1.get()
                    try:
                        item_new = item_dict1['claims']['P735']
                        for item1_new in item_new:
                            itemm = item1_new.target.getID()
                            QID1 = pywikibot.ItemPage(repo, itemm) 
                            name = QID1.get()
                            try:
                                item_new1 = item_dict1['claims']['P734']
                                for item1_new1 in item_new1:
                                    itemm1 = item1_new1.target.getID()
                                    QID2 = pywikibot.ItemPage(repo, itemm1) 
                                    name1 = QID2.get()
                                    m_list = name['labels']['en'] + ', ' + name1['labels']['en']
                                   
                                    i_list.append(m_list)
                            except:
                                print('No Family name')
                    except:
                        print('No Given name')
                    
                    
    return i_list
                    
print_authorname(['Q56603084'])

#%%
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
#This function extracts author names from bibtex 

def author_citation(url):
    list1 = []
    with urllib.request.urlopen(url) as response:
        html = response.read()
        soup = BeautifulSoup(html, "html.parser")
        text3 = soup.findAll(attrs={'property' : re.compile('article:author')})
        for text in text3:
            tip = text['content']
            list1.append(tip)
    return list1

author_citation('https://ui.adsabs.harvard.edu/abs/2018ApJ...852...97H/exportcitation')

#%%
#This function adds the statedin qualifier if not present


#def extract_names():
    #b = citation('https://ui.adsabs.harvard.edu/abs/2018ApJ...852...97H/exportcitation')
    
    #u = [b[int(i) - 1] for i in a]
    #return u 
#extract_names()
#%%
#This function matches the name sof the authors in the citation to their cordinal no

def author_match():
    stated = all_authors()
    authorname = author_citation('https://ui.adsabs.harvard.edu/abs/2018ApJ...852...97H/exportcitation')
    for r in stated:
        num_r = int(r)
        new_list = [authorname[int(i) - 1] for i in stated]
        return new_list
author_match()

#%%
#This function adds the author string name to a list


def print_authorstring(list_item):
    ti = []
    site = pywikibot.Site("wikidata", "wikidata")
    repo = site.data_repository()
    for data_item in list_item:
        item = pywikibot.ItemPage(repo, data_item) 
        item_dict = item.get()
    
        for claim in item_dict['claims']: # Loop through items
            if claim == 'P2093':
                try:
                    for source in item.claims[claim]:
                        QID = source.target
                        ti.append(QID)
                        
                except:
                    print('Name')
    return ti

print_authorstring(['Q56603084'])

#%%
#This function joins the authorstring name and the concatenated given and family name 

def joined():
    first = print_authorstring(['Q56603084'])
    second = print_authorname(['Q56603084'])
    k = first + second
    
    return k
joined()

#%%
#This function adds matches the names in the ikidata and citation 

def match_alt():
    left = author_match()
    right = joined()
    
    print('citation names' + ' - ' + 'wikidata names')
    print('\n')
    for left1, right1 in zip(left, right):
        if left.index(left1) == right.index(right1):
    
            print(left1 + ' - ' + right1 )
match_alt()

#%%
#This function adds seperates the author names in citation

def authorname_seperated():
    listt = author_match()
    
    site = pywikibot.Site("wikidata", "wikidata")
    repo = site.data_repository()
    item = pywikibot.ItemPage(repo, 'Q56603084') 
    item_dict = item.get()
    
    pli1 = []
    for ID in listt:
        x1 = re.split(", ", ID)
        pli1.append(x1)
    return pli1
  
authorname_seperated()

#%%
#This function adds the claims in P2093 and P50-useful to add qualifiers

def join_names():
    
    site = pywikibot.Site("wikidata", "wikidata")
    repo = site.data_repository()
    item = pywikibot.ItemPage(repo, 'Q56603084') 
    item_dict = item.get()
    
    pli = []
    pli1 = []
    for claim in item_dict['claims']['P50']: # Loop through items
            pli.append(claim)
            
    for t_claim in item_dict['claims']['P2093']: # Loop through items
            pli1.append(t_claim)
            
            joined = pli1 + pli
   
    return joined

join_names()

#%%
#This function adds the P9688 and P9687 qualifier if not present

def add_namesqualifier(data_item):
    site = pywikibot.Site("wikidata", "wikidata")
    repo = site.data_repository()
    item = pywikibot.ItemPage(repo, data_item) 
    item_dict = item.get()
    listb = join_names()
    dateCre = authorname_seperated()
    
    for te, tea in zip(listb, dateCre):
        
        if listb.index(te) == dateCre.index(tea):
            if 'P9688' not in te.qualifiers:
                qualifier = pywikibot.Claim(repo, u'P9688')
                qualifier.setTarget(tea[0])
                te.addQualifier(qualifier, summary=u'Adding a qualifier.')
                print('New Qualifier for P9688!')
            else:
                continue
            
            if 'P9687' not in te.qualifiers:
                qualifier = pywikibot.Claim(repo, u'P9687')
                qualifier.setTarget(tea[1])
                te.addQualifier(qualifier, summary=u'Adding a qualifier.')
                print('New Qualifier for P9687!')
            else:
                continue
            
add_namesqualifier('Q56603084')

#%%
#This function adds the statedin qualifier if not present

def add_statedqualifier(list_item):
    
    site = pywikibot.Site("wikidata", "wikidata")
    repo = site.data_repository()
    neu = print_author_info(['Q56603084'])
    names = author_citation('https://ui.adsabs.harvard.edu/abs/2018ApJ...852...97H/exportcitation')
    
    claim_list = []
    for data_item in list_item:
        item = pywikibot.ItemPage(repo, data_item) 
        item_dict = item.get()
    
        for claim in item_dict['claims']['P50']: # Loop through items
                claim_list.append(claim)
    
    teb = [names[int(i) - 1] for i in neu]
    
    for u, p in zip(teb, claim_list):
        
        if claim_list.index(p) == teb.index(u):
            
            if 'P1932' not in p.qualifiers:
                qualifier = pywikibot.Claim(repo, u'P1932')
                qualifier.setTarget(u)
                p.addQualifier(qualifier, summary=u'Adding a qualifier.')
                print('New Qualifier for P1932!')
            else:
                continue
    
add_statedqualifier(['Q56603084'])


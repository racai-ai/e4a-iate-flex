# -*- coding: utf-8 -*-

import codecs
from collections import defaultdict as dd


id_file='covid_terms_ro_withid.txt'
adn_file='covid_terms_ro-inflected-tagged.txt'
corpus_file='ENRICH4ALL - Q&A list.txt'#path to corpus file in txt format
#---------------------------------------------------------------------
f = codecs.open(id_file, "r",encoding='utf-8')
fl=f.readlines()
f.close()

id_list=dd(list)
id_map={}
for line in fl:
    
    itms=line.split(';')
    key=itms[0].strip()
    expr=itms[1].strip()
    id_list[key].append(expr)
    id_map[expr]=key

id_filter_list={}

for k,v in id_list.items():#keep only expressions with synonims
    if len(v)>1:
        id_filter_list[k]=v
        
        
    
#-----------------------------------------------------------------------
f = codecs.open(adn_file, "r",encoding='utf-8')
fl=f.readlines()
f.close()

adn_list=dd(dict)
i=0
base=''
buf_dict={}
for line in fl:
    if (line.strip()!=''):
        if " " in line:
            itms=line.split(' ')
        else:
            itms=[line.strip()]
        for token in itms:
            itm0=itms[0].split('/')
            if(len(itm0)>1):
                root=itm0[0]
                pos=itm0[1]
        
        clean_line=line.strip().replace("/"+pos,'')
        buf_dict[pos]=clean_line
        if base=='':
            base=clean_line
    else:
        adn_list[base]=buf_dict
        base=''
        buf_dict={}
        
#-----------------------------------------------------------------------
f = codecs.open(corpus_file, "r",encoding='utf-8')
fl=f.readlines()
f.close()   
i=1
cdict={}
buf_text=dd(list)
for line in fl:
    if line.strip()!='':
        
        if line.strip()[1]==':':
            cd=line.split(":")[0]
            txt=line.split(":")[1]
        else:
            cd='A'
            txt=line.strip()
            
        buf_text[cd].append(txt)
    else:
        if(len(buf_text)>0 ):
            cdict[i]=buf_text
            buf_text=dd(list)
            i+=1


#-----------------------------------------------------------------------
found=[]

for   root, vr in adn_list.items():
    for adn , expr in vr.items():        
            for ind , vind in cdict.items():
                try:
                    questions=vind['Q']
                except :
                    print(ind)
                else:
                    for q in questions:
                        if expr in q:
                            found.append((expr,adn,root,q,ind))
                            
#----------------------------------------------------------------------
rep_list=[]
for inst in found:
    expr=inst[0]
    adn=inst[1]
    root=inst[2]
    txt=inst[3]
    ind=inst[4]
    eid=id_map[root]
    exprs=id_filter_list[eid]
    elist=[]
    for e in exprs:
        if root!=e:
            try:
                ne=adn_list[e][adn]
            except:
                print(e,adn)
            else:
                rep_list.append((expr,ne,txt,ind))

#--------------------------------------------------------------------

for inst in rep_list:
    expr=inst[0]
    nexp=inst[1]
    txt=inst[2]
    ind=inst[3]
    nq=txt.replace(expr,nexp)
    cdict[ind]['Q'].append(nq)

ntxt=''
f=0
for i, t in cdict.items():
    for tp ,tvl in t.items():
        f=0
        for tv in tvl:
            if(tp=='A' and f>0):
                tpw=''
            else:
                tpw=tp
            ntxt=ntxt+tpw+": "+tv
            f+=1
    ntxt=ntxt+"\n"
    
f = codecs.open(corpus_file+".out", "w",encoding='utf-8') 
f.write(ntxt)     
f.close()    
            
        
    

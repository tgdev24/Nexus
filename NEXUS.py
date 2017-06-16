import re
import xml
from Bio import SeqIO
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
import sys
import argparse
from Bio import SeqIO
import re
import os
import untangle
from xml.dom import minidom
from bs4 import BeautifulSoup
from bioservices import UniProt

input_file = sys.argv[1]
output_file = sys.argv[2]
output = open(output_file,'w')
output.write('Protein_ID' + '\t' + 'Accession_ID'+ '\t' + 'Description' + "\t" + 'e-Value' + '\t' + 'UniProt_ID' + '\t' + 'Pfam_Results' + '\t' + 'Prosite_Results' + '\t'+ 'Comments' + '\n')
n = 0

list1=[]
with open(input_file,'r') as xml:
    count = 0
    wp = ""
    def1 = ""
    eval1 = ""
    for line in xml:
        hit_def = ""
        hit_acc = ""
        e_val = ""
        flag = "false"
        
        if "<Iteration_query-def>" in line:
            abo = line.split(":")[1][0:9]
            count = count + 1
            
        if "<Hit_id>" in line:
            if len(wp) < 1:
                wp = line.split("|")[3]
                count = count +1
        
        if "<Hit_def" in line:
            if len(def1) == 0:
                if "&gt;" in line:
                    def1 = line.split("&gt;")[0][11:]
                    count = count+1
                else:
                    def1 = line.split("</Hit")[0][11:]
                    count = count+1
             
        if "<Hsp_evalue>" in line:
            if len(eval1)==0:
                eval1 = line.split(">")[1].strip('</Hsp_evalue>')
                count = count+1

        if count == 4:
            list1.append([abo, wp, def1, eval1])
            count = 0
            wp = ""
            def1 = ""
            eval1 = ""
    
    #print(len(list1))
    #print(list1)
    uni_entries = []
    listPfam = []
    listProsite = []
#    listuno = []
#    list2 = []
#    list3 = []
    for i in list1:
        u = UniProt()
        d = u.search(i[1], limit=3)
        unilines = d.split("\n")
        #print(unilines,  "bitchHHHHHHHHHHHHHHHHHHHHHH")
        if len(unilines) > 1:
            uni_entry = unilines[1].split("\t")[0]
            uni_entries.append(uni_entry)
        else:
            uni_entries.append("NULL")
        #print("\t", i[0], i[1])
        #print(uni_entries)
    for i in uni_entries:
        if(i == "NULL"):
            listPfam.append("NULL")
            listProsite.append("NULL")
        else:
            with open("uniprot_out.txt", "w") as outfile:
                p = u.retrieve(i, "txt")
                #newone = open("wow.txt", "w")
                #print(p)
                outfile.write(p)
                #newone.write(p)
            with open("uniprot_out.txt", "r") as infile:
                listuno = []
                list2 = []
                list3 = []
                for j in infile.readlines():
                    listuno.append(j.strip())
                #print(listuno)
                for j in listuno:
                    if "Pfam;" in j:
                        list2.append(j)
                        #print(list2, "lISTT2222222222222222222")                        
                    if "PROSITE;" in j:
                        list3.append(j)
                        #print(list3, "LISTTTTTTTTTTTTTTTTTTT33333333333333")
                if(len(list2) > 0):
                    temp = ""
                    if(len(list2) > 1):
                        #print(list2, "WTFFFFFFFFFFF")
                        for nums, k in enumerate(list2):
                            if(nums == (len(list2)-1)):
                                temp = temp + k.split(";")[1].strip()
                            else:
                                temp = temp + k.split(";")[1].strip() + "&"
                    else:
                        temp = list2[0].split(';')[1]
                    listPfam.append(temp)
                else:
                    listPfam.append("NULL")
                if(len(list3) > 0):
                    temp = ""
                    if(len(list3) > 1):
                        #print(list3, "HUHHHHHHHHHHHH")
                        for nums, k in enumerate(list3):
                            if(nums == (len(list3)-1)):
                                temp = temp + k.split(";")[1].strip()
                            else:
                                temp = temp + k.split(";")[1].strip() + " & "
                    else:
                        temp = list3[0].split(';')[1]
                    listProsite.append(temp)
                else:
                    listProsite.append("NULL")
    for i in range(0, len(list1)):
        output.write(list1[i][0]+'\t'+ list1[i][1]+'\t'+list1[i][2]+ '\t' + list1[i][3] + '\t' + uni_entries[i] + "\t" + listPfam[i] + "\t" + listProsite[i] + "\n")

xml.close()
output.close()
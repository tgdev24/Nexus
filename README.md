# Nexus
A protein analysis tool that queries Uniprot database using blast accession ID's and retrieves comprehensive sequence, gene annotation data. 
Input: xml file containing BLASTP results
Output: TXt file to output Tabular data from Uniprot, BLAST, Pfam, PROSITE

Before running, make sure to do the following:
install python 3.6
pip install biopython
pip install xml.dom
pip install bs4
pip install bioservices

**To run:**
python NEXUS.py <input file> <output file>

**To run on sample data, use:**
python NEXUS.py <sample.xml> <kobe.txt>

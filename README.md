# Nexus
A protein analysis tool that queries Uniprot database using blast accession ID's and retrieves comprehensive sequence, gene annotation data. 
Input: xml file containing BLASTP results
Output: TXt file to output Tabular data from Uniprot, BLAST, Pfam, PROSITE

To run:
python NEXUS.py <input file> <output file>

To run on sample data, use:
python NEXUS.py <combined.xml> <KOBE.txt>

#!/usr/bin/env python
# coding: utf-8

# # Task 1: Coding the Central Dogma

# ## 1.1 Write a function that finds the complementary sequence of a given DNA sequence

# In[35]:


def dna_complementary(seq, direction='same'):
    
    #Initiate an empty variable
    a = ''

    # List of DNA nucleotides
    DNA_nucleotides = ['A', 'T', 'G', 'C']

    # Checking if user has inputted only the proper DNA nucleotides
    for i in seq:
        if i.upper() not in DNA_nucleotides:
            raise ValueError('Sequence is non-canonical')

    # Converting the input sequence to uppercase
    seq = seq.upper()
    
    #Calling for complementary sequences
    for j in seq:
        if j == 'A':
            a += 'T'
        elif j == 'T':
            a += 'A'
        elif j == 'C':
            a += 'G'
        else:
            a += 'C'
    
    #Considering the direction input as lowercase to avoid issues due to capitlaization
    direction = direction.lower()
    
    #Condition for printing the complementary or reverse complementary sequences
    if direction == 'same':
        return a
    elif direction == 'reverse':
        return a[::-1]
    else:
        raise ValueError("Invalid direction provided. Use only same or reverse.")


# In[36]:


dna_complementary(seq = 'atGcGcct', direction= 'same')


# ## 1.2 Write a function that finds the RNA sequence of a given DNA sequence

# In[37]:


def dna_rna(seq):
    
    #Initiate an empty variable
    b = ''
    
    # Nucleotides list
    Nucleotides = ['A', 'G', 'C', 'U', 'T']

    #Iterate through the provided sequence
    for i in seq:
        
        #Check for any other bases
        if i not in Nucleotides:
            raise ValueError('Sequence is non-canonical')
        
        #Converting to Uracil if met with a Thymine
        if i == 'T':
            b += 'U'
        
        #Or proceed adding the rest of the rest of the nucleotides
        else:
            b += i

    #Check for Thymine
    if 'T' in seq:
        return b
    
    #No Thymine indicates it mostly is a RNA sequence
    else:
        print('Input sequence is an RNA sequence')
        return b


# In[38]:


dna_rna(seq = 'UUUGTGAAAA')


# ## 1.3 Write a function that finds the amino acid sequence of a given RNA sequence

# In[39]:


def rna_aa(seq):
    
    # Dictionary for codons from RNA to amino acids
    rna_codon_table = {
        "UUU": "F", "UUC": "F", "UUA": "L", "UUG": "L", "CUU": "L", "CUC": "L", "CUA": "L", "CUG": "L",
        "AUU": "I", "AUC": "I", "AUA": "I", "AUG": "M", "GUU": "V", "GUC": "V", "GUA": "V", "GUG": "V",
        "UCU": "S", "UCC": "S", "UCA": "S", "UCG": "S", "CCU": "P", "CCC": "P", "CCA": "P", "CCG": "P",
        "ACU": "T", "ACC": "T", "ACA": "T", "ACG": "T", "GCU": "A", "GCC": "A", "GCA": "A", "GCG": "A",
        "UAU": "Y", "UAC": "Y", "CAU": "H", "CAC": "H", "CAA": "Q", "CAG": "Q", "AAU": "N", "AAC": "N",
        "AAA": "K", "AAG": "K", "GAU": "D", "GAC": "D", "GAA": "E", "GAG": "E", "UGU": "C", "UGC": "C", 
        "UGG": "W", "CGU": "R", "CGC": "R", "CGA": "R", "CGG": "R", "AGA": "R", "AGG": "R", "GGU": "G", 
        "GGC": "G", "GGA": "G", "GGG": "G", "UAA": "*", "UAG": "*", "UGA": "*", "AGU": "S", "AGC": "S"}

    #Empty variables
    amino_acid_sequence = ''
    codon = ''

    #Check for each entry in the sequence
    for i in seq:
        codon += i   #Append the codons

        # Check for the keys in dictionary if the codon length is 3 (Reading Frame)
        if len(codon) == 3:
            amino_acid = rna_codon_table[codon]
            amino_acid_sequence += amino_acid #Append the amino acids to a new variable
            codon = '' #Clear the variable to loop through

    return amino_acid_sequence


# In[40]:


rna_aa (seq = 'UGACGGGCGCGCC')


# ## 1.4 Tying it all together: Write a higher-order function that combines 1.1-1.3.

# In[41]:


def dna_aa(seq, direction = 'same'):
    comp_DNA = dna_complementary(seq, direction)
    RNA = dna_rna(comp_DNA)
    AA = rna_aa(RNA)
    return AA


# In[42]:


dna_aa('AAATTTGGGCCtccacctt', direction = 'reverse')


# ## 1.5 Protein annotator

# In[9]:


get_ipython().system('pip install minotaor')
get_ipython().system('pip install dna_features_viewer')


# In[43]:


import minotaor
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

# Replace the sequence with your own sequence
protein = Seq("MTTPRNSVNGTFPAEPMKGPIAMQSGPKPLFRRMSSLVGPTQSFFMRESKTLGAVQIMNGLFHIALGGLLMIPAGIYAPICVTVWYPLWGGIMYIISGSLLAATEKNSRKCLVKGKMIMNSLSLFAAISGMILSIMDILNIKISHFLKMESLNFIRAHTPYINIYNCEPANPSEKNSPSTQYCYSIQSLFLGILSVMLIFAFFQELVIAGIVENEWKRTCSRPKSNIVLLSAEEKKEQTIEIKEEVVGLTETSSQPKNEEDIEIIPIQEEEEEETETNFPEPPQDQESSPIENDSSP")
protein_record = SeqRecord(protein, id="P11836", annotations={"molecule_type": "protein"})

protein_record = minotaor.annotate_record(protein_record)  # search is case sensitive


# In[44]:


protein_record


# In[45]:


graphic_record = minotaor.MinotaorTranslator().translate_record(protein_record)
ax, _ = graphic_record.plot(figure_width=40, strand_in_label_threshold=8)
graphic_record.plot_sequence(ax)


# The protein I used is **CD20_HUMAN**. It is a B-lymphocyte-specific membrane protein that plays a role in the regulation of cellular calcium influx necessary for the development, differentiation, and activation of B-lymphocytes.
# 
# From the annotation observed here, I could see that there are 15 start codons and the sequence ends in a non-stop codon region. 
# I could see Exportin NES from length 136-150 and also a Polyglutamate tag from length 268-274.
# 
# Exportin NES is indicative of the Nuclear Export Signal (NES) recognized by an exportin protein. 
# NES is a short amino acid sequence motif within a protein that signals its export from the cell nucleus to the cytoplasm. This process is essential for regulating the localization of various proteins within a cell.
# 
# Polyglutamate tag, a stretch of consecutive glutamate (E) amino acid residues in the protein's primary structure serves various functional roles, including protein-protein interactions, subcellular targeting, and post-translational modifications.

# # Task 2: Wrapping it all together with raw data

# 2.1 Write a function that reads the fastq file and extracts all sequences that have a quality scores above Q10.

# In[7]:


def extract_seqs(fastq_file_path):

    # Initializing a dictionary
    id_sequence_dict = {}

    # Open the FASTQ file for reading
    with open(fastq_file_path, 'r') as fastq_file:
        
        #Initiate empty variables
        gene_id = ''
        sequence = ''
        quality_values = ''

        #Moving through every line in file and keeping a count of each line
        for line_num, line in enumerate(fastq_file):
            line = line.strip() #Removing any escape characters at the end

            # Splitting the entries into four lines
            if line_num % 4 == 0:
                
                # Line with the full Gene ID
                full_gene_id = line.strip()[1:]

                # Getting just the ID by splitting from space and starting index from 0
                gene_id = full_gene_id.split(' ', 1)[0]

            elif line_num % 4 == 1:
                
                # Line with the Sequence
                sequence = line
            
            elif line_num % 4 == 3:
                
                # Line with Quality Values
                quality_values = line.strip()

                # Check if quality values contain any of the specified characters
                if any(char in quality_values for char in ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*']):
                    # If any invalid characters are found, skip this entry
                    continue
                
                # If no invalid characters are found, add the entry to the dictionary
                else:
                    id_sequence_dict[gene_id] = sequence 
            
    return id_sequence_dict


# In[8]:


extract_seqs('sample10000.fastq')


# In[4]:


len(extract_seqs('sample10000.fastq'))


# In[49]:


id_sequence_dict = extract_seqs('sample10000.fastq')
for gene_id, sequence in id_sequence_dict.items():
    print("Gene ID:", gene_id)
    print("Sequence:", sequence)


# In[50]:


class Genome:
    """
    Read, store, and analyze the contents of a genome from a FASTA file
    """
    def __init__(self, filepath):
        self.filepath = filepath
        self.dna_seqs = None
        self.dna_complementary_seqs = None
        self.rna_seqs1 = None
        self.aa_seqs1 = None
    
    # UPDATE THE FOLLOWING FUNCTIONS TO POPULATE THE ABOVE PROPERTIES
    def extract_seqs(self):
        self.dna_seqs = extract_seqs(self.filepath) #Calling function to extract the sequences and the gene IDs
    
    def complementary_seqs(self):
        if self.dna_seqs is None:
            raise ValueError("No valid sequences found. Check if extract_seqs is called or empty.") # ValueError message for not calling/empty the extract_seqs
        
        #Empty dictionary
        complementary_dict = {}
        for gene_id, sequence in self.dna_seqs.items(): #Iterating through the dictionary created in the previous function
            complementary_sequence = dna_complementary(sequence) #Passing every sequence as an input for the complementary DNA function
            complementary_dict[gene_id] = complementary_sequence #Mapping the comp. sequence to the Gene ID
        self.dna_complementary_seqs = complementary_dict #Saving it in a new variable
        
    def rna_seqs(self):
        if self.dna_complementary_seqs is None:
            raise ValueError("No complementary DNA sequences found. Check if complementary_seqs is called or empty.") # ValueError message for not calling/empty the complementary_seqs

        rna_dict = {}
        for gene_id, sequence in self.dna_complementary_seqs.items():#Iterating through the dictionary created in the previous function
            rna_sequence = dna_rna(sequence) #Passing every complementary sequence as an input for the DNA-RNA function
            rna_dict[gene_id] = rna_sequence #Mapping the RNA sequence to the Gene ID
        self.rna_seqs1 = rna_dict #Saving it in a new variable

    def aa_seqs(self):
        if self.rna_seqs1 is None:
            raise ValueError("No valid sequences found. Check if rna_seqs is called or empty.") # ValueError message for not calling/empty the rna_seqs
        
        aa_dict = {}
        for gene_id, sequence in self.rna_seqs1.items(): #Iterating through the dictionary created in the previous function
            aa_sequence = rna_aa(sequence) #Passing every sequence as an input for the RNA to Amino acid function
            aa_dict[gene_id] = aa_sequence #Mapping the Amino acid to the Gene ID
        self.aa_seqs1 = aa_dict #Saving it in a new variable

    def annot_aa_plot(self, seqid):
        if self.aa_seqs1 is None:
            raise ValueError("No valid amino acid sequences found. Call aa_seqs first.") # ValueError message for not calling/empty the aa_seqs

        # Create a SeqRecord from the amino acid sequence
        aa_sequence = Seq(self.aa_seqs1[seqid])
        aa_record = SeqRecord(aa_sequence, id=seqid, annotations={"molecule_type": "protein"})

        # Annotate the record
        aa_record = minotaor.annotate_record(aa_record)

        # Translate the annotated record into Minotaor graphical representation
        graphic_record = minotaor.MinotaorTranslator().translate_record(aa_record)

        # Plot the graphic record
        ax, _ = graphic_record.plot(figure_width=30, strand_in_label_threshold=7)
        graphic_record.plot_sequence(ax)


# In[51]:


# Create an instance of the Genome class, providing the filepath to your FASTA file
genome = Genome('sample10000.fastq')

# Extracting DNA sequences from the FASTA file
genome.extract_seqs()

# Making complementary sequences
genome.complementary_seqs()

# RNA sequences for complementary sequences
genome.rna_seqs()

# Find amino acid sequences
genome.aa_seqs()

# Annotate and plot an amino acid sequence for a specific gene ID
seq_id_to_annotate = 'ERR016162.32158054'
genome.annot_aa_plot(seq_id_to_annotate)


from Bio import Entrez
from Bio import Medline
import pandas as pd
import re
import csv


def scrape_pubmed(search_term):

    #=======================================================================================================================
    Entrez.email = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX" #always tell NCBI who you are
    Entrez.api_key = "XXXXXXXXXXXXXXXXXXXXXXXXXXXx" #api_key to allow you get more queries


    # handle = Entrez.egquery(term="orchid")
    # record = Entrez.read(handle)
    # for row in record["eGQueryResult"]:
    #      if row["DbName"]=="pubmed":
    #          print(row["Count"]) #will get you the same number of records if you type the query in pubmed

    #=======================================================================================================================
    search_term = search_term
    handle = Entrez.esearch(db="pubmed",
                            term= search_term,
                            sort='relevance',
                            retmax=50000) #make retmax a huge number in order not to put a cap on queries

    record = Entrez.read(handle)
    handle.close()
    idlist = record["IdList"] #the list is arranged by most recent, if you checked the PMID at the bottom of articles
                                #you see it matches the idlist



    handle = Entrez.efetch(db="pubmed",
                           id=idlist,
                           rettype="medline",
                           retmode="text") #fetch the records of those ids

    records = Medline.parse(handle)

    records = list(records)

    #=======================================================================================================================
    #create empty lists to assign the fields to later
    titles = [] #notice the 's' in the name
    affiliations = []
    journals_titles = []
    first_authors = []
    first_authors_affs = []
    senior_authors = []
    emails = []
    abstracts = []
    dates_of_pub = []
    links = []
    pmids = []
    pubmed_links = []
    #=======================================================================================================================
    for record in records:

         title = record.get("TI", "wrong or absent field") #title
         print("title: {0}".format(title), "\n")
         titles.append(title)

         affiliation = record.get("AD", "wrong or absent field") #Affiliation
         print("affiliation: {0}".format(affiliation), "\n")
         affiliations.append(affiliation)

         journal_title = record.get("JT", "wrong or absent field") #Journal Title
         print("journal title: {0}".format(journal_title), "\n")
         journals_titles.append(journal_title)

         first_author = record.get("AU", "wrong or absent field")[0] #first author
         print("first author: {0}".format(first_author) , "\n")
         first_authors.append(first_author)

         affliations = record.get("AD", "wrong or absent field")
         first_author_aff = affliations.partition(".")[0] #first author affiliation
         print("first author affiliation: {0}".format(first_author_aff), "\n")
         first_authors_affs.append(first_author_aff)

         senior_author = record.get("AU", "wrong or absent field")[-1] #last author
         print("senior author: {0}".format(senior_author), "\n")
         senior_authors.append(senior_author)

         match = re.search(r'[\w\.-]+@[\w\.-]+', affliations)         #contact email "([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"

         if match is None:
             email = 'None'
             print ("contact email: contact email is not provided", "\n")
             emails.append('None')
         else:
             email = match.group(0)
             #get rid of the '.' that sometimes exists at the end of the email string
             if email[-1] == '.':
                 email = email[:-1]
                 emails.append(email)
             else:
                 emails.append(email)

             print("contact email: {0}".format(email), "\n") #contact email

         abstract = record.get("AB", "wrong or absent field") #abstract
         print("abstract: {0}".format(abstract), "\n")
         abstracts.append(abstract)

         date_of_pub = record.get("DP", "wrong or absent field") #date of publication
         print("date of publication: {0}".format(date_of_pub), "\n")
         dates_of_pub.append(date_of_pub)



         link = (record.get("AID", "wrong or absent fiels")[-1][0:-5]) #link
         #make sure the code actually return doi, sometimes it returns pii (publisher idenitfier)
         if link[0:3] == '10.':
             link = "doi.org/{0}".format(record.get("AID", "wrong or absent fiels")[-1][0:-5])
             print("DOI: {0}".format(link), "\n")
         else:
             link = "doi.org/{0}".format(record.get("AID", "wrong or absent fiels")[0][0:-5])
             print("DOI: {0}".format(link), "\n")
         links.append(link)


         pmid = record.get("PMID", "wrong or absent field")
         print("PMID: {0}".format(pmid), "\n")
         pmids.append(pmid)

         pubmed_link = "https://www.ncbi.nlm.nih.gov/pubmed/{0}".format(pmid) #pubmed link (pubmed/pmid)
         print("Pubmed link: {0}".format(pubmed_link))
         pubmed_links.append(pubmed_link)

         print("------------------------------------------------------------------------------------------------------", "\n")


    len_records = len(records) 
    #=======================================================================================================================
    print("Number of records: {0}".format(len_records))

    #=======================================================================================================================
    ##create a data frame out of the lists


    data=[titles,affiliations,journals_titles,first_authors,first_authors_affs,senior_authors,emails,abstracts,dates_of_pub,links,pmids,pubmed_links]

    df = pd.DataFrame(data)
    df = df.transpose()
    df.columns = ['Title',
                 'Affiliation',
                 'Journals_title',
                 'First_author',
                 'First_author_aff',
                 'Senior_author',
                 'Email',
                 'Abstract',
                 'Date_of_pub',
                 'DOI' ,
                 'PMID',
                 'Pubmed_link' ]
    return (df, len_records)




#search = "diffusion tensor imaging AND mice"
#df_mice = scrape_pubmed(search)

#search = "diffusion tensor imaging AND rats"
#df_rats = scrape_pubmed(search)

#search = "diffusion tensor imaging AND ferrets"
#df_ferrets = scrape_pubmed(search)

#search = "diffusion MRI AND mice"
#df_mri_mice = scrape_pubmed(search)

#search = "diffusion MRI AND rats"
#df_mri_rats = scrape_pubmed(search)

#search = "diffusion MRI AND ferrets"
#df_mri_ferrets = scrape_pubmed(search)

#df_concat = pd.concat([df_mice, df_rats, df_ferrets, df_mri_mice, df_mri_rats, df_mri_ferrets])

#df_concat = pd.concat([df_mice, df_rats, df_ferrets, df_mri_ferrets])

search = "Axonal Damage AND Alcohol Use Disorder"
df_aud1 = scrape_pubmed(search)

search = "Axonal Damage AND Alcohol Use Disorder AND MRI"
df_aud2 = scrape_pubmed(search)

search = "Axonal Damage AND Alcohol Addiction"
df_aud2 = scrape_pubmed(search)

search = "diffusion MRI AND Axonal Damage"
df_mri1 = scrape_pubmed(search)

search = "diffusion MRI AND Axonal Death"
df_mri2 = scrape_pubmed(search)



df_concat = pd.concat([df_aud1,df_aud2,df_aud3,df_mri1,df_mri2])
df_unique = df_concat.drop_duplicates()


df_unique.to_csv('/media/mk/Dropbox/Dropbox/articles_aud_unique.csv')
#     All data are stored under the mnemonic appearing in the Medline
#  24      file. These mnemonics have the following interpretations:
#  25
#  26      ========= ==============================
#  27      Mnemonic  Description
#  28      --------- ------------------------------
#  29      AB        Abstract
#  30      CI        Copyright Information
#  31      AD        Affiliation
#  32      IRAD      Investigator Affiliation
#  33      AID       Article Identifier
#  34      AU        Author
#  35      FAU       Full Author
#  36      CN        Corporate Author
#  37      DCOM      Date Completed
#  38      DA        Date Created
#  39      LR        Date Last Revised
#  40      DEP       Date of Electronic Publication
#  41      DP        Date of Publication
#  42      EDAT      Entrez Date
#  43      GS        Gene Symbol
#  44      GN        General Note
#  45      GR        Grant Number
#  46      IR        Investigator Name
#  47      FIR       Full Investigator Name
#  48      IS        ISSN
#  49      IP        Issue
#  50      TA        Journal Title Abbreviation
#  51      JT        Journal Title
#  52      LA        Language
#  53      LID       Location Identifier
#  54      MID       Manuscript Identifier
#  55      MHDA      MeSH Date
#  56      MH        MeSH Terms
#  57      JID       NLM Unique ID
#  58      RF        Number of References
#  59      OAB       Other Abstract
#  60      OCI       Other Copyright Information
#  61      OID       Other ID
#  62      OT        Other Term
#  63      OTO       Other Term Owner
#  64      OWN       Owner
#  65      PG        Pagination
#  66      PS        Personal Name as Subject
#  67      FPS       Full Personal Name as Subject
#  68      PL        Place of Publication
#  69      PHST      Publication History Status
#  70      PST       Publication Status
#  71      PT        Publication Type
#  72      PUBM      Publishing Model
#  73      PMC       PubMed Central Identifier
#  74      PMID      PubMed Unique Identifier
#  75      RN        Registry Number/EC Number
#  76      NM        Substance Name
#  77      SI        Secondary Source ID
#  78      SO        Source
#  79      SFM       Space Flight Mission
#  80      STAT      Status
#  81      SB        Subset
#  82      TI        Title
#  83      TT        Transliterated Title
#  84      VI        Volume
#  85      CON       Comment on
#  86      CIN       Comment in
#  87      EIN       Erratum in
#  88      EFR       Erratum for
#  89      CRI       Corrected and Republished in
#  90      CRF       Corrected and Republished from
#  91      PRIN      Partial retraction in
#  92      PROF      Partial retraction of
#  93      RPI       Republished in
#  94      RPF       Republished from
#  95      RIN       Retraction in
#  96      ROF       Retraction of
#  97      UIN       Update in
#  98      UOF       Update of
#  99      SPIN      Summary for patients in
# 100      ORI       Original report in
# 101      ========= ==============================
# 102
# 103      """

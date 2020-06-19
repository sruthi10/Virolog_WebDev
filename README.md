
# Genome Visualization


Visualization of Viral Proteome based on Mitochondrial Localization. 

Focuses on: 

1. Probability distribution of Viral Proteins as Mitochondrial Targeting Sequences and as Trans-membrane Protein 
2. Cleavage Sites distribution of Viral Proteins based on probability of being mitochondrial target sequence  
3. Comparison of viral protemoe against Human and Mouse Mitochondrial Proteins
4. Viral Orthologs to uncover new functional aspects of protein based on structural comparison.

Goal of the project is to provide interactive application for user to access data analysis of entire Viral Proteome based on orthologs to Human Proteins, Localization, ISG and various filters probability of being mitochondrial protein, number of cleavage sites, probability of being Trans-membrane protein to obtain complete list of viral protein information (including Accession ID, Protein Name, Probability of Mitochondrial signal, Virus Type). This would help researchers acquire viral proteins that mimic the host (human) mitochondrial localized proteins.

## Code Structure
<pre>
<strong>Virolog_WebDev</strong>  
|-- <strong>documentation</strong>  
    +-- ViralAnalysisWebAppArchitecture.jpg  
|-- <strong>filters</strong>  
    |-- <strong>isg</strong>  
        +-- files pertaining to isg filter  
    |-- <strong>mitofates</strong>  
        +-- files pertaining to mitofates filter  
    |-- <strong>tmhmm</strong>  
        +-- files pertaining to tmhmm filter  
    |-- <strong>word++</strong>  
        +-- files pertaining to word++ filter  
    |-- cleanCsvResults.py  
    |-- tmhmm_mitofates_viralResults.csv  
    |-- tmhmm_mitofates_viralShortResults.csv  
    +-- tmhmmMitofatesComparison.py  
|-- <strong>genedata</strong>  
    |-- <strong>csvdata</strong>  
        |-- gene_taxonomy.csv  
        |-- mitofates_viral1.csv  
        |-- mitofatesResults_Human.MitoCarta2.0.csv  
        +-- mitofatesResults_Mouse.MitoCarta2.0.csv  
    |-- <strong>data</strong>  
        |-- gene_identifiers.txt  
        |-- mitofatesResults_Human.MitoCarta2.0.xlsx  
        |-- mitofatesResults_Mouse.MitoCarta2.0.xlsx  
        |-- mitofatesResults_viral1.xlsx  
        +-- mitofatesResults_viral2.xlsx  
    |-- <strong>databasedumps</strong>  
        +-- viralanalysisdb2018.sql  
    |-- <strong>outputdata</strong>  
        |-- gene_taxonomy.csv  
        |-- mitofates_viral_cleaned.csv  
        |-- mitofates_viral1-cleaned2.csv  
        |-- mitofatesResults_Human.MitoCarta2.0-cleaned.csv  
        +-- mitofatesResults_Mouse.MitoCarta2.0-cleaned.csv  
    |-- cleavage_sites.py  
    |-- datacleaner.py  
    |-- presequence_probability.py  
    |-- protein_info.py  
    +-- virus_taxonomy.py  
|-- <strong>HeatMapGeneration</strong>  
    |-- example_heat_map.html  
    |-- geneExpressionData_test.csv  
    |-- geneExpressionData.csv  
    |-- heat_map.py  
    |-- README.md  
    +-- requirements.txt  
|-- <strong>static</strong>  
    |-- <strong>css</strong>  
        |-- dashboard.css  
	|-- index.css  
	+-- layout.css  
    |-- <strong>js</strong>  
        |-- datatables.min.js  
	+-- index.js  
|-- <strong>templates</strong>  
    |-- <strong>partials</strong>  
        |-- cleavagesites.html  
        |-- presequenceprobability.html  
        +-- viraltaxonomy.html  
    |-- dashboard.html  
    +-- layout.html  
|-- create-tables.sql  
|-- Human_Genome.sql  
|-- main.py  
|-- README.md  
+-- requirements.txt  
</pre>

## Deployment

It is assumed that this repo has been cloned locally and you are in the base directory for the cloned repo. Follow the steps at the following url : https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-16-04

1. Create a python virtual environment and activate it ([how?](http://www.pythonforbeginners.com/basics/how-to-use-python-virtualenv 'Detailed info how to create a virtualenv')).
2. Run the following the command after activating the virtualenv:
	```
	pip install -r requirements.txt
    ```
3. Start the application using
    ```
    python main.py
    ```

4. Go to http://localhost:5000 in your browser.

## Database
The app currently uses a mix of csv files and mysql database to store the data. It's in process of migrating from csv to mysql. The database is currently hosted on the same cloud server as that of the app.

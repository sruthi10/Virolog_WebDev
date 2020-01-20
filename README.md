
# Genome Visualization


Visualization of Viral Proteome based on Mitochondrial Localization. 

Focuses on: 

1. Probability distribution of Viral Proteins as Mitochondrial Targeting Sequences and as Trans-membrane Protein 
2. Cleavage Sites distribution of Viral Proteins based on probability of being mitochondrial target sequence  
3. Comparison of viral protemoe against Human and Mouse Mitochondrial Proteins
4. Viral Orthologs to uncover new functional aspects of protein based on structural comparison.

Goal of the project is to provide interactive application for user to access data analysis of entire Viral Proteome based on orthologs to Human Proteins, Localization, ISG and various filters probability of being mitochondrial protein, number of cleavage sites, probability of being Trans-membrane protein to obtain complete list of viral protein information (including Accession ID, Protein Name, Probability of Mitochondrial signal, Virus Type). This would help researchers acquire viral proteins that mimic the host (human) mitochondrial localized proteins.

## Code
Most of the python code is in the genedata module. Try to organize the new code accordingly. 

## Deployment

Follow the steps at the following url : https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-16-04

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

# Genome Visualization


Visualization of Viral Proteome based on Mitochondrial Localization: Code for Generating Heat Map of Gene Expression Data

Focuses on: 

1. Gene Expression data visualization of Viral Proteins for specific tissues

Goal of the overall project is to provide interactive application for user to access data analysis of entire Viral Proteome based on orthologs to Human Proteins, Localization, ISG and various filters probability of being mitochondrial protein, number of cleavage sites, probability of being Trans-membrane protein to obtain complete list of viral protein information (including Accession ID, Protein Name, Probability of Mitochondrial signal, Virus Type). This would help researchers acquire viral proteins that mimic the host (human) mitochondrial localized proteins.

## Code
The main code is located in heat_map.py. The heat map is generated on test data located in geneExpressionData_test.csv. An example webpage with a generated heat map is shown in example_heat_map.html.

## Run

Follow the steps below:

1. Create a python virtual environment and activate it ([how?](http://www.pythonforbeginners.com/basics/how-to-use-python-virtualenv 'Detailed info how to create a virtualenv')).
2. Run the following the command after activating the virtualenv:
	```
	pip install -r requirements.txt
    ```
3. Run the application using
    ```
    python heat_map.py
    ```

4. The generated heat map plot should automatically pop up.

## Database
The app currently uses csv files to store the data for gene expression data.
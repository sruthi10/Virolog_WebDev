"""
Flask App Server

This file creates a Flask app and registers different routes for the Flask web server. Running this file will start the web server.

The following classes and functions are available:
    * FloatConverter - class required to pass floats in a URL route
    * dashboard - renders view for home page dashboard
    * cleavageSitesView - renders view for cleavage site page
    * getCleavageSitesData - get ceavage site data with min P-value
    * presequenceProbabilityView - renders view for preseq prob page
    * getPresequenceProbabilityData - get preseq prob data given P-value range
    * virusTaxonomyView - renders view for viral tax page
    * getVirusTaxonomyData - get all viral tax data
    * getFilteredTaxonomyData - get viral tax data based on list
"""

from flask import Flask, render_template, jsonify, request
from genedata import cleavage_sites, presequence_probability, virus_taxonomy
from werkzeug.routing import FloatConverter as BaseFloatConverter
import sys # only need for printing to console

app = Flask(__name__)


class FloatConverter(BaseFloatConverter):
    """
    A class used to convert to float
    
    Attributes
    ----------
    regex : str
        a formatted regex string to represent a float
    """
    regex = r'-?\d+(\.\d+)?'

""" NOTE: must define this before routes are registered"""
app.url_map.converters['float'] = FloatConverter


@app.route('/')
def dashboard():
    """Renders view for home page dashboard

    Returns
    -------
    string
        a string representing the evaluated html dashboard template
    """
    return render_template('dashboard.html')


@app.route('/cleavagesites')
def cleavageSitesView():
    """Renders view for cleavage sites page

    Returns
    -------
    string
        a string representing the evaluated cleavage sites template
    """
    return render_template('partials/cleavagesites.html')

@app.route('/getcleavagesitesdata/<float:pvalue>')
def getCleavageSitesData(pvalue):
    """Fetches data to be displayed on the cleavage sites page
    
    Parameters
    ----------
    pvalue : float
        The min P-value for the data returned

    Returns
    -------
    flask.Response()
        an object with content-type header 'application/json' that contains cleavage site data
    """
    cleavage_mapping_virus = cleavage_sites.get_mapping(
        r'genedata/outputdata/mitofates_viral_cleaned.csv', pvalue)
    cleavage_mapping_human = cleavage_sites.get_mapping(
        r'genedata/outputdata/mitofatesResults_Human.MitoCarta2.0-cleaned.csv',
        pvalue)
    cleavage_mapping_mouse = cleavage_sites.get_mapping(
        r'genedata/outputdata/mitofatesResults_Mouse.MitoCarta2.0-cleaned.csv',
        pvalue)

    cleavage_labels_virus, cleavage_site_values_virus = \
        cleavage_sites.format_values(cleavage_mapping_virus)
    cleavage_labels_human, cleavage_site_values_human = \
        cleavage_sites.format_values(cleavage_mapping_human)
    cleavage_labels_mouse, cleavage_site_values_mouse = \
        cleavage_sites.format_values(cleavage_mapping_mouse)

    jsonData = {
        'cleavagemappinglabels': cleavage_labels_virus,
        'cleavagesitevaluesvirus': cleavage_site_values_virus,
        'cleavagesitevalueshuman': cleavage_site_values_human,
        'cleavagesitevaluesmouse': cleavage_site_values_mouse,
    }
    return jsonify(jsonData)


@app.route('/presequenceprobability')
def presequenceProbabilityView():
    """Renders view for presequence probability page

    Returns
    -------
    string
        a string representing the evaluated preseq prob template
    """
    return render_template('partials/presequenceprobability.html')

@app.route('/getPresequenceProbabilityData/<float:pvalueMin>/<float:pvalueMax>')
def getPresequenceProbabilityData(pvalueMin, pvalueMax):
    """Fetches data to be displayed on the preseq prob page
    
    Parameters
    ----------
    pvalueMin : float
        The min P-value for the data returned
    pvalueMax : float
        The max P-value for the data returned

    Returns
    -------
    flask.Response()
        an object with content-type header 'application/json' that contains preseq prob data
    """
    probability_mapping_virus = presequence_probability.get_mapping(
        r'genedata/outputdata/mitofates_viral_cleaned.csv')
    probability_mapping_virus_mapping_human = presequence_probability.get_mapping(
        r'genedata/outputdata/mitofatesResults_Human.MitoCarta2.0-cleaned.csv')
    probability_mapping_virus_mapping_mouse = presequence_probability.get_mapping(
        r'genedata/outputdata/mitofatesResults_Mouse.MitoCarta2.0-cleaned.csv')

    probability_labels_virus, probability_site_values_virus = \
        presequence_probability.format_values(probability_mapping_virus, pvalueMin, pvalueMax)
    probability_labels_human, probability_site_values_human = \
        presequence_probability.format_values(
            probability_mapping_virus_mapping_human, pvalueMin, pvalueMax)
    probability_labels_mouse, probability_site_values_mouse = \
        presequence_probability.format_values(
            probability_mapping_virus_mapping_mouse, pvalueMin, pvalueMax)

    jsonData = {
        'probabilitymappinglabels': probability_labels_human,
        'probabilityvaluesvirus': probability_site_values_virus,
        'probabilityvalueshuman': probability_site_values_human,
        'probabilityvaluesmouse': probability_site_values_mouse
    }
    return jsonify(jsonData)


@app.route('/virusTaxonomy')
def virusTaxonomyView():
    """Renders view for viral taxonomy page

    Returns
    -------
    string
        a string representing the evaluated html viral taxonomy template
    """
    return render_template('partials/viraltaxonomy.html')

@app.route('/getVirusTaxonomyData')
def getVirusTaxonomyData():
    """Fetches all the viral tax data to be displayed

    Returns
    -------
    flask.Response()
        an object with content-type header 'application/json' that contains viral tax labels and data
    """
    virus_taxonomy_distribution = virus_taxonomy.getTaxonomyDistribution()
    label, values = virus_taxonomy.format_taxonomy(virus_taxonomy_distribution)
    return jsonify({"labels": label, "data": values})

@app.route('/filteredTaxonomyData/<filteredList>')
def getFilteredTaxonomyData(filteredList):
    """Fetches all the viral tax data to be displayed
    
    Parameters
    ----------
    filteredList : list
        list of the labels to not include for the data/ visualizations

    Returns
    -------
    flask.Response()
        an object with content-type header 'application/json' that contains viral tax labels and data, not including the labels listed in filteredList
    """
    print(request.args, file=sys.stderr)
    return jsonify(virus_taxonomy.newGetTaxonomyData(request.args, filteredList))


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

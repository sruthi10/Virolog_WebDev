from flask import Flask, render_template, jsonify
from genedata import cleavage_sites, presequence_probability, virus_taxonomy

app = Flask(__name__)


@app.route('/getcleavagesitesdata/<float:pvalue>')
def getCleavageSitesData(pvalue):
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


@app.route('/getPresequenceProbabilityData/<float:pvalue>')
def getPresequenceProbabilityData(pvalue):
    probability_mapping_virus = presequence_probability.get_mapping(
        r'genedata/outputdata/mitofates_viral_cleaned.csv')
    probability_mapping_virus_mapping_human = presequence_probability.get_mapping(
        r'genedata/outputdata/mitofatesResults_Human.MitoCarta2.0-cleaned.csv')
    probability_mapping_virus_mapping_mouse = presequence_probability.get_mapping(
        r'genedata/outputdata/mitofatesResults_Mouse.MitoCarta2.0-cleaned.csv')

    probability_labels_virus, probability_site_values_virus = \
        presequence_probability.format_values(probability_mapping_virus, pvalue)
    probability_labels_human, probability_site_values_human = \
        presequence_probability.format_values(
            probability_mapping_virus_mapping_human, pvalue)
    probability_labels_mouse, probability_site_values_mouse = \
        presequence_probability.format_values(
            probability_mapping_virus_mapping_mouse, pvalue)

    jsonData = {
        'probabilitymappinglabels': probability_labels_human,
        'probabilityvaluesvirus': probability_site_values_virus,
        'probabilityvalueshuman': probability_site_values_human,
        'probabilityvaluesmouse': probability_site_values_mouse
    }
    return jsonify(jsonData)


@app.route('/cleavagesites')
def cleavageSitesView():
    return render_template('partials/cleavagesites.html')


@app.route('/presequenceprobability')
def presequenceProbabilityView():
    return render_template('partials/presequenceprobability.html')


@app.route('/getVirusTaxonomyData')
def getVirusTaxonomyData():
    virus_taxonomy_distribution = virus_taxonomy.getTaxonomyDistribution()
    label, values = virus_taxonomy.format_taxonomy(virus_taxonomy_distribution)
    return jsonify({"labels": label, "data": values})
	
@app.route('/getAllVirusTaxonomyData')
def getAllVirusTaxonomyData():
    return jsonify(virus_taxonomy.getTaxonomyData())


@app.route('/virusTaxonomy')
def virusTaxonomyView():
    return render_template('partials/viraltaxonomy.html')


@app.route('/')
def dashboard():
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

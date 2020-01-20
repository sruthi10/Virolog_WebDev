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



@app.route('/')
def cleavageSitesView():
    return render_template('partials/cleavagesites.html')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

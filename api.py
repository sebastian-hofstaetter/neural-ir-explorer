from flask import Flask, request, send_from_directory
import os
import argparse
from tqdm import tqdm
from flask import jsonify
import csv
import numpy
from bling_fire_tokenizer import BlingFireTokenizer

app = Flask(__name__, static_url_path='')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

#
# data loading & prep
#

paths={
    "collection":"C:\\Users\\sebas\\data\\msmarco\\collection\\collection-fixed.tsv",
    "queries":"C:\\Users\\sebas\\data\\wsdm20\\analysis\\clustering_queries.csv",
    "run-info":{"test_collection":"MSMARCO-Passage (Dev)",
                "model_info":"TK using 2 Transformer layers",
                "score_type":"kernel",
                "kernels_mus":[1.0, 0.9, 0.7, 0.5, 0.3, 0.1, -0.1, -0.3, -0.5, -0.7, -0.9],
                "cluster_info_text":"this is tk - hello world!"},
    "secondary-output":"C:\\Users\\sebas\\data\\\wsdm20\\secondary-end-top1000.npz",
    "cluster-stats":"C:\\Users\\sebas\\data\\\wsdm20\\analysis\\clustering_statistics.csv",
    "qrels":"C:\\Users\\sebas\\data\\msmarco\\qrels.dev.tsv"
}
max_doc_char_length = 100_000


with open(paths["cluster-stats"],"r") as csv_file:
    cluster_csv = csv.DictReader(csv_file)
    clusters = {}
    for row in cluster_csv:
        clusters[row["cluster"]] = dict(row)
        clusters[row["cluster"]]["queries"] = []



collection = {} # int id -> full line dictionary
with open(paths["collection"],"r",encoding="utf8") as collection_file:
    for line in tqdm(collection_file):
        ls = line.split("\t") # id<\t>text ....
        _id = ls[0]
        collection[_id] = ls[1].rstrip()[:max_doc_char_length]

with open(paths["queries"],"r") as csv_file:
    query_csv = csv.DictReader(csv_file)
    queries = {}
    queries_with_stats = {}
    for row in query_csv:
        clusters[row["cluster"]]["queries"].append(dict(row))
        queries[row["qid"]] = row["text"]
        queries_with_stats[row["qid"]] = dict(row)


secondary = numpy.load(paths["secondary-output"])
secondary_model = secondary.get("model_data")[()]
secondary_qd = secondary.get("qd_data")[()]

#
# api endpoints
#
@app.route('/dist/<path:path>')
def send_dist(path):
    return send_from_directory('dist', path)

@app.route("/")
def main():
    return send_from_directory('', 'index.html')

@app.route("/run-info")
def run_info():
    return jsonify(runs=paths["run-info"])

clusters_jsonified = None
@app.route("/evaluated-queries")
def all_queries():
    global clusters_jsonified
    if clusters_jsonified == None:
        clusters_jsonified = jsonify(clusters=clusters)
    return clusters_jsonified

@app.route("/query/<qid>")
def query(qid):

    documents = []

    for doc in secondary_qd[qid]:

        documents.append(get_document_info(qid,doc,secondary_qd[qid][doc]))

    return jsonify(documents=documents)

#
# helper methods
#
tokenizer = BlingFireTokenizer()

def analyze_weighted_param_1D(name,values, param_weight,bias=None,after_x=5):
    #print(name, ": value * weight + bias")
    rolling_sum = 0
    rolling_sum_after_x = 0

    kernels = {}

    for i,val in enumerate(values):
        param = param_weight[i]

        kernels[i] = (float(val),float(param))
        #print("["+str(i)+"]", str(val) + " * "+str(param) + " = "+ str(val*param))
        rolling_sum += val*param

        if i >= after_x:
            rolling_sum_after_x += val*param


    #if bias != None:
        #print("Sum:",rolling_sum + bias)
        #print("Sum(>="+str(after_x)+")",rolling_sum_after_x + bias)
    #else:
        #print("Sum:",rolling_sum)
        #print("Sum(>="+str(after_x)+")",rolling_sum_after_x)
    
    #print("-----------")
    if bias != None:
        rolling_sum = rolling_sum + bias
    return (kernels, float(rolling_sum))


def get_document_info(qid,did,secondary_info):

    document_info = {"id":float(did),"score":float(secondary_info["score"])}

    document_info["val_log"] = analyze_weighted_param_1D("log-kernels",secondary_info["per_kernel"],secondary_model["dense_weight"][0])
    document_info["val_len"] = analyze_weighted_param_1D("len-norm-kernels",secondary_info["per_kernel_mean"],secondary_model["dense_mean_weight"][0])

    document_info["tokenized_query"] = tokenizer.tokenize(queries[qid])
    document_info["tokenized_document"] = tokenizer.tokenize(collection[did])

    #matches = []
    matches_per_kernel = []
    matches_per_kernel_strongest = []

    original_mm = numpy.transpose(secondary_info["cosine_matrix_masked"][:len(document_info["tokenized_query"]),:len(document_info["tokenized_document"])]).astype('float64') 

    kernel_transformed = numpy.exp(- pow(numpy.expand_dims(original_mm,2) - numpy.array(paths["run-info"]["kernels_mus"]), 2) / (2 * pow(0.1, 2)))
    kernel_transformed_max_query_per_kernel = numpy.max(kernel_transformed,axis=1)

    #for t,token in enumerate(document_info["tokenized_document"]):
    #    #largest_sim = secondary_info["cosine_matrix_masked"][max_query_id_per_doc[t]][t]
#
    #    kernel_results = [0]*len(paths["run-info"]["kernels_mus"])
    #    #matches_per_doc = []
    #    for i,m in enumerate(paths["run-info"]["kernels_mus"]):
    #        for q in range(secondary_info["cosine_matrix_masked"].shape[0]):
    #            kernel_results[i] = float(max(kernel_results[i],(kernel_transformed[q][t][i])))
    #            #matches_per_doc.append(float(secondary_info["cosine_matrix_masked"][q][t]))
    #    
    #    #matches.append(matches_per_doc)
    #    matches_per_kernel.append(kernel_results)
    #    
    #    strongest_kernel = numpy.argmax(numpy.array(kernel_results),axis=0).tolist()
    #    matches_per_kernel_strongest.append(strongest_kernel)

    #print(secondary_info["cosine_matrix_masked"].dtype)
    #print(original_mm.dtype)
    #print(kernel_transformed.shape)
    #print(kernel_transformed.dtype)
    #print(original_mm)
    #print(numpy.around(original_mm,3).dtype)
    #print(numpy.around(original_mm,3).tolist())
    #print(numpy.around(kernel_transformed,3).dtype)
    document_info["matches"] = numpy.around(original_mm,3).tolist()
    document_info["matches_per_kernel"] = numpy.around(kernel_transformed,3).tolist()
    document_info["matches_per_kernel_max"] = numpy.around(kernel_transformed_max_query_per_kernel,3).tolist()


    #for q in range(len(document_info["tokenized_query"])):
    #    mq = []
    #    for d in range(len(document_info["tokenized_document"])):
    #        mq.append(float(secondary_info["cosine_matrix_masked"][q][d]))
    #    matches.append(mq)
    #document_info["matches"] = matches

    return document_info
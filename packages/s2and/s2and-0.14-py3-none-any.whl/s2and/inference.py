from os.path import join
import pickle
import pprint
from s2and.data import ANDData


def run(path_to_data, dataset_name="pubmed"):
    parent_dir = join(path_to_data, dataset_name)

    signatures = join(parent_dir, f"{dataset_name}_signatures.json")
    papers = join(parent_dir, f"{dataset_name}_papers.json")

    with open(join(path_to_data, production_model.pickle), "rb") as _pkl_file:
        clusterer = pickle.load(_pkl_file)['clusterer']

    anddata = ANDData(
        signatures=signatures,
        papers=papers,
        name="your_name_here",
        mode="inference",
        block_type="s2",
    )
    pred_clusters, pred_distance_matrices = clusterer.predict(anddata.get_blocks(), anddata)
    # print("CLUSTERS")
    # print("-"*80)
    # pprint.pprint(pred_clusters)
    # print("-"*80)
    # print("MATRICES")
    # print("-"*80)
    # pprint.pprint(pred_distance_matrices)
    # print("-"*80)
    return pred_clusters

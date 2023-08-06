
from qdls.gql.cypher.utils.kqa_eval import cypher_exec_eval
from argparse import Namespace

path = "/Users/qing/Downloads/sampled_50.json"

# config = Namespace(neo4j_uri="neo4j://172.23.148.83:28892", neo4j_user="neo4j", neo4j_passwd="kqa", timeout=10)
# cypher_exec_eval(path, key='cypher', nproc=1, config=config)


from qdls.gql.sparql.utils.kqa_eval import sparql_exec_acc, DataForSPARQL


# kqa_eval.db = kqa_eval.DataForSPARQL("/Users/qing/Downloads/kb.json")
# kqa_eval.virtuoso_address = "http://172.23.148.83:28890/sparql"
# kqa_eval.virtuoso_graph_uri = 'kqaspcy'

virtuoso_address = "http://172.23.148.83:28890/sparql"
virtuoso_graph_uri = 'kqaspcy'
config = Namespace(
    kb = DataForSPARQL("/Users/qing/Downloads/kb.json"),
    address = virtuoso_address,
    uri=virtuoso_graph_uri,
)


sparql_exec_acc(path, key='sparql', nproc=1, config=config)
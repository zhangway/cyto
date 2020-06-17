from flask import jsonify, render_template

from app import app
import csv

from app.Edge import Edge
from app.InitNode import InitNode
from app.Node import Node


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/cyto')
def cyto():
    with open("./globalNetwk.txt") as csv_file:
        next(csv_file)
        data = csv.reader(csv_file, delimiter='\t')
        nodes = []
        for row in data:
            nodes.append(InitNode(row[0], row[1], row[2]))
    fishes = list(map(lambda x: x.fish, nodes))
    app.logger.debug(f'original fish count:{len(fishes)}')
    unique_fishes = list(set(fishes))
    app.logger.debug(f'distinct fish count:{len(unique_fishes)}')
    flat_list = []
    for fish in unique_fishes:
        flat_list.append(list(set(list(filter(lambda node: node.fish == fish, nodes)))))
    edges = [item for sublist in flat_list for item in sublist]
    lice = list(map(lambda node: node.lice, nodes))
    unique_lice = list(set(lice))
    app.logger.debug(f'original lice count: {len(lice)}, distinct lice count:{len(unique_lice)}')
    max_bicor = max(map(lambda node: float(node.bicor), nodes))
    min_bicor = min(map(lambda node: float(node.bicor), nodes))
    app.logger.debug(f'max: {max_bicor}, min:{min_bicor}')
    cy_nodes = list(map(lambda s: Node(s, s), unique_fishes + unique_lice))
    app.logger.debug(f'nodes count: {len(cy_nodes)}')
    cy_edges = list(map(lambda edge: Edge(edge.fish + edge.lice, edge.fish, edge.lice, float(edge.bicor)), edges))
    app.logger.debug(f'edges count: {len(cy_edges)}')
    nodes_json = []
    edges_json = []
    for node in cy_nodes:
        app.logger.debug(f'{node.node_id}---{node.label}')
        nodes_json.append({"data": {"id": node.node_id, "label": node.label}})
    for edge in cy_edges:
        edges_json.append({"data": {"id": edge.id, "bicor": edge.bicor, "source": edge.source, "target": edge.target}})

    return jsonify(nodes=nodes_json, edges=edges_json)

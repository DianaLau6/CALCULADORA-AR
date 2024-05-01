class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.hijos = []

def convertir_arbol_a_vis(raiz):
    nodes = []
    edges = []

    def agregar_nodo(nodo, parent=None):
        nonlocal nodes, edges
        node_id = len(nodes) + 1
        nodes.append({'id': node_id, 'label': str(nodo.valor)})
        if parent is not None:
            edges.append({'from': parent, 'to': node_id})
        for hijo in nodo.hijos:
            agregar_nodo(hijo, parent=node_id)

    agregar_nodo(raiz)
    return {'nodes': nodes, 'edges': edges}

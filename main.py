__author__ = 'iashraf'
import sys
import networkx as nx
import matplotlib.pyplot as plt
import subprocess
try:
    print ("Python graph processing")
    import pygraphviz as pg
    from networkx.drawing.nx_agraph import write_dot
    print("using package pygraphviz")
except ImportError:
    try:
        import pydotplus
        from networkx.drawing.nx_pydot import write_dot
        print("using package pydotplus")
    except ImportError:
        print("Both pygraphviz and pydotplus were not found ")
        raise

def readDot(fin):
    dGraph = pg.AGraph(fin)
    # nxGraph = nx.Graph(dGraph)
    nxGraph = nx.DiGraph(dGraph)
    return nxGraph

def readGraph(fname):
    nxGraph = nx.DiGraph()
    fin = open(fname)
    for line in fin:
        if not line.isspace() and not line.startswith('#'):
            # print(line)
            fields = line.split()
            if fields[0] == "f":
                # print("Adding function node")
                nxGraph.add_node(fields[1], {'label': fields[2] }, type="function", name=fields[2], count=fields[3], calls=fields[4])
            elif fields[0] == "o":
                # print("Adding object node")
                nxGraph.add_node(fields[1], {'label': fields[2] }, type="object", name=fields[2], size=fields[3])
            elif fields[0] == "e":
                # print("Adding edge")
                nxGraph.add_edge(fields[1], fields[2], weight=fields[3])
            else:
                print("Incorrect input file")
    fin.close()

    return nxGraph

styles = {
    'graph': {
        'label': 'A Fancy Graph',
        'fontsize': '16',
        'fontcolor': 'white',
        'bgcolor': '#333333',
        'rankdir': 'TB',
    },
    'nodes': {
        'fontname': 'Helvetica',
        'shape': 'hexagon',
        'fontcolor': 'white',
        'color': 'white',
        'style': 'filled',
        'fillcolor': '#006699',
    },
    'functions': {
        'fontname': 'Helvetica',
        'shape': 'ovel',
        'fontcolor': 'white',
        'color': 'white',
        'style': 'filled',
        'fillcolor': '#006699',
    },
    'objects': {
        'fontname': 'Helvetica',
        'shape': 'square',
        'fontcolor': 'white',
        'color': 'white',
        'style': 'filled',
        'fillcolor': '#006699',
    },
    'edges': {
        'style': 'dashed',
        'color': 'white',
        'arrowhead': 'open',
        'fontname': 'Courier',
        'fontsize': '12',
        'fontcolor': 'white',
    }
}

def apply_styles(graph, styles):
    graph.graph_attr.update( ('graph' in styles and styles['graph']) or {} )
    graph.node_attr.update( ('functions' in styles and styles['functions']) or {} )
    graph.edge_attr.update( ('edges' in styles and styles['edges']) or {} )
    return graph

def writeDot(nxGraph):
    fout = "out.dot"
    agraph1 = nx.drawing.nx_agraph.to_agraph(nxGraph)
    agraph2 = apply_styles(agraph1, styles)
    # print( agraph2.string() )
    agraph2.write(fout)
    # write_dot(agraph2,fout) # to write nx graph
    # cmd = "dot -Tpdf %s -O" %fout
    cmd = "/data/repositories/mcprof/scripts/dot2pdf.sh %s" %fout
    ret = subprocess.check_output( cmd, shell=True)
    print("Written %s output dot file." % str(fout))

def filterEdges(nxGraph, thresh):
    for (u,v,d) in nxGraph.edges(data='weight'):
        if int(d) < thresh:
            print("removing edge")
            nxGraph.remove_edge(u,v)

def filterNodes(nxGraph, thresh):
    for n in nxGraph.nodes():
        if( nxGraph.node[n]['type'] == 'function' and int( nxGraph.node[n]['count']) < thresh):
            print("removing node")
            nxGraph.remove_node(n)

if __name__ == "__main__":
    total = len(sys.argv)
    cmdargs = str(sys.argv)
    try:
        # Pharsing args one by one
        scriptName = sys.argv[0]
        fin = sys.argv[1]

    except IndexError:
        fin = "testgraphs/test05.dat"
        print("Input file name not specified as input")
        print("    Usage: %s <somedotfile.dot>" % scriptName )
        # sys.exit(0)

    print ("Processing graph in %s file." % str(fin))

    ethresh = 10
    nthresh = 12000

    g = readGraph(fin)
    filterNodes(g, nthresh)
    filterEdges(g, ethresh)
    writeDot(g)

# def plot(nxGraph):
    # nx.draw(nxGraph)

    # pos=nx.spring_layout(nxGraph)
    # nx.draw_networkx_nodes(nxGraph, pos)
    # nx.draw_networkx_labels(nxGraph, pos)
    # nx.draw_networkx_edges(nxGraph, pos)
    # plt.show()

    # same layout using matplotlib with no labels
    # plt.title("draw_networkx")
    # pos=nx.graphviz_layout(G,prog='dot')
    # nx.draw(G,pos,with_labels=False,arrows=False)
    # plt.savefig('nx_test.png')

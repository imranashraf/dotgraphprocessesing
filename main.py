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

def writeDot(nxGraph):
    fout = "out.dot"
    write_dot(nxGraph,fout)
    cmd = "dot -Tpdf %s -O" %fout
    ret = subprocess.check_output( cmd, shell=True)
    print("Written %s output dot file." % str(fout))

if __name__ == "__main__":
    total = len(sys.argv)
    cmdargs = str(sys.argv)
    try:
        # Pharsing args one by one
        scriptName = sys.argv[0]
        fin = sys.argv[1]

    except IndexError:
        fin = "testgraphs/test03.dot"
        print("Dot file name not specified as input")
        print("    Usage: %s <somedotfile.dot>" % scriptName )
        # sys.exit(0)

    print ("Processing %s dot file." % str(fin))

    g = readDot(fin)
    writeDot(g)

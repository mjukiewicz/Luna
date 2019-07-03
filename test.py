from anytree import Node, RenderTree, Walker
import itertools

def find_all_parents(target,family):
    if not target.parent==None:
        family.append(target.parent)
        find_all_parents(target.parent,family)
    return family

def extract_trees(tree):
    leaf_and_nodes_list=set([node.parent.children for pre, fill, node in RenderTree(tree) if node.children==()])
    leaf_list=[[j for j in i if j.children==()] for i in leaf_and_nodes_list]
    tree_ends_combinations=list(itertools.product(*leaf_list))

    for i in tree_ends_combinations:
        branch=[]
        for j in i: branch.extend(find_all_parents(j,[j]))

        for pre, fill, node in RenderTree(tree):
            if node in branch:
                if len(pre)==0:
                    print("%s" % (node.name))
                else:
                    print("%s%s" % (len(pre[:-4])*" "+"└── ", node.name))

a = Node("a  ")
b = Node("b  ", parent=a)
c = Node("c  ", parent=a)

d = Node("d 1 ", parent=c)
e = Node("e 1 ", parent=c)
f = Node("f 1 ", parent=c)

g = Node("g 2 ", parent=e)
h = Node("h 2 ", parent=e)
i = Node("i 2 ", parent=e)

extract_trees(a)

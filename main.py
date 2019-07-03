from sekwenty import formulaConvertion
from cut import cutRule
from negation import prepare_formula
from anytree import Node, RenderTree
import itertools

base1=["B,A.B,D→G", "D→A,A.B,G", "D→B,A.B,G", "B,A.B,D→G", "B,D→A.B,G", "A,D→A.B,G", "A,D→B,G",
      "A.B,D→A,G", "D→A,A.B,G", "A.B,D→A,G", "A,A.B,D→G", "A.B,D→B,G", "A,B,D→A.B,G",
      "A,B,D→A.B,G", "B,A.B,D→A,G", "A,A.B,D→B,G", "D→A,B,A.B,G", "A,A.B,D→B,G"]
base2=["A,B,D→G", "B,D→A.B,G", "A,D→A.B,G", "A,A.B,D→G", "B,D→A,G", "A,D→B,G", "D→B,A.B,G",
      "A.B,D→B,G", "B,D→A,G", "D→A,B,G", "A,B,D→G", "D→A,B,G", "A,A.B,D→B,G",
      "B,A.B,D→A,G", "D→A,B,A.B,G", "D→A,B,A.B,G", "A,B,D→A.B,G", "B,A.B,D→A,G"]

sek_test=["p->p=p","->p=p,p", "~p->p=p", "->p=p,~p", "p=q->p=r,(p=r)=(q=r)",
          "p=q,p=r->(q=r)=(p=r)", "p=q->~(p=r),(q=r)=(p=r)",
          "p=q,~(p=r)->(q=r)=(p=r)", "p->~(p^p)", "->~(p^p),p", "~p->~(p^p)",
          "->~(p^p),~p", "~(p^q)->p,~((q^r)^(p^r))",'p,p=p->p']


def arrow_to_arrow(formula):
    return formula.replace("->","→")

def cut_formula(formula):
    regula=cutRule(formula)
    return regula.insert_new_elements() #co to za glupie nazwy?!

def check_axiom(formula):
    for i in range(len(formula)):
        if formula[i]=="→":
            seq_position=i
    subformula1=formula[:seq_position].split(",")
    subformula2=formula[seq_position+1:].split(",")
    if any(x in subformula1 for x in subformula2):
        return True
    else:
        return False

def check_linearity(formula):
    results=[]
    for i in range(len(base1)):
        one_rule_covertion=formulaConvertion(formula,base2[i],base1[i])
        obtained_formula=one_rule_covertion.convert_conditions()
        results.append(obtained_formula)

    flated_results=["" if i==[] else i[0] for i in results]
    results_indx=[]
    results=[]
    for i in range(len(flated_results)):
        if not flated_results[i]=="":
            results.append(flated_results[i])
            results_indx.append(i)

    return results, results_indx

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

def create_tree(parent):
    scheme=parent.name[:-4]
    if check_axiom(scheme): return 0
    set_of_new_schemes,indx=check_linearity(scheme)
    print("Zbior uzyskany z liniowych",set_of_new_schemes)
    if not set_of_new_schemes == []:
        for i in range(len(set_of_new_schemes)):
            create_tree(Node(set_of_new_schemes[i]+" "+format(indx[i], '02d')+" ", parent=parent))
        return 0
    if check_axiom(scheme): return 0
    scheme=prepare_formula(scheme)
    if check_axiom(scheme): return 0
    set_of_new_schemes=cut_formula(scheme)
    print("Zbior uzyskany z ciecia",set_of_new_schemes)
    for i in set_of_new_schemes:
        parent.children=[]
        create_tree(Node(i[0]+" "+"CUT", parent=parent))
        create_tree(Node(i[1]+" "+"CUT", parent=parent))


base_scheme=Node(arrow_to_arrow('p,p=p->p'+" "*4))
if not check_axiom(base_scheme.name[:-4]):
    create_tree(base_scheme)
    extract_trees(base_scheme)

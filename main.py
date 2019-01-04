from sekwenty import formulaConvertion

base1=["B,A.B,D→G", "D→A,A.B,G", "D→B,A.B,G", "B,A.B,D→G", "B,D→A.B,G", "A,D→A.B,G", "A,D→B,G",
      "A.B,D→A,G", "D→A,A.B,G", "A.B,D→A,G", "A,A.B,D→G", "A.B,D→B,G", "A,B,D→A.B,G",
      "A,B,D→A.B,G", "B,A.B,D→A,G", "A,A.B,D→B,G", "D→A,B,A.B,G", "A,A.B,D→B,G"]
base2=["A,B,D→G", "B,D→A.B,G", "A,D→A.B,G", "A,A.B,D→G", "B,D→A,G", "A,D→B,G", "D→B,A.B,G",
      "A.B,D→B,G", "B,D→A,G", "D→A,B,G", "A,B,D→G", "D→A,B,G", "A,A.B,D→B,G",
      "B,A.B,D→A,G", "D→A,B,A.B,G", "D→A,B,A.B,G", "A,B,D→A.B,G", "B,A.B,D→A,G"]

sekwenty=["p->p=p","->p=p,p", "~p->p=p", "->p=p,~p", "p=q->p=r,(p=r)=(q=r)",
          "p=q,p=r->(q=r)=(p=r)", "p=q->~(p=r),(q=r)=(p=r)",
          "p=q,~(p=r)->(q=r)=(p=r)", "p->~(p^p)", "->~(p^p),p", "~p->~(p^p)",
          "->~(p^p),~p", "~(p^q)->p,~((q^r)^(p^r))",'p,p=p->p']

def arrow_to_arrow(formula):
    return formula.replace("->","→")

def check_seqent_position(formula):
    for i in range(len(formula)):
        if formula[i]=="→":
            return i

def prepare_formula(formula):
    formula=arrow_to_arrow(formula)
    center=check_seqent_position(formula)
    subformula1=formula[:center]
    subformula2=formula[center+1:]
    subformula1,subformula2=remove_negations(subformula1,subformula2)
    subformula2,subformula1=remove_negations(subformula2,subformula1)
    return subformula1+"→"+subformula2

def remove_negations(subformula1, subformula2):
    subformula_list1=[]
    subformula_list2=[]
    if not len(subformula1)==0:
        subformula_list1=subformula1.split(",")
    if not len(subformula2)==0:
        subformula_list2=subformula2.split(",")

    subformula_list1,subformula_list2=transfer_between_lists(subformula_list1,subformula_list2)
    subformula_list2,subformula_list1=transfer_between_lists(subformula_list2,subformula_list1)

    subformula_list1.sort(key=len)
    subformula_list2.sort(key=len)
    return ','.join(subformula_list1), ','.join(subformula_list2)

def transfer_between_lists(subformula1,subformula2):
    for i in subformula1[:]:
        if i[0]=="~" and len(i)>3:
            subformula2.append(i[2:-1])
            subformula1.remove(i)
        elif i[0]=="~":
            subformula2.append(i[1:])
            subformula1.remove(i)
    return subformula1, subformula2

for j in sekwenty:
    sekwent=prepare_formula(j)
    results=[]
    for i in range(len(base1)):
        one_rule_covertion=formulaConvertion(sekwent,base1[i],base2[i])
        results.extend(one_rule_covertion.convert_conditions())

    print(set(results), len(set(results)))

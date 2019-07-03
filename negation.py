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

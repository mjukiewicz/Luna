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

conj=["="]

def convert(sequent, input, output):
    input_letter_list=prepare_set_of_elements(input)
    output_letter_list=prepare_set_of_elements(output)
    sequent_letter_list=prepare_set_of_elements(sequent)
    #if "A.B" in input_letter_list:
    for i in range(len(sequent_letter_list)):
        if any(x in sequent_letter_list[i] for x in conj):
            dic=[]
            dic.append(["A.B", sequent_letter_list[i]])
            center=int((len(sequent_letter_list[i])-1)/2)
            dic.append(["A", sequent_letter_list[i][:center]]) #uruchomić to tyle razy ile wystepuje
            dic.append(["B", sequent_letter_list[i][center+1:]])
            for k in [x for x in range(len(sequent_letter_list)) if sequent_letter_list[x]==sequent_letter_list[i][:center]]:
                temp=sequent_letter_list[:]
                temp[i]="A.B"
                temp[k]="A"
                niewiem(dic, sequent, input, output, temp)

            dic=[]
            dic.append(["A.B", sequent_letter_list[i]])
            center=int((len(sequent_letter_list[i])-1)/2)
            dic.append(["A", sequent_letter_list[i][:center]]) #uruchomić to tyle razy ile wystepuje
            dic.append(["B", sequent_letter_list[i][center+1:]])
            for k in [x for x in range(len(sequent_letter_list)) if sequent_letter_list[x]==sequent_letter_list[i][center+1:]]:
                temp=sequent_letter_list[:]
                temp[i]="A.B"
                temp[k]="B"
                niewiem(dic, sequent, input, output,temp)

            dic=[]
            dic.append(["A.B", sequent_letter_list[i]])
            center=int((len(sequent_letter_list[i])-1)/2)
            dic.append(["A", sequent_letter_list[i][:center]])
            dic.append(["B", sequent_letter_list[i][center+1:]])
            for k in [x for x in range(len(sequent_letter_list)) if sequent_letter_list[x]==sequent_letter_list[i][:center]]:
                for l in [x for x in range(len(sequent_letter_list)) if sequent_letter_list[x]==sequent_letter_list[i][center+1:]]:
                    temp=sequent_letter_list[:]
                    temp[i]="A.B"
                    temp[k]="A"
                    temp[l]="B"
                    niewiem(dic, sequent, input, output,temp)
        for j in range(len(sequent_letter_list)):
            if not i==j and not sequent_letter_list[i]=="→" and not sequent_letter_list[j]=="→":
                dic=[]
                temp=sequent_letter_list[:]
                dic.append(["A", sequent_letter_list[i]])
                dic.append(["B", sequent_letter_list[j]])
                dic.append(["A.B", sequent_letter_list[i]+"="+sequent_letter_list[j]]) #poprawic znak r
                temp[i]="A"
                temp[j]="B"
                niewiem(dic, sequent, input, output, temp)

    else:
        for i in range(len(sequent_letter_list)):
            for j in range(len(sequent_letter_list)):
                if not i==j and not sequent_letter_list[i]=="→" and not sequent_letter_list[j]=="→":
                    dic=[]
                    temp=sequent_letter_list[:]
                    dic.append(["A", sequent_letter_list[i]])
                    dic.append(["B", sequent_letter_list[j]])
                    dic.append(["A.B", sequent_letter_list[i]+"="+sequent_letter_list[j]]) #poprawic znak r
                    temp[i]="A"
                    temp[j]="B"
                    niewiem(dic, sequent, input, output, temp)

def niewiem(dic, sequent, input, output, temp):
    output_letter_list=prepare_set_of_elements(output)
    temp,D,G=extract_D_and_G(temp)
    temp, dic = add_D_and_G(temp, D, G, dic)
    if ",".join(temp).replace(",→,","→")==input:
        results.append(translate_formula(sequent,dic, output_letter_list))
        print(input, translate_formula(sequent,dic, output_letter_list))

def create_dic(formula, formula2=""):
    base=["A","B","A.B","→"]
    if formula2=="":
        center=int((len(formula)-1)/2)
        seq=[formula[:center], formula[center+1:], formula,"→"]
    else:
        seq=[formula, formula2, formula+"="+formula2,"→"] #zrobic cos z kropka
    dic= [[base[i],seq[i]] for i in range(len(base))]
    return dic

def first_translation(dic, formula):
    for i in range(len(formula)):
        for j in range(len(dic)):
            if formula[i]==dic[j][1]:
                formula[i]=dic[j][0]
                del dic[j]
                break
    return formula

def add_D_and_G(input_formula,D,G, dic):
    dic.append(D)
    dic.append(G)
    input_formula.insert(input_formula.index("→"),"D")
    input_formula.insert(len(input_formula),"G")
    return input_formula, dic

def translate_formula(formula, dic, output_letter_list):
    output=output_letter_list[:]
    for i in range(len(output)):
        for j in range(len(dic)):
            if not output[i] == "→" and output[i]==dic[j][0]:
                output[i]=dic[j][1]
    output=remove_comas(output) #czy to potrzebne?
    return ",".join(output).replace(",→,","→").replace("→,","→")

def extract_D_and_G(input_formula):
    seq_sign=input_formula.index("→")
    D, G=[],[]
    no_allowed_list=["A", "B", "A.B", "→"]
    output_formula=input_formula[:]
    for i in range(len(input_formula)):
        if not input_formula[i] in no_allowed_list:
            if i<seq_sign:
                D.append(input_formula[i])
            elif i>seq_sign:
                G.append(input_formula[i])
            output_formula.remove(input_formula[i])
    return remove_comas(output_formula),["D","".join(D)],["G","".join(G)]

def remove_comas(formula_with_comas):
    for i in formula_with_comas[:]:
        if i=="":
            formula_with_comas.remove(i)
    return formula_with_comas

def prepare_set_of_elements(formula):
    return formula.replace("→",",→,").split(",")

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
    #print(subformula1,subformula2)
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

sekwent=prepare_formula(sekwenty[-1])
results=[]
for i in range(len(base1)):
    print(i)
    convert(sekwent,base1[i],base2[i])

print(set(results))

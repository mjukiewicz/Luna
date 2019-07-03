sek_test=["p→p=p","→p=p,p", "~p→p=p", "→p=p,~p", "p=q→p=r,(p=r)=(q=r)",
          "p=q,p=r→(q=r)=(p=r)", "p=q→~(p=r),(q=r)=(p=r)",
          "p=q,~(p=r)→(q=r)=(p=r)", "p→~(p^p)", "→~(p^p),p", "~p→~(p^p)",
          "→~(p^p),~p", "~(p^q)→p,~((q^r)^(p^r))",'p,p=p→p']

conj_list=["=", "^"]

class cutRule():

    def __init__(self, formula):
        self.formula=formula

    def extract_letters(self):
        return [x for x in self.formula if x.isalpha()]

    def extract_elements(self): #prawdopodbnie do wyrzucenia
        formula_without_seq=self.formula.replace("→",",")
        if formula_without_seq[0]==",":
            return list(formula_without_seq[1:].split(","))
        elif formula_without_seq[-1]==",":
            return list(formula_without_seq[:-1].split(","))
        else:
            return list(formula_without_seq.split(","))

    def extract_assemblings(self):
        formula_without_seq=self.formula.replace("→",",")
        elements_of_formula=formula_without_seq.split(",")
        assemblings=[i for i in elements_of_formula if len(i)>2]
        self.lista=[]
        self.extract_subformulas(assemblings)
        return self.lista

    def extract_subformulas(self, assemblings):
        for assembling in assemblings:
            for j in range(len(assembling)):
                if assembling[:j].count("(")-assembling[:j].count(")")==0 and \
                assembling[j:].count("(")-assembling[j:].count(")")==0 and \
                assembling[j] in conj_list:
                    if  not assembling[j+1:]=="":
                        subform1=self.remove_brackets(assembling[j+1:])
                        self.lista.append(subform1)
                        self.extract_subformulas(subform1)
                    if  not assembling[:j]=="":
                        subform2=self.remove_brackets(assembling[:j])
                        self.lista.append(subform2)
                        self.extract_subformulas(subform2)

    def remove_brackets(self, formula):
        if formula[0]=="(" and formula[-1]==")":
            return formula[1:-1]
        else:
            return formula

    def insert_new_elements(self):
        not_allowed_list=[i for i in set(self.extract_elements()) if len(i)>1] ###???
        elements_list=list(set(self.extract_letters()+self.extract_assemblings()))
        new_elements=elements_list
        #new_elements=[i for i in elements_list if not i in not_allowed_list]
        #for i in new_elements[:]:
        #    if len(i)>3:
        #        new_elements.append("~("+i+")")
        #    else:
        #        new_elements.append("~"+i)
        results=[]
        for x in new_elements:
            if self.formula[0]=="→":
                results.append([self.formula+","+x, x+self.formula])
            elif self.formula[-1]=="→":
                results.append([self.formula+x, x+","+self.formula])
            else:
                results.append([self.formula+","+x, x+","+self.formula])
        return results #zeby wrocic do poprzedniej wersji usunac 0

'''
for i in sek_test:
regula=cutRule(sek_test[0])
print(regula.insert_new_elements())
'''

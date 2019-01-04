conj=["=","^"]

class formulaConvertion():

    def __init__(self,sequent, input, output):
        self.sequent=sequent
        self.input=input
        self.output=output
        self.sequent_list=self.prepare_set_of_elements(sequent)
        self.results=[]

    def convert_conditions(self):
        for i in range(len(self.sequent_list)):
            center=int((len(self.sequent_list[i])-1)/2)
            if any(x in self.sequent_list[i] for x in conj):
                dic=self.create_dic(self.sequent_list[i],self.sequent_list[i][:center],self.sequent_list[i][center+1:])
                for k in [x for x in range(len(self.sequent_list)) if self.sequent_list[x]==self.sequent_list[i][:center]]:
                    temp=self.create_temp_formula(self.sequent_list[:],counterA=k,counterAB=i)
                    temp=self.extract_and_add_noise(dic,temp)
                    self.check_result(dic,temp)

                dic=self.create_dic(self.sequent_list[i],self.sequent_list[i][:center],self.sequent_list[i][center+1:])
                for k in [x for x in range(len(self.sequent_list)) if self.sequent_list[x]==self.sequent_list[i][center+1:]]:
                    temp=self.create_temp_formula(self.sequent_list[:],counterB=k,counterAB=i)
                    temp=self.extract_and_add_noise(dic,temp)
                    self.check_result(dic,temp)

                dic=self.create_dic(self.sequent_list[i],self.sequent_list[i][:center],self.sequent_list[i][center+1:])
                for k in [x for x in range(len(self.sequent_list)) if self.sequent_list[x]==self.sequent_list[i][:center]]:
                    for l in [x for x in range(len(self.sequent_list)) if self.sequent_list[x]==self.sequent_list[i][center+1:]]:
                        temp=self.create_temp_formula(self.sequent_list[:],counterA=k,counterB=l,counterAB=i)
                        temp=self.extract_and_add_noise(dic,temp)
                        self.check_result(dic,temp)

            for j in range(len(self.sequent_list)):
                if not i==j and not self.sequent_list[i]=="→" and not self.sequent_list[j]=="→":
                    dic=self.create_dic(self.sequent_list[i]+"="+self.sequent_list[j],self.sequent_list[i],self.sequent_list[j]) #poprawic znak r
                    temp=self.create_temp_formula(self.sequent_list[:],counterA=i,counterB=j)
                    temp=self.extract_and_add_noise(dic,temp)
                    self.check_result(dic,temp)
        else:
            for i in range(len(self.sequent_list)):
                for j in range(len(self.sequent_list)):
                    if not i==j and not self.sequent_list[i]=="→" and not self.sequent_list[j]=="→":
                        dic=self.create_dic(self.sequent_list[i]+"="+self.sequent_list[j],self.sequent_list[i],self.sequent_list[j]) #poprawic znak r
                        temp=self.create_temp_formula(self.sequent_list[:],counterA=i,counterB=j)
                        temp=self.extract_and_add_noise(dic,temp)
                        self.check_result(dic,temp)
        return self.results

    def extract_and_add_noise(self,dic, temp):
        temp,D,G=self.extract_D_and_G(temp)
        temp, dic = self.add_D_and_G(temp, D, G, dic)
        return temp

    def check_result(self,dic,temp):
        output_list=self.prepare_set_of_elements(self.output)
        if ",".join(temp).replace(",→,","→")==self.input:
            self.results.append(self.translate_formula(self.sequent,dic, output_list))

    def create_temp_formula(self,formula,counterA="",counterB="",counterAB=""):
        if not counterA=="":
            formula[counterA]="A"
        if not counterB=="":
            formula[counterB]="B"
        if not counterAB=="":
            formula[counterAB]="A.B"
        return formula

    def create_dic(self,AB,A,B):
        dic=[]
        dic.append(["A.B", AB])
        dic.append(["A", A])
        dic.append(["B", B])
        return dic

    def add_D_and_G(self,input_formula,D,G, dic):
        dic.append(D)
        dic.append(G)
        input_formula.insert(input_formula.index("→"),"D")
        input_formula.insert(len(input_formula),"G")
        return input_formula, dic

    def translate_formula(self,formula, dic, output_list):
        output=output_list[:]
        for i in range(len(output)):
            for j in range(len(dic)):
                if not output[i] == "→" and output[i]==dic[j][0]:
                    output[i]=dic[j][1]
        output=self.remove_comas(output) #czy to potrzebne?
        return ",".join(output).replace(",→,","→").replace("→,","→")

    def extract_D_and_G(self,input_formula):
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
        return self.remove_comas(output_formula),["D","".join(D)],["G","".join(G)]

    def remove_comas(self,formula_with_comas):
        for i in formula_with_comas[:]:
            if i=="":
                formula_with_comas.remove(i)
        return formula_with_comas

    def prepare_set_of_elements(self,formula):
        return formula.replace("→",",→,").split(",")

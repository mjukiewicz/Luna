conj=["=","^"]

class formulaConvertion():
    def __init__(self,sequent, input, output):
        self.sequent=sequent
        self.input=input
        self.output=output
        self.seq_list=self.prepare_set_of_elements(sequent)
        self.results=[]

    def convert_conditions(self):
        for i in range(len(self.seq_list)):
            center=int((len(self.seq_list[i])-1)/2)
            if any(x in self.seq_list[i] for x in conj):
                self.condition1(center,i,self.seq_list[i][:center])
                self.condition1(center,i,self.seq_list[i][center+1:])
                self.condition2(center,i)
            for j in range(len(self.seq_list)):
                if not i==j and not self.seq_list[i]=="→" and not self.seq_list[j]=="→":
                    conjunction=[i for i in conj for j in self.sequent if i==j][0]
                    self.condition3(center,i,j, conjunction)
        return self.results

    def condition1(self, center,i, check):
        dic=self.create_dic(self.seq_list[i], self.seq_list[i][:center], self.seq_list[i][center+1:])
        for k in [x for x in range(len(self.seq_list))
            if self.seq_list[x]==check]:
                self.condition_processing(dic,k,"",i)

    def condition2(self, center, i):
        dic=self.create_dic(self.seq_list[i],self.seq_list[i][:center],self.seq_list[i][center+1:])
        for k in [x for x in range(len(self.seq_list))
                  if self.seq_list[x]==self.seq_list[i][:center]]:
            for l in [x for x in range(len(self.seq_list))
                      if self.seq_list[x]==self.seq_list[i][center+1:]]:
                self.condition_processing(dic,k,l,i)

    def condition3(self, center, i, j, conjunction):
        dic=self.create_dic(self.seq_list[i]+conjunction+self.seq_list[j], self.seq_list[i],self.seq_list[j])
        if not dic[0][1][0]=="="and not dic[0][1][-1]=="=":
            self.condition_processing(dic,i,j,"")

    def condition_processing(self,dic,countA,countB, countAB):
        temp=self.create_temp_formula(self.seq_list[:],countA,countB, countAB)
        temp=self.extract_and_add_noise(dic,temp)
        self.check_result(dic,temp)

    def extract_and_add_noise(self,dic, temp):
        temp,D,G=self.extract_D_and_G(temp)
        temp, dic = self.add_D_and_G(temp, D, G, dic)
        return temp

    def check_result(self,dic,temp):
        output_list=self.prepare_set_of_elements(self.output)
        if ",".join(temp).replace(",→,","→")==self.input:
            translated_formula=self.translate_formula(self.sequent,dic, output_list)
            self.results.append(translated_formula)

    def create_temp_formula(self,formula,counterA="",counterB="",counterAB=""):
        if not counterA=="": formula[counterA]="A"
        if not counterB=="": formula[counterB]="B"
        if not counterAB=="": formula[counterAB]="A.B"
        return formula

    def create_dic(self,AB,A,B):
        return [["A.B", AB], ["A", A], ["B", B]]

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
        return ",".join(output).replace(",→,","→").replace("→,","→").replace(",→","→")

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
        return [i for i in formula_with_comas[:] if not i==""]

    def prepare_set_of_elements(self,formula):
        return formula.replace("→",",→,").split(",")

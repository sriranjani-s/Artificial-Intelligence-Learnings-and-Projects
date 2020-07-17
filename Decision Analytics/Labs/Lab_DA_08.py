import itertools

class BoolVariable():
    def __init__(self,name):
        self.name_ = name
        self.domain_ = [True,True]

    def RemoveFromDomain(self,v):
        if v:
            self.domain_[1]=False
        else:
            self.domain_[0]=False            
    
    def GetName(self):
        return self.name_
    
    def IsInList(self, list):
        for l in list:
            if self.name_ == l.name_:
                return True
        return False
    
    def GetValues(self):
        values = []
        if self.domain_[0]:
            values.append(False)
        if self.domain_[1]:
            values.append(True)
        return values
    

class Constraint():
    def __init__(self, positive, negative):
        self.scheme_ = []
        for p in positive:
            self.scheme_.append(p)
        for n in negative:
            self.scheme_.append(n)
        self.combinations_ = self.GetAllCombinations_((positive,negative))
#        self.Print()

    def GetAllCombinations_(self,c):        
        scheme = []
        for p in c[0]:
            scheme.append(p)
        for n in c[1]:
            scheme.append(n)
        result = []
        for length in range(len(scheme)+1):
            for subset in itertools.combinations(scheme,length):
                valid = False
                for x in scheme:
                    if x.IsInList(subset):
                        if x.IsInList(c[0]):
                            valid = True
                            break
                    else: 
                        if x.IsInList(c[1]):
                            valid = True
                            break
                if valid:
                    result.append(subset)
        return result

    def CheckConstraint(self, x,v):
        result = False            
        for t in self.combinations_:                                
            is_valid = True
            for s in self.scheme_:
                values = s.GetValues()
                if len(values)==1:
                    if not ((values[0] and s.IsInList(t)) or ((not values[0]) and (not s.IsInList(t)))):
                        is_valid = False
            if is_valid:
                if (v and (x.IsInList(t)) or ((not v) and (not x.IsInList(t)))):                                        
                    result = True
                    break
        return result        

    def Print(self):
        for t in self.combinations_:
            for x in self.scheme_:
                if (x.IsInList(t)):
                    print(x.name_, end=",")
                else:
                    print("not",x.name_, end=",")
            print()
        print()

        

class Model():
    def __init__(self):
        self.variables_ = []
        self.constraints_ = []
        
    def AddBoolVariable(self, name):
        v = BoolVariable(name)
        self.variables_.append(v)
        return v
        
    def AddOrConstraint(self, positive, negative):
        c = Constraint(positive,negative)
        self.constraints_.append(c)

    def PrintDomains(self):
        for x in self.variables_:
            print(x.GetName(), x.GetValues())
        print()
        
    def PropagatorIteration(self):
        while True:
            change = False
            for c in self.constraints_:
                for x in c.scheme_:
                    for v in x.GetValues():
                        if not c.CheckConstraint(x,v):
                            x.RemoveFromDomain(v)
                            change = True
            if not change:
                break

def main():
    model = Model()
    
    v1 = model.AddBoolVariable("v1")
    v2 = model.AddBoolVariable("v2")
    v3 = model.AddBoolVariable("v3")
    v4 = model.AddBoolVariable("v4")
    
    model.AddOrConstraint([v1,v2],[])
    model.AddOrConstraint([],[v2])
    model.AddOrConstraint([v3],[v1])
    model.AddOrConstraint([v4],[v2])
    
    model.PrintDomains()
    model.PropagatorIteration()    
    model.PrintDomains()
    
main()


class Distribution:
    
    def __init__(self,mu=0,sigma=1):
        
        self.mean = mu
        self.stdev = sigma
        self.data =[]
    def read_data(self,filename):
        data_list=[]
        with open(filename,'r') as f:
            
            for line in f:
                data_list.append(float(line))
        self.data = data_list

            
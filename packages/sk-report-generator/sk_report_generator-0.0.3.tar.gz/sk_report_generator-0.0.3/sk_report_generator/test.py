class MatrixSolver:

    def __init__(self,obj,methods):
        self.obj = obj
        self.methods = methods
    def print_object(self):
        print(self.obj,self.methods)

matrix = MatrixSolver('[1,2,3,4,5]','get_max()')
matrix.print_object()
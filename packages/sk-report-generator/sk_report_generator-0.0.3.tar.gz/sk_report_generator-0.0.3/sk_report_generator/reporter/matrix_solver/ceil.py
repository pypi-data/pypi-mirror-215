from ...base import IMethod
import regex
import math
class Ceil:
    def __init__(self):
        pass

    def evaluate(self,obj_name,obj_value,obj_method_name,obj_method_arguments):

        if obj_method_name == 'ceil':
            if len(self.obj_method_arguments) == 0:
                obj_value = math.ceil(obj_value)

        return self.succesor.evaluate(obj_name,obj_value,obj_method_name,obj_method_arguments)


    def set_succesor(self,successor):
        self.succesor = successor

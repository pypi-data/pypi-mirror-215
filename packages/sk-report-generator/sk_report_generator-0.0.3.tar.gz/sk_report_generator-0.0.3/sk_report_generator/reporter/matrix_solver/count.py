from ...base import IMethod
import regex
import math
class Count:
    def __init__(self):
        pass

    def evaluate(self,obj_name,obj_value,obj_method_name,obj_method_arguments):

        if obj_method_name == 'count':
            if type(obj_value) == list:
                if len(obj_method_arguments) == 1:
                    arg1 = obj_method_arguments[0]
                    x = int(arg1) if arg1.endswith('.0') or '.' not in arg1 else float(arg1)
                    obj_value = obj_value.count(x)
        return self.succesor.evaluate(obj_name,obj_value,obj_method_name,obj_method_arguments)


    def set_succesor(self,successor):
        self.succesor = successor

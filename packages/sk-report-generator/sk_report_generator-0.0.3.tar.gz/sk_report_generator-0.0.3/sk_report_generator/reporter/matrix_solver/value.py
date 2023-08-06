from ...base import IMethod
import regex
class Value:
    def __init__(self):
        pass

    def evaluate(self,obj_name,obj_value,obj_method_name,obj_method_arguments):
        if obj_method_name == 'value':
            if len(obj_method_arguments) == 0:
                obj_value = obj_value
            if len(obj_method_arguments) != 0:
                for arg in obj_method_arguments:

                    obj_value = obj_value[int(arg) if str(arg).replace('.', '').isnumeric() else arg]

        return self.succesor.evaluate(obj_name,obj_value,obj_method_name,obj_method_arguments)


    def set_succesor(self,successor):
        self.succesor = successor

from ...base import IMethod
import regex
class Min:
    def __init__(self):
        pass

    def evaluate(self,obj_name,obj_value,obj_method_name,obj_method_arguments):
        if obj_method_name == 'min':
            if len(obj_method_arguments) == 0:
                obj_value = min(obj_value)
            if len(obj_method_arguments) != 0:
                pattern = r'\((.)*?\)=>(.*)$'
                conditional_argument = [condition for index, condition in enumerate(obj_method_arguments) if '=>' in condition][0]
                matches = regex.search(pattern, conditional_argument)
                condition = eval(f"[{matches[1]} for index, {matches[1]} in enumerate({obj_value}) if  {matches[2]}]")
                obj_value = min(condition)
        return self.succesor.evaluate(obj_name,obj_value,obj_method_name,obj_method_arguments)


    def set_succesor(self,successor):
        self.succesor = successor

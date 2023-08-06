from ...base import IMethod
import regex
class Avg:
    def __init__(self):
        pass

    def evaluate(self,obj_name,obj_value,obj_method_name,obj_method_arguments):
        if obj_method_name == 'avg':
            if len(obj_method_arguments) == 0:
                obj_value = sum(obj_value) / len(obj_value)
            if len(obj_method_arguments) != 0:
                pattern = r'\((.)*?\)=>(.*)$'
                conditional_argument = [condition for index, condition in enumerate(self.obj_method_arguments) if '=>' in condition][0]
                matches = regex.search(pattern, conditional_argument)
                condition = eval(f"[{matches[1]} for index, {matches[1]} in enumerate({self.value}) if {matches[2]}]")
                obj_value = sum(condition) / len(condition)
        return self.succesor.evaluate(obj_name,obj_value,obj_method_name,obj_method_arguments)


    def set_succesor(self,successor):
        self.succesor = successor

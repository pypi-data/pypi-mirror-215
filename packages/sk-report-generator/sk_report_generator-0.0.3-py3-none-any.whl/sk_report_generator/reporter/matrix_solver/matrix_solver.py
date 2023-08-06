import regex
import json
import math
from .min import Min
from .max import Max
from .avg import Avg
from .ceil import Ceil
from .floor import Floor
from .count import Count
from .sum import Sum
from .len import Len
from .value import Value
from .default import Default
class MatrixSolver:
    def __init__(self):
        self.min = Min()
        self.max = Max()
        self.avg = Avg()
        self.ceil = Ceil()
        self.floor = Floor()
        self.count = Count()
        self.sum = Sum()
        self.len = Len()
        self.get_value = Value()
        self.default = Default()

        self.min.set_succesor(self.max)
        self.max.set_succesor(self.avg)
        self.avg.set_succesor(self.ceil)
        self.ceil.set_succesor(self.floor)
        self.floor.set_succesor(self.count)
        self.count.set_succesor(self.sum)
        self.sum.set_succesor(self.len)
        self.len.set_succesor(self.get_value)
        self.get_value.set_succesor(self.default)




    def declare_object(self, obj, value):
        self.obj = obj
        self.value = value
        self.convert_value()
        self.get_object_name()
        self.get_object_methods()

    def get_result(self):
        self.solve()
        self.result = self.value
        return self.result

    def get_object_name(self):
        pattern = r'\$[^.\[]+'
        match = regex.search(pattern, self.obj)
        self.obj_name = match[0]

    def get_object_methods(self):
        pattern = r'\.([^\.]+)'
        matches = regex.findall(pattern, self.obj)
        value_search_pattern = r'\[(.*?)\]'
        index_keys = [item.replace("'", '').replace('"', '') for index, item in enumerate(regex.findall(value_search_pattern, self.obj))]
        self.index_keys = index_keys
        self.obj_methods = matches

    def solve(self):
        if self.obj_methods:
            for method in self.obj_methods:
                self.get_method_name(method)
                self.get_method_arguments(method)
                self.value = self.min.evaluate(self.obj_name,self.value,self.obj_method_name,self.obj_method_arguments)

        elif self.index_keys:
            method = 'value('
            i = 0
            while True:
                if i != len(self.index_keys)-1:
                    method = method + str(self.index_keys[i] if self.index_keys[i].isnumeric() else f"{self.index_keys[i]}") + ','
                else:
                    method = method + str(self.index_keys[i] if self.index_keys[i].isnumeric() else f"{self.index_keys[i]}") + ')'
                    break
                i = i+1

            self.obj_methods = self.obj_methods + [method]
            self.index_keys = None
            self.solve()
        else:
            self.value = self.obj

    def convert_value(self):
        try:
            self.value = json.loads(str(self.value).replace("'", '"'))
        except json.decoder.JSONDecodeError:
            pass

    def get_method_name(self, method):
        pattern = r'^[^\(]+'
        match = regex.search(pattern, method)
        self.obj_method_name = match[0]

    def change_object_call_format(self):
        pass

    def get_method_arguments(self, method):
        method = regex.sub(r'^.*?[\(]|[\)]$', '', method)
        self.obj_method_arguments = [item.replace("'", '').replace('"', '') for index, item in enumerate(method.split(',')) if item != '' and item not in self.obj_methods]

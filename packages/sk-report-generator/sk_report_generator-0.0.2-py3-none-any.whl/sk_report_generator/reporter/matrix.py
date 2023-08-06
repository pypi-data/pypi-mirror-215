from ..base import IReporter
from .matrix_solver.matrix_solver import MatrixSolver
import regex


class Matrix(IReporter):

    def __init__(self):
        self.matrix_solver = MatrixSolver()

    def report(self, template):
        matrix_pattern = r'({{[^{}]+}})'
        objects_values = {
            item: self.data[var] for item in regex.findall(matrix_pattern, template)
            for index, var in enumerate(self.data) if var in item
        }

        for obj, value in objects_values.items():
            obj_call = self.get_object_call(obj)
            self.matrix_solver.declare_object(obj_call, value)
            result = self.matrix_solver.get_result()
            replacement = regex.sub(regex.escape(obj_call), str(result), obj)
            template = regex.sub(regex.escape(obj), replacement, template)

        return self.successor.report(template)

    def set_successor(self, successor):
        self.successor = successor

    def set_data(self, data):
        self.data = data

    def get_object_call(self, obj):
        pattern = r'\s*[^{}:]+\s*'
        match = regex.search(pattern, obj)
        return match[0]


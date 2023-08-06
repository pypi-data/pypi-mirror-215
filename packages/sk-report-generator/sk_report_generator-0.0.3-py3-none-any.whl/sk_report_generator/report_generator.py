import regex
from  .reporter.format import Formater
from .reporter.variable import VariableReporter
from .reporter.default import Default
from .reporter.matrix import Matrix
from .reporter.script_evaluate import ScriptEvaluate
class ReportGenerator:

    def __init__(self):
        self.variable_reporter= VariableReporter()
        self.formater = Formater()
        self.default = Default()
        self.matrix = Matrix()
        self.script =ScriptEvaluate()

        self.variable_reporter.set_successor(self.matrix)
        self.matrix.set_successor(self.script)
        self.script.set_successor(self.formater)
        self.formater.set_successor(self.default)


    def generate_report(self,template,data):

        self.variable_reporter.set_data(data)
        self.matrix.set_data(data)
        self.formater.set_data(data)

        return self.variable_reporter.report(template)

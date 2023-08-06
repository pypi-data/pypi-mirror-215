from ..base import IReporter
import regex
import io
import sys
class ScriptEvaluate(IReporter):

    def __init__(self):
        self.scripts = None
        self.template = None
        self.script_values  ={}
        self.row_scripts = None


    def report (self,template):
        self.template = template
        script_pattern = r'\{%python%\}([\s\S]*?)\{%endpython%\}'

        scripts_list_1 = regex.findall(script_pattern,self.template)
        script_pattern = r'\{\{%\s*(.*?)%\}\}'
        scripts_list_2 = regex.findall(script_pattern,self.template)
        self.row_scripts = scripts_list_1+scripts_list_2
        self.process_scripts()

        self.run_scripts()

        self.update_template()





        return self.successor.report(self.template)

    def set_successor(self,successor):
        self.successor = successor


    def set_data(self,data):
        self.data = data

    def run_scripts(self):
        for row_script,script in self.scripts.items():

            output_stream = io.StringIO()
            sys.stdout = output_stream

            code_string = script
            exec(code_string)

            sys.stdout = sys.__stdout__
            captured_output = output_stream.getvalue()

            self.script_values[row_script] =captured_output
    def process_scripts(self):
        temp = {}
        for script in self.row_scripts:
            value  = self.successor.report(script)
            temp[script] = value

        self.scripts = temp



    def update_template(self):

        for script,value in self.script_values.items():

            pattern = r'(\{\{%\s*'+regex.escape(script)+r'%\}\})|(\{%python%\}'+regex.escape(script)+r'\{%endpython%\})'

            self.template = regex.sub(pattern,value,self.template)


        return self.template






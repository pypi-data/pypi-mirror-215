from ..base import IReporter
import regex
class VariableReporter(IReporter):

    def report (self,template):
        pattern = r'{{.*?}}'
        matches = regex.findall(pattern,template)
        match_value  = ''
        for match in matches:
            match_value = match
            for variable,value in self.data.items():

                variale_pattern = regex.escape(variable)+r'\b'
                if str(value).replace(' ','').replace('.','').isnumeric():
                    match_value = regex.sub(variale_pattern,str(value),match_value)


            template  = regex.sub(regex.escape(match),match_value,template)


        return self.successor.report(template)

    def set_successor(self,successor):
        self.successor = successor
    def set_data(self,data):
        self.data = data

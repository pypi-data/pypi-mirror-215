from ..base import IReporter
import regex
class Default(IReporter):

    def report (self,template):
        b = r'({{([^{}]+)}})'
        matches = regex.findall(b,template)
        for match,value in matches:

            if '$' not in value:
                template = regex.sub(regex.escape(match),value,template)

        return template

    def set_successor(self,successor):
        pass
    def set_data(self,data):
        self.data = data

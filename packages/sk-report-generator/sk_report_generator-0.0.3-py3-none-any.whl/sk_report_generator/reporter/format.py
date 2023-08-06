import regex
from ..base import IReporter
class Formater(IReporter):
    def report(self,template):
        format_pattern = r'(?<=[^\{]\{\{)[^{}]+:[^{}]+(?=\}\}[^\}])'
        matches =  regex.findall(format_pattern,template)

        for match in matches:

            value,formula = match.replace(' ','').split(':')
            try:
                value = int(value) if value.endswith('.0') or '.' not in value else float(value)
                formula = formula
                replacement =format(value, formula)

            except ValueError as error:
                error_message = str(error)
                replacement = f'({value}, {error_message})'


            pattern = r'({{)\s*'+regex.escape(match)+'\s*(}})'
            template = regex.sub(pattern,replacement,template)

        return self.successor.report(template)

    def set_successor(self,successor):
        self.successor = successor
    def set_data(self,data):
        self.data = data

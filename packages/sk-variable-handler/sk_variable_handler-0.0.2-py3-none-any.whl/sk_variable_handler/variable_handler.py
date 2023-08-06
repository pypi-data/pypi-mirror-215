import regex as re
import json

class VariableHandler:
    def __init__(self):
        self.constant_expression_list = {}
        self.variable_expression_list = {}
        self.declaration_list = {}
        self.matrix_list = {}
        self.flag = 0
        self.iterate = 0
        self.recursive_variable = {}
        self.calculator = None

    def set_calculator(self, calculator):
        self.calculator = calculator


    def remove_comments(self):
        single_line_comment = r'\#[^\$]+($)?'
        self.declarations = re.sub(single_line_comment, '', self.declarations)

        multiline_comment = r'\\\*[^\\]+\*\\'
        self.declarations = re.sub(multiline_comment, '', self.declarations)

        self.declarations = self.declarations.strip()

    def validate(self):
        pass
    def exception_handle(self):
        temp = {}
        for key,value in self.declaration_list.items():
            if '$' in value:
##                print(f'Unkonw Variable present {key} = {value}')
                pass
        for key,value in temp.items():
            del self.declaration_list[key]



    def declare(self):
        pattern = '\$[^=]+=[^;]+'

        declare_text = re.sub('\n|\s+','',self.declarations)
        declarations = re.findall(pattern, self.declarations)

        for declaration in declarations:
            matches = list(filter(None, re.split(r'\s*(\$[^=]+)\s*=\s*', declaration)))

            variable, expression = matches if len(matches)>1 else [matches[0],'0']

            variable =variable.replace(' ','')

            if variable in self.declaration_list and (variable in expression or variable in self.recursive_variable):
                if len(self.recursive_variable) ==0:
                    self.recursive_variable[variable] = [self.declaration_list[variable]] + [expression]
                    continue

                if type(self.recursive_variable[variable]) ==list:
                    self.recursive_variable[variable] =self.recursive_variable[variable] + [expression]
            else:
                self.declaration_list[variable] = expression

    def get_constant_expression_list(self):
        for variable, expression in self.declaration_list.items():
            if '$' not in expression and '[' not in expression and '{' not in expression:

                value =str(self.calculator.evaluate(expression))
                if 'Unsupported' in str(value):
                    value = expression.replace('"','').replace("'",'')
                self.constant_expression_list[variable] =value
                self.declaration_list[variable] = value

    def get_variable_expression_list(self):
        for variable, expression in self.declaration_list.items():
            if '$' in expression and '[' not in expression and '{' not in expression:

                self.variable_expression_list[variable]=expression

    def solve_variable_expression_list(self):
        if self.iterate > self.flag:
            self.exception_handle()
            return


        temp = {}
        for variable, expression in self.variable_expression_list.items():
            temp_expression = expression
            for key, value in self.constant_expression_list.items():
                pattern = re.escape(key) + r'(\s|\b)'
                temp_expression = re.sub(pattern, str(value), temp_expression)
            temp[variable] = temp_expression

        for variable, expression in temp.items():
            value =expression
            if '$' not in expression:
                value =str(self.calculator.evaluate(expression))
                self.constant_expression_list[variable] =value
                del self.variable_expression_list[variable]
                self.declaration_list[variable] = value
            else:
                self.variable_expression_list[variable]= value
                self.declaration_list[variable] = value
        iterate = False
        if [value for value in self.variable_expression_list.values() if '$' in value]:

            iterate = True
        if iterate:
            self.iterate += 1
            self.solve_variable_expression_list()
    def matrix_handler(self):
        pass
    def get_matrix(self):
        for key,value in self.declaration_list.items():
            if '[' in value or '{' in value:
                self.matrix_list[key] = value
    def solve_matrix(self):
        temp = {}
        for key,value in self.matrix_list.items():
            value = str(value)
            pattern = r'eval(\((?>[^()]|(?1))*\))'
            expression_list =[item for index,item in enumerate(re.findall(pattern,value)) if item != ' ' ]


            for expression in expression_list:
                expression_value =str(self.calculator.evaluate(expression))
                pattern = r'eval'+re.escape(expression)
                value = re.sub(pattern,expression_value,value)
            temp[key] = value
        for key,value in temp.items():
            try:
                value = json.loads(value.replace("'",'"'))
            except:
                pass
            self.matrix_list[key] = value
            self.declaration_list[key] = value
    def solve_variable_matrix(self):
        temp = {}
        for key,value in self.matrix_list.items():
            for variable,expressaion in self.constant_expression_list.items():
                pattern =  re.escape(variable)+r'(?:\b|\s)'
                value  = re.sub(pattern,expressaion,value)
            temp[key] = value
        for key,value in temp.items():


            self.matrix_list[key] =value
            self.declaration_list[key] = value

    def solve_recursive_variable(self):

        for key,values in self.recursive_variable.items():
            i = 1
            values = values[::-1]
            if type(values) ==str:
##                self.variable_expression_list[key] = '0'
                break

            value = values[0]

            while i<len(values):
                value = value.replace(key,f'({values[i]})')
                i = i+1
            if key in value:

                continue
            self.variable_expression_list[key] = value






    def get_values(self, declarations):
        self.constant_expression_list = {}
        self.variable_expression_list = {}
        self.declaration_list = {}
        self.matrix_list = {}
        self.flag = 0
        self.iterate = 0
        self.recursive_variable = {}


        self.declarations = declarations
        self.validate()
        self.remove_comments()
        self.flag = self.declarations.count('$')
        self.declare()
        self.get_matrix()
        self.get_constant_expression_list()
        self.get_variable_expression_list()
        self.solve_recursive_variable()
        self.solve_variable_expression_list()
        self.solve_variable_matrix()
        self.solve_matrix()
        self.declaration_list

        return self.declaration_list
# coding: konira

from cStringIO import StringIO
from konira import tokenizer


describe "quote remover":


    before each:
        self.remover = tokenizer.quote_remover


    it "removes commas from strings":
        assert self.remover("a,separated,string") == "aseparatedstring"


    it "removes commas respecting whitespace":
        assert self.remover("a, separated, string") == "a separated string"


    it "removes single quotes from strings":
        assert self.remover("a ' string '") == "a  string "


    it "removes a combination of commas and quotes":
        assert self.remover("a, 'string',") == "a string"


    it "removes dots from strings":
        assert self.remover("a. dotted. string.") == "a dotted string"


    it "respects camel case strings":
        assert self.remover("a Camel Case string") == "a Camel Case string"



describe "valid method names":


    before each:
        self.valid = tokenizer.valid_method_name


    it "replaces whitespace with underscores":
        assert self.valid("a name with underscores") == "it_a_name_with_underscores"


    it "removes double quotes from strings":
        assert self.valid('a double \"quoted\" string') == "it_a_double_quoted_string"


    it "removes commas from strings":
        assert self.valid('a ,in a string,') == "it_a_in_a_string"


    it "removes commas quotes and double quotes from strings":
        assert self.valid('a \", in a string\'') == 'it_a__in_a_string'


    it "removes dots from strings":
        assert self.valid("a. dotted. string.") == "it_a_dotted_string"


    it "respects camel case from strings":
        assert self.valid("a CamelCase string") == "it_a_CamelCase_string"



describe "valid class names":


    before each:
        self.valid = tokenizer.valid_class_name


    it "replaces whitespace with underscores":
        assert self.valid("a string with whitespace") == "Case_a_string_with_whitespace"


    it "removes double quotes from strings":
        assert self.valid("a string\"") == "Case_a_string"


    it "removes dots and commas from strings":
        assert self.valid("a. string, \'") == "Case_a_string_"


    it "removes single quotes from strings":
        assert self.valid("\'single quote") == "Case_single_quote"


    it "respects camel case in strings":
        assert self.valid("my Test") == "Case_my_Test"



describe "translate dsl into valid Python":
    

    before each:
        self.translate = tokenizer.translate
        self.line      = StringIO


    it "always has import konira at the top":
        line = self.line('').readline
        assert self.translate(line) == [[1, 'import'], [1, 'konira'], [0, '']] 

    
    it "translates describe into a class":
        line = self.line('describe "my test class":\n pass')
        result = self.translate(line.readline)
        assert len(result) == 13
        assert result[0]   == [1, 'import']
        assert result[1]   == [1, 'konira']
        assert result[2]   == [1, 'class']
        assert result[3]   == [1, 'Case_my_test_class']
        assert result[4]   == [51, '(']
        assert result[5]   == [1, 'object']
        assert result[6]   == [51, ')']
        assert result[7]   == [51, ':']
        assert result[8]   == [4, '\n']
        assert result[9]   == [5, ' ']
        assert result[10]  == [1, 'pass']
        assert result[11]  == [6, '']
        assert result[12]  == [0, '']
        

    it "translates an it to a def":
        line = self.line('it "should test my method":\n pass')
        result = self.translate(line.readline)
        assert len(result) == 13
        assert result[0]   == [1, 'import']
        assert result[1]   == [1, 'konira']
        assert result[2]   == [1, 'def']
        assert result[3]   == [3, 'it_should_test_my_method']
        assert result[4]   == [51, '(']
        assert result[5]   == [1, 'self']
        assert result[6]   == [51, ')']
        assert result[7]   == [51, ':']
        assert result[8]   == [4, '\n']
        assert result[9]   == [5, ' ']
        assert result[10]  == [1, 'pass']
        assert result[11]  == [6, '']
        assert result[12]  == [0, '']


    it "translates a describe with inheritance":
        line = self.line('describe "my test class", Foo:\n pass')
        result = self.translate(line.readline)
        assert len(result) == 13
        assert result[0]   == [1, 'import']
        assert result[1]   == [1, 'konira']
        assert result[2]   == [1, 'class']
        assert result[3]   == [1, 'Case_my_test_class']
        assert result[4]   == [51, '(']
        assert result[5]   == [1, 'Foo']
        assert result[6]   == [51, ')']
        assert result[7]   == [51, ':']
        assert result[8]   == [4, '\n']
        assert result[9]   == [5, ' ']
        assert result[10]  == [1, 'pass']
        assert result[11]  == [6, '']
        assert result[12]  == [0, '']


    it "translates a describe with inheritance regardless of space":
        line = self.line('describe "my test class",Foo:\n pass')
        result = self.translate(line.readline)
        assert len(result) == 13
        assert result[0]   == [1, 'import']
        assert result[1]   == [1, 'konira']
        assert result[2]   == [1, 'class']
        assert result[3]   == [1, 'Case_my_test_class']
        assert result[4]   == [51, '(']
        assert result[5]   == [1, 'Foo']
        assert result[6]   == [51, ')']
        assert result[7]   == [51, ':']
        assert result[8]   == [4, '\n']
        assert result[9]   == [5, ' ']
        assert result[10]  == [1, 'pass']
        assert result[11]  == [6, '']
        assert result[12]  == [0, '']


    it "translates a describe with inheritance with a lot of whitespace":
        line = self.line('describe "my test class"    ,          Foo:\n pass')
        result = self.translate(line.readline)
        assert len(result) == 13
        assert result[0]   == [1, 'import']
        assert result[1]   == [1, 'konira']
        assert result[2]   == [1, 'class']
        assert result[3]   == [1, 'Case_my_test_class']
        assert result[4]   == [51, '(']
        assert result[5]   == [1, 'Foo']
        assert result[6]   == [51, ')']
        assert result[7]   == [51, ':']
        assert result[8]   == [4, '\n']
        assert result[9]   == [5, ' ']
        assert result[10]  == [1, 'pass']
        assert result[11]  == [6, '']
        assert result[12]  == [0, '']
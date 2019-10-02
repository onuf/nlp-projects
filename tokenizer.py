"""

This module is designed for string tokenization.
Class `Token` represents a token and class `Tokenizer` performs tokenization.

"""


import unicodedata


class Token(object):
    """A token with its attributes and properties."""

    def __init__(self, start, end, string, cur_type):
        """
        :param start: an index of the first symbol of the token in the string.
        :param end: an index of the next symbol after the token in the string.
        :param string: a string being tokenized.
        :param cur_type: a type of the token based on its content (letter, digit, space, punctuation mark, other).
        """
        self.start = start
        self.end = end
        self.string = string
        self.type = cur_type

    @property
    def length(self):
        return self.end - self.start
    
    @property
    def token(self):
        return self.string[self.start:self.end]

    def __eq__(self, other):
        return (self.start == other.start and self.string == other.string
                and self.end == other.end and self.type == other.type)

    def __repr__(self):
        return f'{self.token}: [{self.start}:{self.end}], {self.type}'


class Tokenizer(object):
    """

    Class of tokenizers.

    A token is understood differently in the methods of this class:
    
    `a_tokenize` - takes a string and returns its alphabetical tokens.
    `ad_tokenize` - takes a string and returns its alphabetical and digital tokens.
    `i_tokenize` - takes a string and generates its tokens.
    `tokenize` - takes a string and returns all its tokens.
    
    """
    
    @staticmethod
    def type_id(char):
        """
        This static method identifies the type of a token.
        :param char: a string whose contents determine the type.
        :return: a string with the type (alpha, digit, space, punct or other).
        """
        if char.isalpha():
            return 'alpha'
        elif char.isdigit():
            return 'digit'
        elif char.isspace():
            return 'space'
        elif unicodedata.category(char).startswith('P'):
            return 'punct'
        else:
            return 'other'

    def a_tokenize(self, string):
        """
        This method collects tokens consisting of alphabetical characters.
        Only a sequence of alphabetical symbols is regarded as a token.
        :param string: a string for tokenization.
        :raise: TypeError, not given a string object.
        :return: a list of Token instances.
        """
        if not isinstance(string, str):
            raise TypeError('Only strings can be tokenized.')
        
        start = 0
        part_of_token = False  # check whether the previous character is a part of a token
        tokens = []

        for i, char in enumerate(string):

            cur_type = self.type_id(char)  # the type of the current character

            if not part_of_token and cur_type == 'alpha':
                # initiate a token
                start = i
                part_of_token = True
            elif part_of_token and cur_type != 'alpha':
                # collect the token when a non-alphabetic character appears
                tokens.append(Token(start, i, string, 'alpha'))
                part_of_token = False

        # The last token will be added to the list only if the string's end is marked by a non-alphabetic symbol.
        # Otherwise, this block allows to capture the token.
        if string and part_of_token and self.type_id(string[-1]) == 'alpha':
            tokens.append(Token(start, i + 1, string, 'alpha'))
        
        return tokens

    def ad_tokenize(self, string):
        """
        This method collects tokens consisting of alphabetical or digital characters.
        :param string: a string for tokenization.
        :raise: TypeError, not given a string object.
        :return: a list of Token instances.
        """
        if not isinstance(string, str):
            raise TypeError('Only strings can be tokenized.')
        
        start = 0
        tokens = []
        
        for i, char in enumerate(string):

            if i:
                # start with the second character
                prev_type = self.type_id(string[i-1])  # the type of the previous character
                cur_type = self.type_id(char)          # the type of the current character

                if cur_type != prev_type:

                    if prev_type == 'alpha' or prev_type == 'digit':
                        # collect the token when the types differ
                        tokens.append(Token(start, i, string, prev_type))
                    
                    # update the start position    
                    start = i
            
        # This block allows to capture the last token.
        if string:
            cur_type = self.type_id(string[-1])
            if cur_type == 'alpha' or cur_type == 'digit':
                tokens.append(Token(start, len(string), string, cur_type))
        
        return tokens
    
    def tokenize(self, string):
        """
        This method allows you to tokenize the whole string.
        :param string: a string for tokenization.
        :raise: TypeError, not given a string object.
        :return: a list of Token instances.
        """
        if not isinstance(string, str):
            raise TypeError('Only strings can be tokenized.')
        
        start = 0
        tokens = []

        for i, char in enumerate(string):

            if i:
                # start with the second character
                prev_type = self.type_id(string[i-1])  # the type of the previous character
                cur_type = self.type_id(char)          # the type of the current character

                if cur_type != prev_type:
                    # collect the token when the types differ
                    tokens.append(Token(start, i, string, prev_type))
                    start = i

        # This block allows to capture the last token if string is not empty.
        if string:
            cur_type = self.type_id(string[-1])
            tokens.append(Token(start, len(string), string, cur_type))

        return tokens

    def i_tokenize(self, string):
            """
            This tokenizer yields tokens from a string.
            An alternative to method `tokenize`.
            :param string: a string for tokenization.
            :raise: TypeError, not given a string object.
            :yield: Token instances.
            """
            if not isinstance(string, str):
                raise TypeError('Only strings can be tokenized.')
            
            start = 0

            for i, char in enumerate(string):

                if i:
                    # start with the second character
                    prev_type = self.type_id(string[i-1])  # the type of the previous character
                    cur_type = self.type_id(char)          # the type of the current character

                    if cur_type != prev_type:
                        # collect the token when the types differ
                        yield Token(start, i, string, prev_type)
                        start = i
                
            # This block allows to capture the last token if string is not empty.
            if string:
                cur_type = self.type_id(string[-1])
                yield Token(start, len(string), string, cur_type)

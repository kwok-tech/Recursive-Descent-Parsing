#Name: Jack Kwok
#CMPSC 461 Assignment Due: 2/5/2022 6pm

#Prof. Gary Tan: Parsing has 2 steps, lexical and syntactical analysis

# the first step is to recognize tokens, the second step is to construct a tree
WEBPAGE, TEXT, LISTITEM, STRING, KEYWORD, EOI, INVALID = 1, 2, 3, 4, 5, 6, 7

def typeToString (tp):
    if (tp == WEBPAGE) :
        return "Webpage"
    elif (tp == TEXT) :
        return "Text"
    elif (tp == LISTITEM) :
        return "ListItem"
    elif (tp == STRING) :
        return "String"
    elif (tp == KEYWORD) :
        return "Keyword"
    elif (tp == EOI) :
        return "EOI"
    return "Invalid"

#Tokens: Webpage, Text, ListItem, String, Letter, Digit, Keyword
class Token:
    "A class for representing Tokens"

    # a Token object has two fields: the token's type and its value
    def __init__ (self, tokenType, tokenVal):
        self.type = tokenType
        self.val = tokenVal

    def getTokenType(self):
        return self.type

    def getTokenValue(self):
        return self.val

    def __repr__(self):
        if (self.type in [WEBPAGE, TEXT, LISTITEM, STRING, KEYWORD]):
            return self.val
        elif (self.type == EOI):
            return ""
        else:
            return "invalid"

LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGITS = "0123456789"
KEYWORDLIST = ["<body>", "</body>", "<b>", "</b>", "<i>", "</i>", "<ul>", "</ul>", "<li>", "</li>"]

class Lexer:

    # stmt is the current statement to perform the lexing;
    # index is the index of the next char in the statement
    def __init__ (self, s):
        self.stmt = s
        self.index = 0
        self.nextChar()

    def nextToken(self):
        while True:
            if self.ch == ' ': self.nextChar()  # whitespace
            elif self.ch.isalpha(): # is a letter
                str = self.consumeChars(LETTERS + DIGITS)
                return Token(STRING, str)
            elif self.ch == '<': #is a keyword
                # creates keyword
                keyword = "<"
                self.nextChar()
                while (self.ch != '>'):
                    keyword += self.ch
                    self.nextChar()
                keyword += ">"
                self.nextChar()
                for x in KEYWORDLIST:
                    if (x == keyword):
                        return Token(KEYWORD, keyword)
            elif self.ch == '$':
                return Token(EOI,"")
            else:
                self.nextChar()
                return Token(INVALID, self.ch)

    def nextChar(self):
        self.ch = self.stmt[self.index] 
        self.index = self.index + 1

    def consumeChars (self, charSet):
        r = self.ch
        self.nextChar()
        while (self.ch in charSet):
            r = r + self.ch
            self.nextChar()
        return r

    def checkChar(self, c):
        if (self.ch==c):
            self.nextChar()
            return True
        else: return False

import sys

class Parser:
    def __init__(self, s):
        self.lexer = Lexer(s+"$")
        self.token = self.lexer.nextToken()

    def run(self):
        self.webpage()

    def webpage(self):
        print("WEBPAGE")
        if self.token.getTokenValue() == "<body>":
            self.text()
            while self.token.getTokenValue() != "</body>":
                self.token = self.lexer.nextToken()
                self.text()
            self.match(EOI)
            print("WEBPAGE END")

    def listItem(self):
        if self.token.getTokenValue() == "<li>":
            key = self.match(KEYWORD)
            print("\t\t\t\tKEYWORD" + key + "KEYWORD")
        if self.token.getTokenType() == STRING:
            print("\t\t\t" + self.token.getTokenValue())
            self.token = self.lexer.nextToken()
            key = self.match(KEYWORD)
            print("\t\t\t\tKEYWORD" + key + "KEYWORD")

    # eKs = []
    endingKey = ""
    def text(self):
        print("\tTEXT")
        if self.token.getTokenType() == STRING:
            print("\t\t\t" + self.token.getTokenValue())
        elif self.token.getTokenType() == KEYWORD:
            if self.token.getTokenValue() == "<li>":
                self.listItem()
            #ending keyword
            Parser.endingKey += self.token.getTokenValue()
            key = self.match(KEYWORD)
            print("\t\tKEYWORD" + key + "KEYWORD")
            if (Parser.endingKey[1] != "/"):
                Parser.endingKey = Parser.endingKey[:1] + '/' + Parser.endingKey[1:]
                while (self.token.getTokenValue() != Parser.endingKey):
                    self.text()
            #checks if appeared before stores if not
            # inList = True
            # for i in Parser.eKs:
            #     if (i != endingKey):
            #         inList = False
            #         #add to list
            #         Parser.eKs.append(endingKey)
            #         while (self.token.getTokenValue() != endingKey):
            #             self.text()
            #     elif (inList == True):
            #         Parser.eKs.remove(endingKey)
            #         while (self.token.getTokenValue() != endingKey):
            #             self.text()
            if self.token.getTokenValue() == "<ul>":
                print("\t\tKEYWORD<ul>KEYWORD")
                self.token = self.lexer.nextToken()
                self.listItem()
        else:
            print("Syntax error: expecting an int or char" \
                  + "; saw:" \
                  + typeToString(self.token.getTokenType()))
            sys.exit(1)
        self.token = self.lexer.nextToken()
        print("\tTEXT END")


    def match (self, tp):
        val = self.token.getTokenValue()
        if (self.token.getTokenType() == tp):
            self.token = self.lexer.nextToken()
        else: self.error(tp)
        return val

    def error(self, tp):
        print ("Syntax error: expecting: " + typeToString(tp) \
               + "; saw: " + typeToString(self.token.getTokenType()))
        sys.exit(1)


print("Testing the lexer: test 1")
lex = Lexer ("<body> google <b><i><b> yahoo</b></i></b></body> $")
tk = lex.nextToken()
while (tk.getTokenType() != EOI):
    print(tk)
    tk = lex.nextToken()
print("")



print("Testing the parser: test 1")
parser = Parser ("<body> google <b><i><b><ul> <li> item1 <\li> <li> item2 <\li> </ul> yahoo</b></i></b></body>")
parser.run()


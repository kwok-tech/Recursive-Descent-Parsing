# Recursive-Descent-Parsing

Penn State CMPSC 461 Assignment: Parsing has 2 steps, lexical and syntactical analysis

The following program defines a Lexer and Parser class for processing a simple HTML-like language. The program is designed to take in an input string and check if it is a valid expression in the language.

The input string is expected to contain "Webpage" elements, which can contain "Text" elements or "ListItem" elements. "Text" elements can contain strings, which are sequences of letters and digits, and "bold" and "italic" tags. "ListItem" elements are similar to "Text" elements, but can also contain "unordered list" tags.

The input string is expected to be in the following format:

```
<body>
    [Text | ListItem]
    [Text | ListItem]
    ...
</body>
```
Each "Text" element is expected to be in the following format:

```
[<b>]
    [String]
[</b>]
[<i>]
    [String]
[</i>]
```
Each "ListItem" element is expected to be in the following format:

```
<ul>
    <li>
        [String]
    </li>
</ul>
```
To use the program, first create a Lexer object with the input string and a Parser object with the Lexer object. Then call the run() method of the Parser object. If the input string is a valid expression in the language, the program will print "WEBPAGE" and the details of each element in the input string. If the input string is not a valid expression, an error message will be printed.





# This file was created to test Python JavaScript parsers

from pyjsparser import parse

test1Code = 'var $ = "Hello!";'
test2Code = 'let x = 13;'
test3Code = 'if (1 == 2) '
test4Code = 'x = x + 1'
y = parse(test1Code +  test2Code + test3Code + test4Code)
x = 2
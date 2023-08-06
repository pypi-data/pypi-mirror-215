from tapescript import parsing
symbols = ['{', 'a', '{', 'b', '}', 'c', '}', 'd', '{', 'e', '}']

index = parsing._find_matching_brace(symbols, '{', '}')

print(symbols)
print(index)
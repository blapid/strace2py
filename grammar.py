from parsimonious.grammar import Grammar

grammar = Grammar(
'''
    entry = entry_prefix? syscall entry_suffix?

    entry_prefix = "UNUSED"
    entry_suffix = "UNUSED"

    syscall = syscall_name "(" argument_list ")" " "+ "=" " "+  ret_val
    argument_list = argument? (", " argument)*
    ret_val = symbol ("(" symbol ")")?
    syscall_name = symbol / "UNUSED"

    argument = comment / truncated_args / dict / list / literal

    dict = "{" dict_argument? (", " dict_argument)* "}"
    dict_argument = truncated_args / dict_kv / argument
    dict_kv = symbol "=" argument

    list = "[" argument? (", " argument)* "]"

    literal = function_call / string / bytes / symbol

    function_call = symbol "(" argument_list ")"
    truncated_args = "..."
    comment = "/*" string_chars "*/"
    symbol = ~"[\?a-zA-Z 0-9_\-\|\*]*"i truncated_args?
    string = ~"[\\"]"i string_chars ~"[\\"]"i truncated_args?
    string_chars = ~"[a-zA-Z \t0-9_/\.\|\-]*"i
    bytes = ~"[\\"][ -~]*[\\"]"i truncated_args?
''')

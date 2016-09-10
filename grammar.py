from parsimonious.grammar import Grammar

grammar = Grammar(
'''
    entry = entry_prefix? syscall entry_suffix?

    entry_prefix = "UNUSED"
    entry_suffix = "UNUSED"

    syscall = syscall_name "(" argument_list ")" " "+ "=" " "+  ret_val
    argument_list = (argument_list_value)*
    ret_val = symbol argument?
    syscall_name = symbol / "UNUSED"

    argument_list_value = separator? argument
    argument = comment / truncated_args / keyval / dict / list / literal

    dict = "{" (dict_argument)* "}"
    dict_argument = separator? (truncated_args / keyval / argument)
    keyval = symbol "=" argument

    list = "[" (list_value)* "]"
    list_value = separator? argument

    literal = function_call / string / bytes / symbol

    function_call = symbol "(" argument_list ")"
    truncated_args = "..."
    comment = "/*" string_chars "*/"
    symbol = ~"[\?a-zA-Z 0-9_\-\|\*]*"i truncated_args?
    string = ~"[\\"]"i string_chars ~"[\\"]"i truncated_args?
    string_chars = ~"[a-zA-Z \t0-9_/\.\|\-]*"i
    bytes = ~"[\\"][ -~]*[\\"]"i truncated_args?
    separator = ", "
''')

#!/usr/bin/env python
import sys
import parsimonious
import grammar

class StraceVisitor(parsimonious.NodeVisitor):
    def visit_argument(self, node, visited_children):
        return visited_children[0]

    def visit_entry(self, node, (prefix, entry, suffix)):
        return entry

    def visit_dict_argument(self, node, (sep, argument,)):
        if not argument:
            return argument
        if isinstance(argument, dict):
            return argument
        elif isinstance(argument, parsimonious.nodes.Node):
            if argument.expr_name == 'comment':
                return {'_comment': argument.text}
            else:
                return {'_unknown': argument.text}
        else:
            return argument

    def visit_keyval(self, node, visited_children):
        kv = {visited_children[0]: visited_children[2]}
        return kv

    def visit_dict(self, node, visited_children):
        d = {}
        i = 0
        visited_children = visited_children[1]
        if not isinstance(visited_children, list):
            visited_children = [visited_children]
        for child in visited_children:
            if isinstance(child, dict):
                d.update(child)
            else:
                d["_%d" % (i,)] = child
            i += 1
        return d

    def visit_list(self, node, visited_children):
        #print visited_children
        values = []
        visited_children = visited_children[1]
        if not isinstance(visited_children, list):
            visited_children = [visited_children]
        for child in visited_children:
            values.append(child)
        return values

    def visit_argument_list(self, node, visited_children):
        values = []
        for child in visited_children:
            values.append(child)
        return values

    def visit_argument_list_value(self, node, (sep, argument)):
        return argument

    def visit_syscall(self, node, (syscall_name,  _1,
                        argument_list,  _2, _3, _4, _5, ret_val)):
        return {
            'name': syscall_name,
            'args': argument_list or [],
            'ret': ret_val
        }

    def visit_list_value(self, node, visited_children):
        return visited_children[-1]

    def visit_syscall_name(self, node, visited_children):
        return node.text

    def visit_ret_val(self, node, visited_children):
        return node.text

    def visit_symbol(self, node, visited_children):
        return node.text

    def visit_literal(self, node, visited_children):
        return node.text

    def visit_truncated_args(self, node, visited_children):
        return node.text

    def visit_comment(self, node, visited_children):
        return node.text

    def generic_visit(self, node, visited_children):
        if len(visited_children) == 1:
            return visited_children[0]
        elif len(visited_children) == 0:
            return node.text
        else:
            values = []
            for child in visited_children:
                if not str(child):
                    continue
                values.append(child)
            return values


class StraceParser(object):
    def __init__(self, override_grammer = None):
        if override_grammer:
            self.grammar = override_grammer
        else:
            self.grammar = grammar.grammar

    def parse_line(self, line):
        parsed = self.grammar.parse(line)
        visitor = StraceVisitor()
        return visitor.visit(parsed)

def main(argv):
    p = StraceParser()
    b = open(argv[1],'rb').readlines()
    i = 0
    for line in b:
        #l = p.grammar.parse(line[:-1])
        try:
            l = p.parse_line(line[:-1])
            i += 1
            print l
        except:
            print line, i
            raise

if __name__ == '__main__':
    sys.exit(main(sys.argv))

import unittest
import strace_parser

class TestStraceParser(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestStraceParser, self).__init__(*args, **kwargs)
        self.p = strace_parser.StraceParser()

    def helper(self, line, name, args, ret):
        r = self.p.parse_line(line)
        self.assertEqual(r,
            {
                'name': name,
                'args': args,
                'ret': ret
            })

    def test_no_args(self):
        self.helper('syscall() = 0', 'syscall', [],'0')

    def test_with_args(self):
        self.helper('syscall(1, BLA|ABL, "/dev/null") = 0',
            'syscall', ["1", "BLA|ABL", "\"/dev/null\""], '0')

    def test_with_comment(self):
        self.helper('execve("/bin/ls", ["ls"], [/* 41 vars */]) = 0',
            'execve', ['"/bin/ls"', '["ls"]', '[/* 41 vars */]'], '0')

    def test_dict(self):
        self.helper('fstat(3, {st_mode=S_IFREG|0644, st_size=121824}) = 0',
            'fstat', ['3', {'st_mode': 'S_IFREG|0644',
                'st_size': '121824'}], '0')

    def test_truncated_arg(self):
        self.helper('syscall(1, BLA|ABL, ...) = 0',
            'syscall', ["1", "BLA|ABL", "..."], '0')

    def test_dict_truncated(self):
        self.helper('fstat(3, {st_mode=S_IFREG|0644, st_size=121824, ...}) = 0',
            'fstat', ['3', {'st_mode': 'S_IFREG|0644',
                'st_size': '121824', '_truncated': True}], '0')

    def test_dict_comment(self):
        self.helper('fstat(3, {st_mode=S_IFREG|0644, st_size=121824, /* comment */}) = 0',
            'fstat', ['3', {'st_mode': 'S_IFREG|0644',
                'st_size': '121824', '_comment': '/* comment */'}], '0')

if __name__ == '__main__':
    unittest.main()

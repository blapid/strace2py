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
            'execve', ['"/bin/ls"', ['"ls"'], ['/* 41 vars */']], '0')

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
                'st_size': '121824', '_2': '...'}], '0')

    def test_dict_comment(self):
        self.helper('fstat(3, {st_mode=S_IFREG|0644, st_size=121824, /* comment */}) = 0',
            'fstat', ['3', {'st_mode': 'S_IFREG|0644',
                'st_size': '121824', '_2': '/* comment */'}], '0')

    def test_bytes(self):
        self.helper(r'read(3, "\177ELF\2\1\1\0\0\0\0\0\0\0\0\0\3") = 0',
            'read', ['3', r'"\177ELF\2\1\1\0\0\0\0\0\0\0\0\0\3"'], '0')

    def test_weird_ioctl(self):
        self.helper('ioctl(1, SNDCTL_TMR_TIMEBASE or TCGETS, {B38400 opost isig icanon echo ...}) = 0',
            'ioctl', ['1', 'SNDCTL_TMR_TIMEBASE or TCGETS',
            {'_0': 'B38400 opost isig icanon echo ...'}], '0')

    def test_string_tabs_truncated(self):
        self.helper('write(1, "orbit-user\t    pulse-jLVloMsUqiG"..., 109) = 109',
            'write', ['1', '"orbit-user\t    pulse-jLVloMsUqiG"...', '109'], '109')

    def test_hex_literal(self):
        self.helper('umask(0x100) = 0',
            'umask', ['0x100'], '0')

    def test_mult_literal(self):
        self.helper('umask(0x100*100) = 0',
            'umask', ['0x100*100'], '0')

    def test_list_comment_args(self):
        self.helper('execve("/bin/ls", ["ls"], [/* 41 vars */]) = 0',
            'execve', ['"/bin/ls"', ['"ls"'], ['/* 41 vars */']], '0')

    def test_lists(self):
        self.helper('execve([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) = 0',
            'execve', [[['1','2','3'],['4','5','6'],['7','8','9']]], '0')

    def test_poll(self):
        self.helper(r'poll([{fd=5, events=POLLIN}, {fd=4, events=POLLIN}, {fd=7, events=POLLIN|POLLPRI}, {fd=10, events=POLLIN}, {fd=9, events=POLLIN|POLLPRI}, {fd=26, '
            +r'events=POLLIN}, {fd=22, events=POLLIN}, {fd=23, events=POLLIN}], 8, -1) = 1 ([{fd=23, revents=POLLIN}])',
            'poll',[[{'events': 'POLLIN', 'fd': '5'},{'events': 'POLLIN', 'fd': '4'},
            {'events': 'POLLIN|POLLPRI', 'fd': '7'},{'events': 'POLLIN', 'fd': '10'},
            {'events': 'POLLIN|POLLPRI', 'fd': '9'},{'events': 'POLLIN', 'fd': '26'},
            {'events': 'POLLIN', 'fd': '22'},{'events': 'POLLIN', 'fd': '23'}],
            '8','-1'],
            '1 ([{fd=23, revents=POLLIN}])')

if __name__ == '__main__':
    unittest.main()

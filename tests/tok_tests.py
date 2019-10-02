"""

Tests for module `tokenizer`.

"""


import unittest
from tokenizer import Token, Tokenizer


class TokenizerTests(unittest.TestCase):

    def test_unexpected_type(self):
        """Object that is not a string."""
        t = Tokenizer()
        with self.assertRaises(TypeError):
            t.tokenize([])

    def test_empty_string(self):
        """Empty string."""
        t = Tokenizer()
        a = t.a_tokenize('')
        ad = t.ad_tokenize('')
        it = list(t.i_tokenize(''))
        tt = t.tokenize('')
        ref = []
        self.assertEqual(a, ref)
        self.assertEqual(ad, ref)
        self.assertEqual(it, ref)
        self.assertEqual(tt, ref)

    def test_type_id(self):
        """Type identifier."""
        t = Tokenizer()
        self.assertEqual(t.type_id('A'), 'alpha')
        self.assertEqual(t.type_id('7'), 'digit')
        self.assertEqual(t.type_id(' '), 'space')
        self.assertEqual(t.type_id('?'), 'punct')
        self.assertEqual(t.type_id('~'), 'other')

    def test_symbol(self):
        """One symbol."""
        t = Tokenizer()
        a = t.a_tokenize('d')
        ad = t.ad_tokenize('d')
        it = list(t.i_tokenize('d'))
        tt = t.tokenize('d')
        ref = [Token(0, 1, 'd', 'alpha')]
        self.assertEqual(a, ref)
        self.assertEqual(ad, ref)
        self.assertEqual(it, ref)
        self.assertEqual(tt, ref)

    def test_singletok(self):
        """A single token."""
        t = Tokenizer()
        res = t.tokenize('fika')
        self.assertIsInstance(res[0], Token)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].start, 0)
        self.assertEqual(res[0].end, 4)
        self.assertEqual(res[0].string, 'fika')
        self.assertEqual(res[0].type, 'alpha')
        self.assertEqual(res[0].length, 4)
        self.assertEqual(res[0].token, 'fika')

    def test_singletok_alph(self):
        """A single alpha token."""
        t = Tokenizer()
        res = t.a_tokenize('fika')
        self.assertIsInstance(res[0], Token)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].start, 0)
        self.assertEqual(res[0].end, 4)
        self.assertEqual(res[0].string, 'fika')
        self.assertEqual(res[0].type, 'alpha')
        self.assertEqual(res[0].length, 4)
        self.assertEqual(res[0].token, 'fika')

    def test_singletok_nonalp(self):
        """A single non-alphabetic token."""
        t = Tokenizer()
        res = t.a_tokenize('_')
        self.assertEqual(res, [])

    def test_alph_toks(self):
        """String starts and ends with an alphabetic symbol."""
        t = Tokenizer()
        res = t.a_tokenize('eesti kiiking')
        self.assertEqual(len(res), 2)
        self.assertIsInstance(res[0], Token)
        self.assertIsInstance(res[1], Token)
        self.assertEqual(res[0].token, 'eesti')
        self.assertEqual(res[1].token, 'kiiking')
        self.assertEqual(res[0].start, 0)
        self.assertEqual(res[1].start, 6)
        self.assertEqual(res[0].end, 5)
        self.assertEqual(res[1].end, 13)
        self.assertEqual(res[0].type, 'alpha')
        self.assertEqual(res[1].type, 'alpha')

    def test_nonalph_toks(self):
        """String starts and ends with a non-alphabetic symbol."""
        t = Tokenizer()
        res = t.a_tokenize(' eesti kiiking ')
        self.assertEqual(len(res), 2)
        self.assertIsInstance(res[0], Token)
        self.assertIsInstance(res[1], Token)
        self.assertEqual(res[0].token, 'eesti')
        self.assertEqual(res[1].token, 'kiiking')
        self.assertEqual(res[0].start, 1)
        self.assertEqual(res[1].start, 7)
        self.assertEqual(res[0].end, 6)
        self.assertEqual(res[1].end, 14)
        self.assertEqual(res[0].type, 'alpha')
        self.assertEqual(res[1].type, 'alpha')

    def test_singletok_dig(self):
        """A single digit token."""
        t = Tokenizer()
        res = t.ad_tokenize('2019')
        self.assertIsInstance(res[0], Token)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].start, 0)
        self.assertEqual(res[0].end, 4)
        self.assertEqual(res[0].string, '2019')
        self.assertEqual(res[0].type, 'digit')
        self.assertEqual(res[0].length, 4)
        self.assertEqual(res[0].token, '2019')

    def test_alph_dig_toks(self):
        """Alphabetical and digital tokens."""
        t = Tokenizer()
        res = t.ad_tokenize('October 3rd, 2019')
        self.assertEqual(len(res), 4)
        self.assertIsInstance(res[0], Token)
        self.assertIsInstance(res[1], Token)
        self.assertIsInstance(res[2], Token)
        self.assertIsInstance(res[3], Token)
        self.assertEqual(res[0].token, 'October')
        self.assertEqual(res[1].token, '3')
        self.assertEqual(res[2].token, 'rd')
        self.assertEqual(res[3].token, '2019')
        self.assertEqual(res[0].type, 'alpha')
        self.assertEqual(res[1].type, 'digit')
        self.assertEqual(res[2].type, 'alpha')
        self.assertEqual(res[3].type, 'digit')

    def test_alph_space_toks(self):
        """Letter spacing for the general tokenizer."""
        t = Tokenizer()
        res = t.tokenize('s i l v a')
        self.assertEqual(len(res), 9)
        self.assertEqual(res[-1].token, 'a')
        self.assertEqual(res[-2].token, ' ')
        self.assertEqual(res[-1].type, 'alpha')
        self.assertEqual(res[-2].type, 'space')

    def test_all_toks(self):
        """All tokens of a string are identified."""
        t = Tokenizer()
        res = t.tokenize('~  0  ~ мама мыла раму...')
        self.assertEqual(len(res), 12)
        self.assertEqual(res[0].token, '~')
        self.assertEqual(res[1].token, '  ')
        self.assertEqual(res[2].token, '0')
        self.assertEqual(res[3].token, '  ')
        self.assertEqual(res[4].token, '~')
        self.assertEqual(res[5].token, ' ')
        self.assertEqual(res[6].token, 'мама')
        self.assertEqual(res[7].token, ' ')
        self.assertEqual(res[8].token, 'мыла')
        self.assertEqual(res[9].token, ' ')
        self.assertEqual(res[10].token, 'раму')
        self.assertEqual(res[11].token, '...')
        self.assertEqual(res[0].type, 'other')
        self.assertEqual(res[1].type, 'space')
        self.assertEqual(res[2].type, 'digit')
        self.assertEqual(res[6].type, 'alpha')
        self.assertEqual(res[11].type, 'punct')
        self.assertEqual(res[0].string, '~  0  ~ мама мыла раму...')
        self.assertNotEqual(res[1].length, res[5].length)
        self.assertEqual(res[2].start, 3)
        self.assertEqual(res[2].end, 4)


if __name__ == '__main__':
    unittest.main()

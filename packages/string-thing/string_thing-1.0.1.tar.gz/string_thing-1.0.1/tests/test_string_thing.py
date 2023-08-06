import unittest
from string_thing import StringThing

class TestStringThing(unittest.TestCase):
    my_string = 'This is my string'

    def test_default_pattern(self):
        my_string_thing = StringThing()
        encoded = my_string_thing.encode(self.my_string)

        self.assertEqual(encoded, 'ZN!TJ!TJIuHOJSUT!')

    def test_split_halves(self):
        my_string_thing = StringThing(['split-halves'])
        encoded = my_string_thing.encode(self.my_string)

        self.assertEqual(encoded, 'y stringThis is m')

    def test_reverse(self):
        my_string_thing = StringThing(['reverse'])
        encoded = my_string_thing.encode(self.my_string)

        self.assertEqual(encoded, 'gnirts ym si sihT')

    def test_shift(self):
        my_string_thing = StringThing(['shift'])
        encoded = my_string_thing.encode(self.my_string)

        self.assertEqual(encoded, 'Uijt!jt!nz!tusjoh')

    def test_swap_case(self):
        my_string_thing = StringThing(['swap-case'])
        encoded = my_string_thing.encode(self.my_string)

        self.assertEqual(encoded, 'tHIS IS MY STRING')

    def test_rotate(self):
        my_string_thing = StringThing(['rotate'])
        encoded = my_string_thing.encode(self.my_string)

        self.assertEqual(encoded, 'gThis is my strin')

    def test_shift_shift(self):
        my_string_thing = StringThing(['shift', 'shift'])
        encoded = my_string_thing.encode(self.my_string)

        self.assertEqual(encoded, 'Vjku"ku"o{"uvtkpi')

    def test_rotate_rotate(self):
        my_string_thing = StringThing(['rotate', 'rotate'])
        encoded = my_string_thing.encode(self.my_string)

        self.assertEqual(encoded, 'ngThis is my stri')

    def test_rotate_split_halves_shift_reverse_shift_swap_case_rotate(self):
        my_string_thing = StringThing(['shift', 'split-halves', 'shift', 'reverse', 'shift', 'swap-case', 'rotate'])
        encoded = my_string_thing.encode(self.my_string)

        self.assertEqual(encoded, '|P#VL#VLKwJQLUWV#')

    # Errors

    def test_split_halves_split_halves(self):
        with self.assertRaises(Exception) as context:
            StringThing(['split-halves', 'split-halves'])

    def test_reverse_reverse(self):
        with self.assertRaises(Exception) as context:
            StringThing(['split-reverse', 'reverse-halves'])

    def test_shift_95_times_plus(self):
        with self.assertRaises(Exception) as context:
            StringThing(['shift'] * 95)

    def test_swap_case_swap_case(self):
        with self.assertRaises(Exception) as context:
            StringThing(['swap-case', 'swap-case'])

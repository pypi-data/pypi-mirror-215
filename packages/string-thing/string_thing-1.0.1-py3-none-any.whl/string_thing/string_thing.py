from functools import reduce

class StringThing:
    def __init__(self, pattern = ['split-halves', 'reverse', 'shift', 'swap-case', 'rotate']):
        patternOpMap = {
            'split-halves': '0',
            'reverse': '1',
            'shift': '2',
            'swap-case': '3',
            'rotate': '4',
        }

        patternString = ''.join(list(map(lambda op: patternOpMap[op], pattern)))

        for error in self.__errorChecks():
            if error['match'] in patternString:
                raise Exception('Error: {}'.format(error['description']))

        self.opFunctionMap = self.__opFunctionMap()
        self.pattern = pattern

    def encode(self, text):
        return reduce(lambda newText, op: self.opFunctionMap[op](newText, False) if op in self.opFunctionMap else newText, self.pattern, text)

    def decode(self, text):
        return reduce(lambda newText, op: self.opFunctionMap[op](newText, True) if op in self.opFunctionMap else newText, self.pattern, text)

    def __opFunctionMap(self):
        return {
            'split-halves': lambda text, decode = False: text[len(text) // 2 if decode else -(-len(text) // 2):] + text[:len(text) // 2 if decode else -(-len(text) // 2)],
            'reverse': lambda text, _: text[::-1],
            'shift': lambda text, decode = False: self.__shift(text, -1 if decode else 1),
            'swap-case': lambda text, _: ''.join(c.lower() if c.isupper() else c.upper() for c in text),
            'rotate': lambda text, decode = False: text[1:] + text[0] if decode else text[-1] + text[:-1],
        }

    def __shift(self, text, shift = 1):
        chars = [chr(i) for i in range(32, 127)]

        chars_max_index = len(chars) - 1

        result = []

        for char in text:
            index = chars.index(char) if char in chars else None

            if index is not None:
                new_index = index + shift

                if new_index > chars_max_index:
                    result.append(chars[new_index - chars_max_index - 1])
                elif new_index < 0:
                    result.append(chars[chars_max_index + new_index + 1])
                else:
                    result.append(chars[new_index])
            else:
                result.append(char)

        return ''.join(result)

    def __errorChecks(self):
        return [
			{
				'description': "Using 'split-halves' back-to-back results in the original string",
				'match': '00',
			},
			{
				'description': "Using 'reverse' back-to-back results in the original string",
				'match': '11',
			},
			{
				'description': "Using 'shift' 95 times results in the original string. Using 'shift' more than 95 times is the same as using using it X - 95 times.",
				'match': '2' * 95,
			},
			{
				'description': "Using 'swap-case' back-to-back results in the original string",
				'match': '33',
			},
		]

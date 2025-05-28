import unittest

def is_satisfactory(original, received):
    if len(original) != len(received):
        return False

    diff = []
    for i in range(len(original)):
        if original[i] != received[i]:
            diff.append(i)
            if len(diff) > 2:
                return False

    if not diff:
        return True
    if len(diff) == 2 and diff[1] == diff[0] + 1:
        i, j = diff
        return original[i] == received[j] and original[j] == received[i]
    return False

def main():
    original = input().strip()
    received = input().strip()
    
    result = is_satisfactory(original, received)
    
    print("YES" if result else "NO")


class TestSatisfactoryChannel(unittest.TestCase):
    def test_example1(self):
        original = "0001010"
        received = "0010010"
        self.assertTrue(is_satisfactory(original, received))

    def test_example2(self):
        original = "0001010"
        received = "0010101"
        self.assertFalse(is_satisfactory(original, received))

    def test_example3(self):
        original = "0001010"
        received = "0001010"
        self.assertTrue(is_satisfactory(original, received))

    def test_example4(self):
        original = "0"
        received = "0"
        self.assertTrue(is_satisfactory(original, received))
    
    def test_example5(self):
        original = "01"
        received = "10"
        self.assertTrue(is_satisfactory(original, received))

    def test_example6(self):
        original = "01"
        received = "01"
        self.assertTrue(is_satisfactory(original, received))

    def test_example7(self):
        original = "010"
        received = "100"
        self.assertTrue(is_satisfactory(original, received))

    def test_example8(self):
        original = "010"
        received = "001"
        self.assertTrue(is_satisfactory(original, received))

    def test_example9(self):
        original = "0101"
        received = "1010"
        self.assertFalse(is_satisfactory(original, received))

    def test_example10(self):
        original = "0101"
        received = "0110"
        self.assertTrue(is_satisfactory(original, received))

    def test_example11(self):
        original = "0001"
        received = "1000"
        self.assertFalse(is_satisfactory(original, received))

if __name__ == "__main__":
    # Run tests by default
    unittest.main()
    
    # To run the actual program, comment out the line above and uncomment the line below
    # main()

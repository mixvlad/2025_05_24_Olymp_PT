def solution(input_data: str) -> int:
    a, b = map(int, input_data.split())
    return b * (2 * a + b - 1)

def main():
    result = solution(input())
    print(result)

def run_tests():
    test_cases = [
        {
            "input": "1 2",
            "expected": 6,
            "name": "Example 1"
        },
        {
            "input": "5 0",
            "expected": 0,
            "name": "Example 2"
        },
        {
            "input": "0 5",
            "expected": 20,
            "name": "Zero start"
        },
        {
            "input": "1 5",
            "expected": 35,
            "name": "Sum from 1 to 5"
        },
        {
            "input": "2 3",
            "expected": 24,
            "name": "Sum from 2 to 4"
        },
        {
            "input": "10 4",
            "expected": 92,
            "name": "Larger start"
        },
        {
            "input": "1 10",
            "expected": 110,
            "name": "Sum from 1 to 10"
        },
        {
            "input": "100 5",
            "expected": 520,
            "name": "Large start with small range"
        }
    ]

    for tc in test_cases:
        result = solution(tc["input"])
        status = "✓" if result == tc["expected"] else "✗"
        print(f"{status} {tc['name']}")
        print(f"  Input: {tc['input']}")
        print(f"  Expected: {tc['expected']}")
        print(f"  Got: {result}\n")

if __name__ == "__main__":
    run_tests()
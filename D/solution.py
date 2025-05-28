def solution(n, deadlines) -> str:
    tasks = [(deadlines[i], i) for i in range(n)]
    
    tasks.sort()
    
    result = [0] * n
    for i, (_, task_idx) in enumerate(tasks):
        result[task_idx] = i + 1
    
    return ' '.join(map(str, result))

def main():
    n = int(input())
    deadlines = list(map(int, input().split()))
    
    result = solution(n, deadlines)
    print(result)

def run_tests():
    test_cases = [
        {
            "n": 3,
            "deadlines": [2, 3, 1],
            "expected": "2 3 1",
            "name": "Example 1"
        },
        {
            "n": 4,
            "deadlines": [2, 1, 2, 1],
            "expected": "4 1 3 2",
            "name": "Example 2"
        },
        {
            "n": 1,
            "deadlines": [1],
            "expected": "1",
            "name": "Single task"
        },
        {
            "n": 2,
            "deadlines": [1, 1],
            "expected": "1 2",
            "name": "Two tasks with same deadline"
        },
        {
            "n": 3,
            "deadlines": [1, 1, 1],
            "expected": "1 2 3",
            "name": "Three tasks with same deadline"
        }
    ]

    for tc in test_cases:
        result = solution(tc["n"], tc["deadlines"])
        status = "✓" if result == tc["expected"] else "✗"
        print(f"{status} {tc['name']}")
        print(f"  Input: n={tc['n']}, deadlines={tc['deadlines']}")
        print(f"  Expected: {tc['expected']}")
        print(f"  Got: {result}\n")

if __name__ == "__main__":
    run_tests()
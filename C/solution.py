def solution(n, m, vert_streets, hor_streets) -> int:
    if len(vert_streets) == 0 and len(hor_streets) == 0:
        return min(n, m)

    vert_streets.sort()
    hor_streets.sort()
    
    vert_streets = [0] + vert_streets + [n]
    hor_streets = [0] + hor_streets + [m]
    
    max_vert_gap = 0
    for i in range(1, len(vert_streets)):
        gap = vert_streets[i] - vert_streets[i-1]
        max_vert_gap = max(max_vert_gap, gap)
    
    max_hor_gap = 0
    for i in range(1, len(hor_streets)):
        gap = hor_streets[i] - hor_streets[i-1]
        max_hor_gap = max(max_hor_gap, gap)
    
    return min(max_vert_gap, max_hor_gap)

def main():
    n, m = map(int, input().split())
    
    # vertical streets
    vert = int(input())
    vert_streets_input = input()
    vert_streets = list(map(int, vert_streets_input.split())) if vert > 0 else []
    
    # horizontal streets
    hor = int(input())
    hor_streets_input = input()
    hor_streets = list(map(int, hor_streets_input.split())) if hor > 0 else []
    
    result = solution(n, m, vert_streets, hor_streets)
    print(result)

def run_tests():
    test_cases = [
        {
            "n": 10,
            "m": 10,
            "vert_streets": [3],
            "hor_streets": [5],
            "expected": 5,
            "name": "Example 1"
        },
        {
            "n": 4,
            "m": 7,
            "vert_streets": [],
            "hor_streets": [],
            "expected": 4,
            "name": "Example 2"
        },
        {
            "n": 5,
            "m": 7,
            "vert_streets": [5, 0],
            "hor_streets": [3, 1, 2],
            "expected": 4,
            "name": "Example 3"
        },
        {
            "n": 100,
            "m": 100,
            "vert_streets": [25, 50, 75],
            "hor_streets": [25, 50, 75],
            "expected": 25,
            "name": "Grid with equal spacing"
        },
        {
            "n": 1000,
            "m": 1000,
            "vert_streets": [100, 200, 300, 400, 500, 600, 700, 800, 900],
            "hor_streets": [100, 200, 300, 400, 500, 600, 700, 800, 900],
            "expected": 100,
            "name": "Large grid with equal spacing"
        }
    ]

    for tc in test_cases:
        result = solution(tc["n"], tc["m"], tc["vert_streets"], tc["hor_streets"])
        status = "✓" if result == tc["expected"] else "✗"
        print(f"{status} {tc['name']}")
        print(f"  Input: n={tc['n']}, m={tc['m']}")
        print(f"  Vertical streets: {tc['vert_streets']}")
        print(f"  Horizontal streets: {tc['hor_streets']}")
        print(f"  Expected: {tc['expected']}")
        print(f"  Got: {result}\n")

if __name__ == "__main__":
    run_tests()

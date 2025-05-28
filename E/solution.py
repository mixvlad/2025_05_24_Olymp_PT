def solution(n, m, used) -> str:
    if m > n:
        return ' '.join(['1'] * n + ['0'] * (m - n))
    if m == n:
        return ' '.join(['1'] * n)
    
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + used[i]
    
    weighted_prefix = [0] * (n + 1)
    for i in range(n):
        weighted_prefix[i + 1] = weighted_prefix[i] + used[i] * (i + 1)
    
    dp = [[float('inf')] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = 0
    
    for i in range(1, n + 1):
        for j in range(1, min(i + 1, m + 1)):
            for k in range(1, i + 1):
                start = i - k
                end = i
                segment_sum = (weighted_prefix[end] - weighted_prefix[start]) - start * (prefix[end] - prefix[start])
                dp[i][j] = min(dp[i][j], dp[i - k][j - 1] + segment_sum)
    
    result = [0] * m
    i, j = n, m
    while j > 0:
        for k in range(1, i + 1):
            start = i - k
            end = i
            segment_sum = (weighted_prefix[end] - weighted_prefix[start]) - start * (prefix[end] - prefix[start])
            if dp[i][j] == dp[i - k][j - 1] + segment_sum:
                result[j - 1] = k
                i -= k
                j -= 1
                break
    
    return ' '.join(map(str, result))

def main():
    n, m = map(int, input().split())
    used = list(map(int, input().split()))
    result = solution(n, m, used)
    print(result)

def run_tests():
    import time
    
    test_cases = [
        {
            "input": "5 3\n1 3 5 1 1",
            "expected": "1 1 3",
            "name": "Example 1"
        },
        {
            "input": "2 2\n1 1",
            "expected": "1 1",
            "name": "Example 2"
        },
        {
            "input": "3 1\n1 1 1",
            "expected": "3",
            "name": "Example 3"
        },
        {
            "input": "4 2\n2 1 1 2",
            "expected": "2 2",
            "name": "Test 4: Even split"
        },
        {
            "input": "5 2\n1 2 3 2 1",
            "expected": "2 3",
            "name": "Test 5: Symmetric array"
        },
        {
            "input": "3 3\n1 1 1",
            "expected": "1 1 1",
            "name": "Test 6: Equal segments"
        },
        {
            "input": "4 1\n1 2 3 4",
            "expected": "4",
            "name": "Test 7: Single segment"
        },
        {
            "input": "5 4\n1 1 1 1 1",
            "expected": "1 1 1 2",
            "name": "Test 8: Equal elements"
        },
        {
            "input": "3 2\n2 1 2",
            "expected": "1 2",
            "name": "Test 9: Middle minimum"
        },
        {
            "input": "4 3\n1 2 1 2",
            "expected": "1 1 2",
            "name": "Test 10: Alternating values"
        },
        {
            "input": "5 5\n5 4 3 2 1",
            "expected": "1 1 1 1 1",
            "name": "Test 11: Decreasing sequence"
        },
        {
            "input": "5 3\n5 1 5 1 5",
            "expected": "1 1 3",
            "name": "Test 12: Alternating peaks"
        },
        {
            "input": "5 2\n5 4 3 4 5",
            "expected": "2 3",
            "name": "Test 13: Valley pattern"
        },
        {
            "input": "5 5\n1 2 3 4 5",
            "expected": "1 1 1 1 1",
            "name": "Test 14: Increasing sequence"
        },
        {
            "input": "1 5\n5",
            "expected": "0 0 0 0 0",
            "name": "Test 15: More buttons than emojis"
        }
    ]

    for tc in test_cases:
        lines = tc["input"].strip().split('\n')
        n, m = map(int, lines[0].split())
        used = list(map(int, lines[1].split()))
        
        start_time = time.time()
        result = solution(n, m, used)
        end_time = time.time()
        execution_time = end_time - start_time
        
        status = "✓" if result == tc["expected"] else "✗"
        print(f"{status} {tc['name']}")
        print(f"  Input:\n{tc['input']}")
        print(f"  Expected: {tc['expected']}")
        print(f"  Got: {result}")
        print(f"  Time: {execution_time:.3f} seconds\n")

if __name__ == "__main__":
    run_tests()
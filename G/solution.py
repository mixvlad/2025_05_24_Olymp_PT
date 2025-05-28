def read_transaction():
    """Read a single transaction's data from input."""
    r_i, w_i = map(int, input().split())
    read_set = list(map(int, input().split()))
    write_set = list(map(int, input().split()))
    return read_set, write_set

def has_conflict(transactions, i, j):
    """
    Check if there's a conflict between transactions i and j.
    A conflict occurs if transaction i writes to a location that j reads from.
    """
    write_set_i = transactions[i][1]  # Write set of transaction i
    read_set_j = transactions[j][0]   # Read set of transaction j
    
    # Check if any location in write_set_i is in read_set_j
    return any(loc in read_set_j for loc in write_set_i)

def solve():
    # Read input
    n, m = map(int, input().split())
    
    # Read all transactions
    transactions = []
    for _ in range(n):
        read_set, write_set = read_transaction()
        transactions.append((read_set, write_set))
    
    # Try to build the longest sequence
    result = []
    used = [False] * n
    
    # Try each transaction as a starting point
    for start in range(n):
        if used[start]:
            continue
            
        # Start a new sequence
        current_sequence = [start + 1]  # +1 because transactions are 1-indexed
        used[start] = True
        
        # Try to extend the sequence
        while True:
            found_next = False
            for i in range(n):
                if used[i]:
                    continue
                    
                # Check if we can add this transaction
                can_add = True
                for prev in current_sequence:
                    if has_conflict(transactions, prev - 1, i):
                        can_add = False
                        break
                
                if can_add:
                    current_sequence.append(i + 1)
                    used[i] = True
                    found_next = True
                    break
            
            if not found_next:
                break
        
        # Update result if we found a longer sequence
        if len(current_sequence) > len(result):
            result = current_sequence
    
    # Output result
    print(len(result))
    print(*result)

if __name__ == "__main__":
    solve()

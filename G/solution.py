import time
import sys
from io import StringIO
from collections import defaultdict

def read_transaction():
    """Read a single transaction's data from input."""
    r_i, w_i = map(int, input().split())
    read_set = list(map(int, input().split()))
    write_set = list(map(int, input().split()))
    return read_set, write_set

def solve():
    start_time = time.time()
    # Read input
    n, m = map(int, input().split())
    
    # Read all transactions
    transactions = []
    for _ in range(n):
        read_set, write_set = read_transaction()
        transactions.append((set(read_set), set(write_set)))
    
    # Initialize data structures
    result = []
    used = [False] * n
    corrupted_cells = set()  # Track corrupted cells
    
    # Precompute which transactions read from each cell
    cell_to_readers = defaultdict(set)
    for i, (read_set, _) in enumerate(transactions):
        for cell in read_set:
            cell_to_readers[cell].add(i)
    
    # Precompute initial corruption impact for each transaction
    corruption_impact = [0] * n
    for i, (_, write_set) in enumerate(transactions):
        for cell in write_set:
            corruption_impact[i] += len(cell_to_readers[cell]) - 1  # -1 because we don't count self
    
    # Try to build the longest sequence
    available_transactions = set(range(n))
    
    while available_transactions:
        if time.time() - start_time > 3.8:
            break
            
        # Find the best transaction to add
        best_transaction = None
        best_score = (-1, float('inf'))  # (available_reads, corruption_impact)
        
        for i in available_transactions:
            read_set, write_set = transactions[i]
            
            # Check if this transaction can be executed (no reads from corrupted cells)
            if read_set & corrupted_cells:  # Intersection check - faster than loop
                continue
                
            # Calculate score for this transaction
            available_reads = len(read_set - corrupted_cells)
            current_corruption = corruption_impact[i]
            
            score = (available_reads, -current_corruption)  # Higher reads, lower corruption impact
            if score > best_score:
                best_score = score
                best_transaction = i
        
        if best_transaction is None:
            break
            
        # Add the best transaction
        result.append(best_transaction + 1)
        used[best_transaction] = True
        available_transactions.remove(best_transaction)
        
        # Update corrupted cells and corruption impacts
        _, write_set = transactions[best_transaction]
        newly_corrupted = write_set - corrupted_cells
        corrupted_cells.update(write_set)
        
        # Update corruption impacts for remaining transactions
        for cell in newly_corrupted:
            for reader_idx in cell_to_readers[cell]:
                if reader_idx in available_transactions:
                    corruption_impact[reader_idx] -= 1
        
        # Remove transactions that can no longer be executed
        to_remove = set()
        for i in available_transactions:
            read_set, _ = transactions[i]
            if read_set & corrupted_cells:
                to_remove.add(i)
        available_transactions -= to_remove
    
    # Output result
    print(len(result))
    print(*result)

def test_solution():
    """Run test with example input data."""
    try:
        test_input = """3 3
1 1
1
2
1 1
2
3
1 1
3
1"""
        
        expected_output = """2
1 3"""
        
        print("Starting test...", flush=True)
        
        # Save original stdin and stdout
        original_stdin = sys.stdin
        original_stdout = sys.stdout
        
        try:
            # Redirect stdin and stdout
            sys.stdin = StringIO(test_input)
            output_buffer = StringIO()
            sys.stdout = output_buffer
            
            # Run solution
            print("Running solution...", file=original_stdout, flush=True)
            solve()
            
            # Get output
            output = output_buffer.getvalue().strip()
            
            # Print test results
            print("\nTest Results:", file=original_stdout, flush=True)
            print("Input:", file=original_stdout, flush=True)
            print(test_input, file=original_stdout, flush=True)
            print("\nOutput:", file=original_stdout, flush=True)
            print(output, file=original_stdout, flush=True)
            print("\nExpected:", file=original_stdout, flush=True)
            print(expected_output, file=original_stdout, flush=True)
            print("\nTest Status:", "PASSED" if output == expected_output else "FAILED", file=original_stdout, flush=True)
            
        finally:
            # Restore original stdin and stdout
            sys.stdin = original_stdin
            sys.stdout = original_stdout
            
    except Exception as e:
        print(f"Error during test execution: {str(e)}", file=original_stdout, flush=True)
        import traceback
        traceback.print_exc(file=original_stdout)

if __name__ == "__main__":
    try:
        if len(sys.argv) > 1 and sys.argv[1] == "--run":
            print("Running in interactive mode...", flush=True)
            solve()
        else:
            print("Running in test mode...", flush=True)
            test_solution()
    except Exception as e:
        print(f"Error in main execution: {str(e)}", flush=True)
        import traceback
        traceback.print_exc()

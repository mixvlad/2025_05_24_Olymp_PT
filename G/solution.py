import time
import sys
from io import StringIO
from collections import defaultdict
import random

# Time limits in seconds
SWITCH_TO_SIMPLE_TIME = 2.5  # Switch to simple algorithm after this time
SWITCH_TO_ULTRA_FAST_TIME = 3.2  # Switch to ultra-fast algorithm after this time
MAX_EXECUTION_TIME = 3.9     # Maximum execution time before stopping

# Performance thresholds
MEDIUM_DATASET_THRESHOLD = 400  # Use complex algorithm if n <= this
LARGE_DATASET_THRESHOLD = 1000  # Consider dataset large if n > this
HUGE_DATASET_THRESHOLD = 5000   # Consider dataset huge if n > this

def read_transaction():
    """Read a single transaction's data from input."""
    r_i, w_i = map(int, input().split())
    read_set = list(map(int, input().split()))
    write_set = list(map(int, input().split()))
    return read_set, write_set

def solve_with_multiple_starts(transactions, start_time, max_attempts=2):
    """Try multiple starting strategies and return the best result."""
    best_result = []
    n = len(transactions)
    
    for attempt in range(max_attempts):
        if time.time() - start_time > MAX_EXECUTION_TIME - 1.0:
            break
            
        # Different starting strategies
        if attempt == 0:
            # Strategy 1: Sort by simple read/write ratio
            ratios = [(len(transactions[i][0]) / max(len(transactions[i][1]), 1), i) 
                     for i in range(n)]
            ratios.sort(reverse=True)
            order = [i for _, i in ratios]
        else:
            # Strategy 2: Sort by write set size (ascending)
            write_sizes = [(len(transactions[i][1]), i) for i in range(n)]
            write_sizes.sort()
            order = [i for _, i in write_sizes]
        
        # Try greedy with this order
        result = solve_greedy_with_order(transactions, order, start_time)
        
        if len(result) > len(best_result):
            best_result = result
    
    return best_result

def solve_greedy_with_order(transactions, order, start_time):
    """Solve greedily following the given order of transaction preferences."""
    result = []
    used = set()
    corrupted_cells = set()
    
    for i in order:
        if time.time() - start_time > MAX_EXECUTION_TIME:
            break
            
        if i in used:
            continue
            
        read_set, write_set = transactions[i]
        
        # Check if this transaction can be executed
        if read_set & corrupted_cells:
            continue
            
        # Add the transaction
        result.append(i + 1)
        used.add(i)
        
        # Update corrupted cells
        corrupted_cells.update(write_set)
    
    return result

def try_additional_improvements(transactions, initial_result, start_time):
    """Try additional optimization strategies if time permits."""
    best_result = initial_result[:]
    n = len(transactions)
    
    # Determine strategies based on dataset size
    if n <= LARGE_DATASET_THRESHOLD:
        # For small/medium datasets: more comprehensive search
        max_random_attempts = min(10, max(1, int((MAX_EXECUTION_TIME - (time.time() - start_time)) * 5)))
        
        # Strategy 1: Try different random orders
        attempts = 0
        while attempts < max_random_attempts and time.time() - start_time < MAX_EXECUTION_TIME - 0.3:
            order = list(range(n))
            random.shuffle(order)
            
            result = solve_greedy_with_order(transactions, order, start_time)
            if len(result) > len(best_result):
                best_result = result
            
            attempts += 1
        
        # Strategy 2: Try reverse order
        if time.time() - start_time < MAX_EXECUTION_TIME - 0.2:
            reverse_order = list(range(n))
            reverse_order.reverse()
            
            result = solve_greedy_with_order(transactions, reverse_order, start_time)
            if len(result) > len(best_result):
                best_result = result
        
        # Strategy 3: Try sorting by read set size
        if time.time() - start_time < MAX_EXECUTION_TIME - 0.1:
            read_sizes = [(len(transactions[i][0]), i) for i in range(n)]
            read_sizes.sort(reverse=True)
            order = [i for _, i in read_sizes]
            
            result = solve_greedy_with_order(transactions, order, start_time)
            if len(result) > len(best_result):
                best_result = result
    
    else:
        # For large datasets: simpler and faster strategies
        max_attempts = min(3, max(1, int((MAX_EXECUTION_TIME - (time.time() - start_time)) * 2)))
        
        attempts = 0
        while attempts < max_attempts and time.time() - start_time < MAX_EXECUTION_TIME - 0.2:
            if attempts == 0:
                # Strategy 1: Sort by write set size (ascending)
                write_sizes = [(len(transactions[i][1]), i) for i in range(n)]
                write_sizes.sort()
                order = [i for _, i in write_sizes]
            elif attempts == 1:
                # Strategy 2: Sort by read/write ratio (descending)
                ratios = [(len(transactions[i][0]) / max(len(transactions[i][1]), 1), i) for i in range(n)]
                ratios.sort(reverse=True)
                order = [i for _, i in ratios]
            else:
                # Strategy 3: Sort by total size (read + write, ascending)
                total_sizes = [(len(transactions[i][0]) + len(transactions[i][1]), i) for i in range(n)]
                total_sizes.sort()
                order = [i for _, i in total_sizes]
            
            result = solve_greedy_with_order(transactions, order, start_time)
            if len(result) > len(best_result):
                best_result = result
            
            attempts += 1
    
    return best_result

def solve():
    start_time = time.time()
    # Read input
    n, m = map(int, input().split())
    
    # Read all transactions
    transactions = []
    for _ in range(n):
        read_set, write_set = read_transaction()
        transactions.append((set(read_set), set(write_set)))
    
    # For very large datasets, use simplified multi-start approach
    if n > HUGE_DATASET_THRESHOLD:
        result = solve_with_multiple_starts(transactions, start_time, max_attempts=2)
        
        # Try additional improvements if we have time left
        time_left = MAX_EXECUTION_TIME - (time.time() - start_time)
        if time_left > 0.3:
            improved_result = try_additional_improvements(transactions, result, start_time)
            if len(improved_result) > len(result):
                result = improved_result
        
        print(len(result))
        print(*result)
        return
    
    # Initialize data structures
    result = []
    corrupted_cells = set()  # Track corrupted cells
    
    # Determine initial algorithm choice
    initial_algorithm_mode = ""
    if n <= MEDIUM_DATASET_THRESHOLD:
        initial_algorithm_mode = "complex"
    else: # MEDIUM_DATASET_THRESHOLD < n <= HUGE_DATASET_THRESHOLD
        initial_algorithm_mode = "simple"

    # Precompute data if needed
    cell_to_readers = defaultdict(set)
    potential_victims = {}
    
    if initial_algorithm_mode == "complex":
        # Precompute which transactions read from each cell
        for i, (read_set, _) in enumerate(transactions):
            for cell in read_set:
                cell_to_readers[cell].add(i)
        
        # Precompute potential impact for each transaction (approximation)
        for i, (_, write_set) in enumerate(transactions):
            victims = set()
            for cell in write_set:
                victims.update(cell_to_readers[cell])
            victims.discard(i)  # Don't count self
            potential_victims[i] = victims
    
    # Try to build the longest sequence
    available_transactions = set(range(n))
    
    while available_transactions:
        current_time = time.time() - start_time
        
        if current_time > MAX_EXECUTION_TIME:
            break
            
        # Determine effective algorithm mode based on initial choice and time
        effective_algorithm_mode = initial_algorithm_mode
        if current_time > SWITCH_TO_ULTRA_FAST_TIME:
            effective_algorithm_mode = "ultra_fast"
        elif current_time > SWITCH_TO_SIMPLE_TIME:
            if effective_algorithm_mode == "complex": # Downgrade complex to simple
                effective_algorithm_mode = "simple"
            # If it was already simple, it stays simple until ultra_fast kicks in
            
        # Find the best transaction to add
        best_transaction = None
        
        if effective_algorithm_mode == "ultra_fast":
            # Ultra-fast algorithm: simple sampling + basic scoring
            sample_size = min(50, len(available_transactions))
            if len(available_transactions) > sample_size:
                candidates = random.sample(list(available_transactions), sample_size)
            else:
                candidates = list(available_transactions)
            
            best_score = float('inf')
            for i in candidates:
                if time.time() - start_time > MAX_EXECUTION_TIME:
                    break
                read_set, write_set = transactions[i]
                if read_set & corrupted_cells:
                    continue
                score = len(write_set)
                if score < best_score:
                    best_score = score
                    best_transaction = i
                    
        elif effective_algorithm_mode == "simple":
            # Enhanced simple algorithm with better scoring
            best_score = (-1, float('inf'))  # (available_reads, -corruption_count)
            for i in available_transactions:
                if time.time() - start_time > MAX_EXECUTION_TIME:
                    break
                read_set, write_set = transactions[i]
                if read_set & corrupted_cells:
                    continue
                available_reads = len(read_set - corrupted_cells)
                corruption_count = len(write_set - corrupted_cells)
                current_score = (available_reads, -corruption_count)
                if current_score > best_score:
                    best_score = current_score
                    best_transaction = i
        
        elif effective_algorithm_mode == "complex": # And initial_algorithm_mode was "complex"
            # Complex algorithm: use approximation for speed
            best_score = (-1, -1)  # (remaining_transactions_estimate, available_reads)
            for i in available_transactions:
                if time.time() - start_time > MAX_EXECUTION_TIME:
                    break
                read_set, write_set = transactions[i]
                if read_set & corrupted_cells:
                    continue
                affected_transactions = potential_victims[i] & available_transactions
                remaining_estimate = len(available_transactions) - 1 - len(affected_transactions)
                available_reads = len(read_set - corrupted_cells)
                score = (remaining_estimate, available_reads)
                if score > best_score:
                    best_score = score
                    best_transaction = i
        
        if best_transaction is None:
            break
            
        # Add the best transaction
        result.append(best_transaction + 1)
        available_transactions.remove(best_transaction)
        
        # Update corrupted cells
        _, write_set = transactions[best_transaction]
        corrupted_cells.update(write_set)
        
        # Remove transactions that can no longer be executed
        # Check if effective_algorithm_mode is ultra_fast for less frequent cleanup
        is_ultra_fast_now = (effective_algorithm_mode == "ultra_fast")
        if not is_ultra_fast_now or len(result) % 20 == 0:
            to_remove = set()
            for i in available_transactions:
                if time.time() - start_time > MAX_EXECUTION_TIME:
                    break
                read_set, _ = transactions[i]
                if read_set & corrupted_cells:
                    to_remove.add(i)
            available_transactions -= to_remove
    
    # Try additional improvements if we have time left
    time_left = MAX_EXECUTION_TIME - (time.time() - start_time)
    if time_left > 0.3:
        improved_result = try_additional_improvements(transactions, result, start_time)
        if len(improved_result) > len(result):
            result = improved_result
    
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

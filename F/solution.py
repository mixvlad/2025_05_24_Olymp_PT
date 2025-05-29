import re
from typing import List, Tuple
import sys

def parse_html(html: str) -> List[List[Tuple[int, int]]]:
    """
    Parse HTML table and return list of rows, where each row contains tuples of (colspan, rowspan)
    for each cell.
    
    Args:
        html: HTML string containing table markup
        
    Returns:
        List of rows, where each row is a list of (colspan, rowspan) tuples
    """
    # Remove whitespace and newlines for easier parsing
    html = re.sub(r'\s+', ' ', html.strip())
    
    # Find table content between <table> and </table>
    table_match = re.search(r'<table[^>]*>(.*?)</table>', html, re.IGNORECASE | re.DOTALL)
    if not table_match:
        return []
    
    table_content = table_match.group(1)
    
    # Find all rows
    row_pattern = r'<tr[^>]*>(.*?)</tr>'
    row_matches = re.findall(row_pattern, table_content, re.IGNORECASE | re.DOTALL)
    
    rows = []
    for row_content in row_matches:
        # Find all cells in this row
        cell_pattern = r'<td([^>]*?)>(.*?)</td>'
        cell_matches = re.findall(cell_pattern, row_content, re.IGNORECASE | re.DOTALL)
        
        cells = []
        for attributes, content in cell_matches:
            # Parse colspan and rowspan attributes
            colspan = 1
            rowspan = 1
            
            # Extract colspan
            colspan_match = re.search(r'colspan\s*=\s*["\']?(\d+)["\']?', attributes, re.IGNORECASE)
            if colspan_match:
                colspan = int(colspan_match.group(1))
            
            # Extract rowspan
            rowspan_match = re.search(r'rowspan\s*=\s*["\']?(\d+)["\']?', attributes, re.IGNORECASE)
            if rowspan_match:
                rowspan = int(rowspan_match.group(1))
            
            cells.append((colspan, rowspan))
        
        if cells:  # Only add non-empty rows
            rows.append(cells)
    
    return rows

def create_table(rows: List[List[Tuple[int, int]]]) -> List[str]:
    """Create table for complex case with merged cells."""
    # Build logical grid to handle rowspan and colspan
    # First pass: determine grid dimensions and cell placement
    grid = {}  # (row, col) -> (cell_id, is_start, rowspan, colspan)
    cell_id = 0
    
    for row_idx, row in enumerate(rows):
        col_idx = 0
        for colspan, rowspan in row:
            # Find next available column
            while (row_idx, col_idx) in grid:
                col_idx += 1
            
            # Mark all cells occupied by this cell
            for r in range(row_idx, row_idx + rowspan):
                for c in range(col_idx, col_idx + colspan):
                    is_start = (r == row_idx and c == col_idx)
                    grid[(r, c)] = (cell_id, is_start, rowspan, colspan)
            
            cell_id += 1
            col_idx += colspan
    
    # Find grid dimensions
    if not grid:
        return []
    
    max_row = max(r for r, c in grid.keys())
    max_col = max(c for r, c in grid.keys())
    num_rows = max_row + 1
    num_cols = max_col + 1
    
    # Create empty ASCII grid
    ascii_height = 2 * num_rows + 1
    ascii_width = 2 * num_cols + 1
    ascii_grid = [[' ' for _ in range(ascii_width)] for _ in range(ascii_height)]
    
    # Draw cells and their borders
    processed_cells = set()
    
    for (log_r, log_c), (cell_id, is_start, rowspan, colspan) in grid.items():
        if cell_id in processed_cells or not is_start:
            continue
        
        processed_cells.add(cell_id)
        
        # Draw cell borders
        # Top border
        ascii_r = 2 * log_r
        for c in range(colspan + 1):
            ascii_c = 2 * (log_c + c)
            if ascii_grid[ascii_r][ascii_c] != '+':
                ascii_grid[ascii_r][ascii_c] = '-'
            if c < colspan and ascii_grid[ascii_r][ascii_c + 1] != '+':
                ascii_grid[ascii_r][ascii_c + 1] = '-'
            
        ascii_grid[ascii_r][2 * log_c] = '+'
        ascii_grid[ascii_r][2 * (log_c + colspan)] = '+'
        
        # Bottom border
        ascii_r = 2 * (log_r + rowspan)
        for c in range(colspan + 1):
            ascii_c = 2 * (log_c + c)
            if ascii_grid[ascii_r][ascii_c] != '+':
                ascii_grid[ascii_r][ascii_c] = '-'
            if c < colspan and ascii_grid[ascii_r][ascii_c + 1] != '+':
                ascii_grid[ascii_r][ascii_c + 1] = '-'
        ascii_grid[ascii_r][2 * log_c] = '+'
        ascii_grid[ascii_r][2 * (log_c + colspan)] = '+'
        
        # Left and right borders
        for r in range(rowspan):
            ascii_r = 2 * (log_r + r) + 1
            # Left border
            ascii_c = 2 * log_c
            if ascii_grid[ascii_r][ascii_c] != '+':
                ascii_grid[ascii_r][ascii_c] = '|'
            if r < rowspan and ascii_grid[ascii_r + 1][ascii_c] != '+':
                ascii_grid[ascii_r + 1][ascii_c] = '|'
            
            # Right border
            ascii_c = 2 * (log_c + colspan)
            if ascii_grid[ascii_r][ascii_c] != '+':
                ascii_grid[ascii_r][ascii_c] = '|'
            if r < rowspan and ascii_grid[ascii_r + 1][ascii_c] != '+':
                ascii_grid[ascii_r + 1][ascii_c] = '|'
    
    # Convert to strings and remove trailing spaces
    result = []
    for row in ascii_grid:
        line = ''.join(row).rstrip()
        result.append(line)
    
    # Remove empty trailing lines
    while result and not result[-1]:
        result.pop()
    
    return result

def draw_table(html: str) -> str:
    """
    Convert HTML table to ASCII art representation.
    
    Args:
        html: HTML string containing table markup
        
    Returns:
        ASCII art representation of the table
    """
    # Parse HTML table
    rows = parse_html(html)
    
    # Create ASCII structure
    table = create_table(rows)
    
    # Join rows with newlines
    return '\n'.join(table)

if __name__ == "__main__":
    # Пытаемся прочитать из input.txt, если не получится - читаем из стандартного ввода
    try:
        with open('input.txt', 'r') as f:
            html = f.read()
    except FileNotFoundError:
        html = sys.stdin.read()
    
    # Получаем результат
    result = draw_table(html)
    
    # Записываем результат в output.txt
    try:
        with open('output.txt', 'w') as f:
            f.write(result)
    except Exception:
        pass  # Игнорируем ошибки при записи в файл
    
    # Выводим результат в стандартный вывод
    print(result)

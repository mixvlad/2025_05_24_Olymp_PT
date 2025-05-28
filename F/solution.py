import re
from typing import List, Tuple

def parse_html(html: str) -> List[List[Tuple[int, int]]]:
    """
    Parse HTML table and return list of rows, where each row contains tuples of (colspan, rowspan)
    for each cell.
    
    Args:
        html: HTML string containing table markup
        
    Returns:
        List of rows, where each row is a list of (colspan, rowspan) tuples
    """
    pass

def create_table_structure(rows: List[List[Tuple[int, int]]]) -> List[List[str]]:
    """
    Create ASCII table structure based on parsed HTML data.
    
    Args:
        rows: List of rows with (colspan, rowspan) tuples
        
    Returns:
        List of strings representing ASCII table structure
    """
    pass

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
    table = create_table_structure(rows)
    
    # Join rows with newlines
    return '\n'.join(table)

def test_simple_table():
    html = """<table>
<TR><td>1</td><td>2</td></TR>
<TR><td>3</td></TR>
<TR><td>4</td><td>5</td><td>6</td></TR>
</table>"""
    expected = """+-+-+
| | |
+-+-+
| |  
+-+-+-+
| | | |
+-+-+-+"""
    assert draw_table(html) == expected

def test_complex_table():
    html = """<table>
<tr>
<td colspan="3">1</td>
<td rowspan="2" colspan="2">2</td>
</tr>
<tr>
<td colspan="2">3</td>
<td>4</td>
<td rowspan="2">5</td>
</tr>
<tr>
<td>6</td>
</tr>
<tr>
<td>7</td>
</tr>
<tr>
<td rowspan="2">8</td>
<td rowspan="2">9</td>
</tr>
<tr>
<td colspan="2" rowspan="2">0</td>
</tr>
</table>"""
    expected = """+-----+---+
|     |   |
+---+-+   +-+
|   | |   | |
+-+-+-+---+ |
| |       | |
+-+       +-+
| |          
+-+-+
| | |
| | +---+
| | |   |
+-+-+   |
    |   |
    +---+"""
    assert draw_table(html) == expected

if __name__ == "__main__":
    # Читаем входной файл
    with open('input.txt', 'r') as f:
        html = f.read()
    
    # Получаем результат
    result = draw_table(html)
    
    # Записываем в выходной файл
    with open('output.txt', 'w') as f:
        f.write(result)

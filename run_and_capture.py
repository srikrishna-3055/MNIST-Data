import subprocess
import sys
from pathlib import Path

script = Path(__file__).parent / 'main.py'
output_file = Path(__file__).parent / 'run_output.txt'

try:
    proc = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
    out = proc.stdout + proc.stderr
    output_file.write_text(out, encoding='utf-8')
    print(f'WROTE {output_file}')
except Exception as e:
    print('ERROR:', e)

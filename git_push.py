import subprocess
import os
from pathlib import Path

repo_dir = Path(__file__).parent
os.chdir(repo_dir)
output_file = repo_dir / 'git_push_output.txt'

def run(cmd):
    res = subprocess.run(cmd, capture_output=True, text=True)
    return (cmd, res.returncode, res.stdout, res.stderr)

outputs = []

# Check git version
outputs.append(run(['git','--version']))

# Check if .git exists
outputs.append(('check .git', 0, str((repo_dir / '.git').exists()), ''))

if not (repo_dir / '.git').exists():
    outputs.append(run(['git','init']))

outputs.append(run(['git','status','--porcelain','-b']))

# Try to add specific files, fallback to add all
add_res = run(['git','add','run_output.txt','run_and_capture.py'])
if add_res[1] != 0:
    outputs.append(add_res)
    outputs.append(run(['git','add','-A']))
else:
    outputs.append(add_res)

# Commit
commit_res = run(['git','commit','-m','Add run output and helper script'])
outputs.append(commit_res)

# Reset origin if exists
outputs.append(run(['git','remote','remove','origin']))
# Add origin
outputs.append(run(['git','remote','add','origin','https://github.com/srikrishna-3055/MNIST_data.git']))
# Set branch
outputs.append(run(['git','branch','-M','main']))
# Push
outputs.append(run(['git','push','-u','origin','main']))

# Write outputs
with open(output_file, 'w', encoding='utf-8') as f:
    for cmd, code, out, err in outputs:
        f.write('COMMAND: ' + str(cmd) + '\n')
        f.write('RETURN CODE: ' + str(code) + '\n')
        if out:
            f.write('STDOUT:\n' + out + '\n')
        if err:
            f.write('STDERR:\n' + err + '\n')
        f.write('\n' + ('-'*60) + '\n\n')

print('WROTE', output_file)

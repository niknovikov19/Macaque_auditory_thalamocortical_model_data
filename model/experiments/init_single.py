from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent))

from run_exp import run_exp


exp_name = 'exp_20s_LFPpop'

run_exp(exp_name, is_batch=False)


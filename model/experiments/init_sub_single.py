from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent))

from run_subnet_exp import run_exp


exp_name = 'exp_subnet_L3_3s_replay'

run_exp(exp_name, is_batch=False)


from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent))

from run_subnet_exp import run_exp


exp_name = 'exp_subnet_L2_8s_replay_t=0-10'
#exp_name = 'exp_subnet_L3_8s_poiss_t=1-10'

run_exp(exp_name, is_batch=False)

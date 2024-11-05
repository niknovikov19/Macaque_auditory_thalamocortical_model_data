from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent))

from run_subnet_exp_batch import run_exp


run_exp()  # exp_name will be taken from batchtools via cfg.simLabel

import pickle as pkl

fpath = '/ddn/niknovikov19/repo/A1_model_old/data/A1_test_600ms/A1_test_600ms_data.pkl'
with open(fpath, 'rb') as fid: X=pickle.load(fid)

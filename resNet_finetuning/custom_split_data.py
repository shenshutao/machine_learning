import os
import shutil

import numpy as np


def split_data(train_data_dir, test_data_dir, test_precentage):
    if not os.path.exists(test_data_dir):
        os.makedirs(test_data_dir)

    # put all test data back to train data folder
    folders = os.listdir(test_data_dir)
    for fod in folders:
        if not fod.startswith('.'):
            files = os.listdir(test_data_dir + '/' + fod)

            for f in files:
                if not f.startswith('.'):
                    shutil.move(test_data_dir + '/' + fod + '/' + f, train_data_dir + '/' + fod + '/' + f)

    # redo split train / test
    folders = os.listdir(train_data_dir)
    for fod in folders:
        if not fod.startswith('.'):
            files = os.listdir(train_data_dir + '/' + fod)

            if not os.path.exists(test_data_dir + '/' + fod):
                os.makedirs(test_data_dir + '/' + fod)

            for f in files:
                if not f.startswith('.'):
                    if np.random.rand(1) < test_precentage:
                        shutil.move(train_data_dir + '/' + fod + '/' + f, test_data_dir + '/' + fod + '/' + f)

#
# if __name__ == "__main__":
#     os.chdir('/home/users/nus/e0015130/shopee/')
#     split_data('train_all', 'validate_all', 0.3)

import os
import sys
import time

import numpy as np
import scipy as sp

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

from joblib import Parallel, delayed

from pyod.models.iforest import IForest
from pyod.models.lof import LOF
from pyod.models.ocsvm import OCSVM
from pyod.models.pca import PCA
from pyod.models.knn import KNN
from pyod.models.hbos import HBOS
from pyod.models.lscp import LSCP
from pyod.utils.utility import standardizer
from pyod.utils.data import evaluate_print

# suppress warnings
import warnings

warnings.filterwarnings("ignore")

# temporary solution for relative imports in case combo is not installed
# if combo is installed, no need to use the following line
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname("__file__"), '..')))

from suod.models.base import SUOD
from suod.models.parallel_processes import _parallel_fit
from suod.models.parallel_processes import _parallel_predict
from suod.models.parallel_processes import _parallel_decision_function
from suod.models.parallel_processes import _partition_estimators
from suod.utils.utility import _unfold_parallel

if __name__ == "__main__":
    # load files
    mat_file_list = [
        # 'cardio.mat',
        # 'satellite.mat',
        # 'satimage-2.mat',
        'mnist.mat',
    ]

    mat_file = mat_file_list[0]
    mat_file_name = mat_file.replace('.mat', '')
    print("\n... Processing", mat_file_name, '...')
    mat = sp.io.loadmat(os.path.join('', 'datasets', mat_file))

    X = mat['X']
    y = mat['y']

    # standardize data to be digestible for most algorithms
    X = StandardScaler().fit_transform(X)

    X, X, y_train, y_test = \
        train_test_split(X, y, test_size=0.4, random_state=42)

    contamination = y.sum() / len(y)

    base_estimators = [
        LOF(n_neighbors=5, contamination=contamination),
        LOF(n_neighbors=15, contamination=contamination),
        LOF(n_neighbors=25, contamination=contamination),
        LOF(n_neighbors=35, contamination=contamination),
        LOF(n_neighbors=45, contamination=contamination),
        LOF(n_neighbors=5, contamination=contamination),
        LOF(n_neighbors=15, contamination=contamination),
        LOF(n_neighbors=25, contamination=contamination),
        LOF(n_neighbors=35, contamination=contamination),
        LOF(n_neighbors=45, contamination=contamination),
        LOF(n_neighbors=5, contamination=contamination),
        LOF(n_neighbors=15, contamination=contamination),
        LOF(n_neighbors=25, contamination=contamination),
        LOF(n_neighbors=35, contamination=contamination),
        LOF(n_neighbors=45, contamination=contamination),
        LOF(n_neighbors=5, contamination=contamination),
        LOF(n_neighbors=15, contamination=contamination),
        LOF(n_neighbors=25, contamination=contamination),
        LOF(n_neighbors=35, contamination=contamination),
        LOF(n_neighbors=45, contamination=contamination),
        LOF(n_neighbors=5, contamination=contamination),
        LOF(n_neighbors=15, contamination=contamination),
        LOF(n_neighbors=25, contamination=contamination),
        LOF(n_neighbors=35, contamination=contamination),
        LOF(n_neighbors=45, contamination=contamination),
        
        HBOS(contamination=contamination),
        HBOS(contamination=contamination),
        HBOS(contamination=contamination),
        HBOS(contamination=contamination),
        HBOS(contamination=contamination),
        HBOS(contamination=contamination),
        HBOS(contamination=contamination),
        HBOS(contamination=contamination),
        HBOS(contamination=contamination),
        HBOS(contamination=contamination),
        HBOS(contamination=contamination),
        HBOS(contamination=contamination),
        HBOS(contamination=contamination),
        HBOS(contamination=contamination),
        HBOS(contamination=contamination),
        HBOS(contamination=contamination),
        HBOS(contamination=contamination),
        HBOS(contamination=contamination),
        HBOS(contamination=contamination),
        HBOS(contamination=contamination),
        
        PCA(contamination=contamination),
        OCSVM(contamination=contamination),
        PCA(contamination=contamination),
        OCSVM(contamination=contamination),
        PCA(contamination=contamination),
        OCSVM(contamination=contamination),
        PCA(contamination=contamination),
        OCSVM(contamination=contamination),
        PCA(contamination=contamination),
        OCSVM(contamination=contamination),
        
        KNN(n_neighbors=5, contamination=contamination),
        KNN(n_neighbors=15, contamination=contamination),
        KNN(n_neighbors=25, contamination=contamination),
        KNN(n_neighbors=35, contamination=contamination),
        KNN(n_neighbors=45, contamination=contamination),
        KNN(n_neighbors=5, contamination=contamination),
        KNN(n_neighbors=15, contamination=contamination),
        KNN(n_neighbors=25, contamination=contamination),
        KNN(n_neighbors=35, contamination=contamination),
        KNN(n_neighbors=45, contamination=contamination),
        KNN(n_neighbors=5, contamination=contamination),
        KNN(n_neighbors=15, contamination=contamination),
        KNN(n_neighbors=25, contamination=contamination),
        KNN(n_neighbors=35, contamination=contamination),
        KNN(n_neighbors=45, contamination=contamination),
        KNN(n_neighbors=5, contamination=contamination),
        KNN(n_neighbors=15, contamination=contamination),
        KNN(n_neighbors=25, contamination=contamination),
        KNN(n_neighbors=35, contamination=contamination),
        KNN(n_neighbors=45, contamination=contamination),
        IForest(n_estimators=50, contamination=contamination),
        IForest(n_estimators=100, contamination=contamination),
        IForest(n_estimators=50, contamination=contamination),
        IForest(n_estimators=100, contamination=contamination),
        IForest(n_estimators=50, contamination=contamination),
        IForest(n_estimators=100, contamination=contamination),
        IForest(n_estimators=50, contamination=contamination),
        IForest(n_estimators=100, contamination=contamination),
       
        LSCP(detector_list=[LOF(contamination=contamination),
                            LOF(contamination=contamination)]),
        LSCP(detector_list=[LOF(contamination=contamination),
                            LOF(contamination=contamination)]),
        LSCP(detector_list=[LOF(contamination=contamination),
                            LOF(contamination=contamination)]),
        LSCP(detector_list=[LOF(contamination=contamination),
                            LOF(contamination=contamination)]),
        LSCP(detector_list=[LOF(contamination=contamination),
                            LOF(contamination=contamination)]),
    ]

    # model = SUOD(base_estimators=base_estimators, rp_flag_global=True,
    #              n_jobs=6, bps_flag=False, contamination=contamination,
    #              approx_flag_global=True)
    model = SUOD(base_estimators=base_estimators, rp_flag_global=True,
                 n_jobs=6, bps_flag=True, contamination=contamination,
                 approx_flag_global=True)

    start = time.time()
    model.fit(X)  # fit all models with X
    print('Fit time:', time.time() - start)
    print()

    start = time.time()
    model.approximate(X)  # conduct model approximation if it is enabled
    print('Approximation time:', time.time() - start)
    print()

    start = time.time()
    predicted_labels = model.predict(X)  # predict labels
    print('Predict time:', time.time() - start)
    print()

    start = time.time()
    predicted_scores = model.decision_function(X)  # predict scores
    print('Decision Function time:', time.time() - start)
    print()

    ##########################################################################
    # compare with no projection, no bps, and no approximation
    print("******************************************************************")
    n_estimators = len(base_estimators)
    n_jobs = 6
    n_estimators_list, starts, n_jobs = _partition_estimators(n_estimators,
                                                              n_jobs)

    rp_flags = np.zeros([n_estimators, 1])
    approx_flags = np.zeros([n_estimators, 1])
    objective_dim = None
    rp_method = None

    start = time.time()
    all_results = Parallel(n_jobs=n_jobs, max_nbytes=None, verbose=True)(
        delayed(_parallel_fit)(
            n_estimators_list[i],
            base_estimators[starts[i]:starts[i + 1]],
            X,
            n_estimators,
            rp_flags[starts[i]:starts[i + 1]],
            objective_dim,
            rp_method=rp_method,
            verbose=True)
        for i in range(n_jobs))

    print('Orig Fit time:', time.time() - start)
    print()

    all_results = list(map(list, zip(*all_results)))
    trained_estimators = _unfold_parallel(all_results[0], n_jobs)
    jl_transformers = _unfold_parallel(all_results[1], n_jobs)

    ##########################################################################
    start = time.time()
    # model prediction
    all_results_pred = Parallel(n_jobs=n_jobs, max_nbytes=None,
                                verbose=True)(
        delayed(_parallel_predict)(
            n_estimators_list[i],
            trained_estimators[starts[i]:starts[i + 1]],
            None,
            X,
            n_estimators,
            rp_flags[starts[i]:starts[i + 1]],
            jl_transformers,
            approx_flags[starts[i]:starts[i + 1]],
            contamination,
            verbose=True)
        for i in range(n_jobs))

    print('Orig Predict time:', time.time() - start)
    print()

    # unfold and generate the label matrix
    predicted_labels_orig = np.zeros([X.shape[0], n_estimators])
    for i in range(n_jobs):
        predicted_labels_orig[:, starts[i]:starts[i + 1]] = np.asarray(
            all_results_pred[i]).T
        
    
    ##########################################################################
    # start = time.time()
    # # model prediction
    # all_results_pred_p = Parallel(n_jobs=n_jobs, max_nbytes=None,
    #                             verbose=True)(
    #     delayed(_parallel_predict)(
    #         n_estimators_list[i],
    #         model.base_estimators[starts[i]:starts[i + 1]],
    #         model.approximators[starts[i]:starts[i + 1]],
    #         X,
    #         n_estimators,
    #         rp_flags[starts[i]:starts[i + 1]],
    #         jl_transformers,
    #         approx_flags[starts[i]:starts[i + 1]],
    #         contamination,
    #         verbose=True)
    #     for i in range(n_jobs))

    # print('Orig Predict time p:', time.time() - start)
    # print()

    # # unfold and generate the label matrix
    # predicted_labels_orig = np.zeros([X.shape[0], n_estimators])
    # for i in range(n_jobs):
    #     predicted_labels_orig[:, starts[i]:starts[i + 1]] = np.asarray(
    #         all_results_pred_p[i]).T

    ##########################################################################

    start = time.time()
    # model prediction
    all_results_scores = Parallel(n_jobs=n_jobs, max_nbytes=None,
                                  verbose=True)(
        delayed(_parallel_decision_function)(
            n_estimators_list[i],
            trained_estimators[starts[i]:starts[i + 1]],
            None,
            X,
            n_estimators,
            rp_flags[starts[i]:starts[i + 1]],
            None,
            approx_flags[starts[i]:starts[i + 1]],
            verbose=True)
        for i in range(n_jobs))

    print('Orig decision_function time:', time.time() - start)
    print()

    # unfold and generate the label matrix
    predicted_scores_orig = np.zeros([X.shape[0], n_estimators])
    for i in range(n_jobs):
        predicted_scores_orig[:, starts[i]:starts[i + 1]] = np.asarray(
            all_results_scores[i]).T
    ##########################################################################
    predicted_scores = standardizer(predicted_scores)
    predicted_scores_orig = standardizer(predicted_scores_orig)

    evaluate_print('orig', y_test, np.mean(predicted_scores_orig, axis=1))
    evaluate_print('new', y_test, np.mean(predicted_scores, axis=1))
    
#%%

    ##########################################################################
    start = time.time()
    for i in range(n_estimators):
        print(i)
        trained_estimators[i].predict(X)

    print('Orig decision_function time:', time.time() - start)
    print()
    
    ##########################################################################
    start = time.time()
    for i in range(n_estimators):
        print(i)
        if approx_flags[i] == 1:
            model.approximators[i].predict(X)
        else:
            model.base_estimators[i].predict(X)

    print('Orig decision_function time:', time.time() - start)
    print()
    



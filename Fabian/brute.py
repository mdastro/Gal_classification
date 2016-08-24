import copy
import numpy
from sklearn import neighbors

class Combination(object):
    
    def __init__(self, error, coords):
        
        self.error = error
        self.coords = coords
        
    def __repr__(self):
        
        return str(self.error)

class BruteNN(object):
    """     
    """

    ALLOWED_FLOAT_TYPES = ['float', "double"]
    MAX_N_FEATURES = 6    

    DEFAULT_PARAMS = {
                       'n_neighbors':10, \
                       'n_selected_features':2, \
                       'n_top_combinations':10, \
                       'float_type':"double", \
                       'n_jobs':-1, \
                       'verbose':0, \
                      }    
        
    def __init__(self, **kwargs):

        self.algorithm_params = copy.deepcopy(self.DEFAULT_PARAMS)
        for key in kwargs.keys():
            self.algorithm_params[key] = kwargs[key]
        for key in self.algorithm_params:
            setattr(self, key, self.algorithm_params[key])

    def get_params(self, deep=True):

        return {"n_neighbors": self.n_neighbors, \
                "n_selected_features": self.n_selected_features, \
                "n_top_combinations": self.n_top_combinations, \
                "algorithm_params": self.algorithm_params, \
                "float_type": self.float_type, \
                "verbose": self.verbose
                }

    def set_params(self, **parameters):

        for parameter, value in parameters.items():
            self.setattr(parameter, value)
        
    def fit(self, X, y):

        assert self.n_top_combinations > 0;
        assert self.float_type in self.ALLOWED_FLOAT_TYPES

        ## set numpy float and int dtypes
        if self.float_type == "float":
            self.numpy_dtype_float = numpy.float32
        else:
            self.numpy_dtype_float = numpy.float64
        self.numpy_dtype_int = numpy.int32

        # convert input data to correct types (and generate local
        # variable to prevent destruction of external array)
        self.Xtrain = X
        self.ytrain = y
                                                    
        self._check_all_combinations()

        return self
    
    def _check_all_combinations(self):
        
        # init combinations (last one is error)
        self._top_combinations_errors = []
        for _ in xrange(self.n_top_combinations):
            comb = Combination(float('Inf'), [-1 for _ in xrange(self.MAX_N_FEATURES)])
            self._top_combinations_errors.append(comb)

        if self.n_selected_features == 2:
            self._check_all_2d()
        elif self.n_selected_features == 3:
            self._check_all_3d()
        elif self.n_selected_features == 4:
            self._check_all_4d()
        elif self.n_selected_features == 5:
            self._check_all_5d()
        elif self.n_selected_features == 6:
            self._check_all_6d()                        
        else:
            raise Exception("Implementation can only handle up to 4 features to be selected ...")
    
    def _check_all_2d(self):

        for i1 in range(self.Xtrain.shape[1]):
            if self.verbose > 0:
                print("Progress %i/%i" % (i1,self.Xtrain.shape[1]-1))
            for i2 in range(i1 + 1, self.Xtrain.shape[1]):
                
                model = neighbors.KNeighborsClassifier(self.n_neighbors, n_jobs=self.n_jobs)
                model.fit(self.Xtrain[:, [i1, i2]], self.ytrain)
                err = self._get_classification_error(model, self.Xtrain[:, [i1, i2]], self.ytrain)
                    
                comb = Combination(err, coords=[i1, i2])
                self._add_to_top_combinations_errors(comb)
                
    def _check_all_3d(self):
        
        for i1 in range(self.Xtrain.shape[1]):
            if self.verbose > 1:
                print("i1=%i" % i1)
            for i2 in range(i1 + 1, self.Xtrain.shape[1]):
                for i3 in range(i2 + 1, self.Xtrain.shape[1]):
                    
                    model = neighbors.KNeighborsClassifier(self.n_neighbors, n_jobs=self.n_jobs)
                    model.fit(self.Xtrain[:, [i1, i2, i3]], self.ytrain)
                    err = self._get_classification_error(model, self.Xtrain[:, [i1, i2, i3]], self.ytrain)
                        
                    comb = Combination(err, coords=[i1, i2, i3])
                    self._add_to_top_combinations_errors(comb)       
                    
    def _check_all_4d(self):
        
        for i1 in range(self.Xtrain.shape[1]):
            if self.verbose > 0: print("i1=%i" % i1)            
            for i2 in range(i1 + 1, self.Xtrain.shape[1]):
                if self.verbose > 1: print("i2=%i" % i2)                         
                for i3 in range(i2 + 1, self.Xtrain.shape[1]):
                    for i4 in range(i3 + 1, self.Xtrain.shape[1]):
                    
                        model = neighbors.KNeighborsClassifier(self.n_neighbors, n_jobs=self.n_jobs)
                        model.fit(self.Xtrain[:, [i1, i2, i3, i4]], self.ytrain)
                        err = self._get_classification_error(model, self.Xtrain[:, [i1, i2, i3, i4]], self.ytrain)
                            
                        comb = Combination(err, coords=[i1, i2, i3, i4])
                        self._add_to_top_combinations_errors(comb)  
                        
    def _check_all_5d(self):
        
        for i1 in range(self.Xtrain.shape[1]):
            if self.verbose > 0: print("i1=%i" % i1)            
            for i2 in range(i1 + 1, self.Xtrain.shape[1]):
                if self.verbose > 1: print("i2=%i" % i2)                         
                for i3 in range(i2 + 1, self.Xtrain.shape[1]):
                    for i4 in range(i3 + 1, self.Xtrain.shape[1]):
                        for i5 in range(i4 + 1, self.Xtrain.shape[1]):
                    
                            model = neighbors.KNeighborsClassifier(self.n_neighbors, n_jobs=self.n_jobs)
                            model.fit(self.Xtrain[:, [i1, i2, i3, i4, i5]], self.ytrain)
                            err = self._get_classification_error(model, self.Xtrain[:, [i1, i2, i3, i4, i5]], self.ytrain)
                                
                            comb = Combination(err, coords=[i1, i2, i3, i4, i5])
                            self._add_to_top_combinations_errors(comb)       
                            
    def _check_all_6d(self):
        
        for i1 in range(self.Xtrain.shape[1]):
            if self.verbose > 0: print("i1=%i" % i1)            
            for i2 in range(i1 + 1, self.Xtrain.shape[1]):
                if self.verbose > 1: print("i2=%i" % i2)                         
                for i3 in range(i2 + 1, self.Xtrain.shape[1]):
                    for i4 in range(i3 + 1, self.Xtrain.shape[1]):
                        for i5 in range(i4 + 1, self.Xtrain.shape[1]):
                            for i6 in range(i5 + 1, self.Xtrain.shape[1]):
                    
                                model = neighbors.KNeighborsClassifier(self.n_neighbors, n_jobs=self.n_jobs)
                                model.fit(self.Xtrain[:, [i1, i2, i3, i4, i5, i6]], self.ytrain)
                                err = self._get_classification_error(model, self.Xtrain[:, [i1, i2, i3, i4, i5, i6]], self.ytrain)
                                    
                                comb = Combination(err, coords=[i1, i2, i3, i4, i5, i6])
                                self._add_to_top_combinations_errors(comb)                                                                            
    
    def _get_classification_error(self, model, X, y):
        
        ypred = model.predict(X)
        return float((ypred != y).sum()) / len(y)
                
    def _add_to_top_combinations_errors(self, comb):

        if self.verbose > 0 and comb.error < self._top_combinations_errors[-1].error:
            print("Adding combination with error %f to list ..." % comb.error)
        
        self._top_combinations_errors.append(comb)
        self._top_combinations_errors.sort(key=lambda x: x.error)
        self._top_combinations_errors = self._top_combinations_errors[:self.n_top_combinations]
            
    def get_top_combinations(self):
        
        combinations = numpy.zeros((self.n_top_combinations, self.n_selected_features), dtype=self.numpy_dtype_int)
        
        for i in xrange(self.n_top_combinations):
            for j in xrange(self.n_selected_features):
                combinations[i, j] = self._top_combinations_errors[i].coords[j]
                
        return combinations

    def get_top_errors(self):
        
        errors = numpy.zeros((self.n_top_combinations), dtype=self.numpy_dtype_float)
        
        for i in xrange(self.n_top_combinations):
            errors[i] = self._top_combinations_errors[i].error
            
        return errors    

    def predict(self, X):

        model = neighbors.KNeighborsClassifier(self.n_neighbors, n_jobs=self.n_jobs)
        comb = self.get_top_combinations()[0]
        model.fit(self.Xtrain[:, comb], self.ytrain)
        preds = model.predict(X[:, comb])

        return preds
        

import numpy as np
from sklearn import decomposition


class MLE:
    """
    My implementation of the closed form approch to maximum likelihood principal component analysis.
    The implementation is based on the paper "Bayesian PCA" by Christopher M. Bishop section 2.
    see: https://papers.nips.cc/paper/1549-bayesian-pca.pdf

    The naming of the variables are based on the paper, so the code should be easy to follow if you have read the paper.

    """
    def __init__(self,q_dimension,verbose=True,centered_data=False):
        self.q = q_dimension # dimension to reduce to
        self.verbose = verbose

    def center_data(self, X):
        return X - np.mean(X,axis=0)

    def _calculate_MLE(self, X):
        # Assuming that the data is centered
        assert np.allclose(np.mean(X,axis=0),0), 'Data is not centered'

        n,d = X.shape

        U, L, _ = np.linalg.svd(X)

        Eigvals,_ = np.linalg.eig(np.cov(X.T)) # Same as L**2 / (n-1)
        Eigvals = -np.sort(-Eigvals)

        var = np.sum(Eigvals[self.q:]) / (d-self.q)

        w_1 = np.diag(Eigvals[:self.q] - np.ones(self.q)*var)**0.5
        W = U[:,:self.q] @ w_1

        m =  (W.T@ W) + np.ones(self.q)*var

        z =  np.linalg.inv(m) @ W.T @ X
        print(z.shape)

        return var, W, z, U, L

    def applyDimensionality(self,U,L):
        return U[:,:self.q] * -L[:self.q]

    def _C(self,W):
        eps = np.zeros((self.q,self.q),dtype=float)
        np.fill_diagonal(a = eps, val = np.random.normal(0,1))
        return np.dot(W.T,W) + eps

    def log_like(self,W, n,d):
        C = self._C(W)
        return -(n/2) * (d * np.log(2 * np.pi) + np.log( np.linalg.det(C) ) + np.trace( np.dot( np.linalg.inv(C), C) ) ) # The last variable should be S but C is also described as the covariance
    
    def fit(self, X, is_centered=False):
        N, d = X.shape

        if not is_centered:
            X=self.center_data(X)

        S = np.cov(X,rowvar=False)

        # Maximum Likelihood Estimate
        var, W, z, U, L = self._calculate_MLE(X)

        x_new = self.applyDimensionality(U,L)
        
        # Loglike
        ll = self.log_like(W, N, d)

        return var, W, z, x_new, ll

if __name__ == '__main__':
    
    from sklearn import datasets

    X = datasets.load_iris().data
    y = datasets.load_iris().target

    model = MLE(q_dimension=3,verbose=False)
    var, W, z, x_new, ll = model.fit(X)
    
    pca = decomposition.PCA(n_components=3)
    pca.fit(X)
    X = pca.transform(X)

    print('scikit PC variance:\n', pca.noise_variance_,'\nMy PC variance:\n', var,'\nDifference in variance:\n', var-pca.noise_variance_)
    print('Scikit transform:\n', X, '\nMy transform:\n', x_new)
    print('loglikelihood of solution: ', ll)
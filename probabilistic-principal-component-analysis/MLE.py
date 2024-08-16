import numpy as np
from sklearn import decomposition


class mlePCA:
    """
    My implementation of the closed form approch to maximum likelihood principal component analysis.
    The implementation is based on the paper "Bayesian PCA" by Christopher M. Bishop section 2.
    see: https://papers.nips.cc/paper/1549-bayesian-pca.pdf
    """
    def __init__(self,data,q_dimension,verbose=True,centered_data=False):
        self.D = data                   # numpy array of data
        self.N, self.d = self.D.shape   # dimensions
        self.q = q_dimension            # dimension to reduce to

        self.S = np.cov(self.D,rowvar=False)

        self.centered = centered_data
        self.verbose = verbose

    def center_data(self):
        if not self.centered:
            self.Dm = self.D.copy()
            self.Dm = (self.Dm - np.mean(self.Dm,axis=0))
            self.centered = True

    def MLE(self):
        U, L, _ = np.linalg.svd(self.Dm)

        Eigvals,_ = np.linalg.eig(np.cov(self.Dm.T)) # Same as L**2 / (n-1)
        Eigvals = -np.sort(-Eigvals)

        var = np.sum(Eigvals[self.q:]) / (self.d-self.q)

        w_1 = np.diag(Eigvals[:self.q] - np.ones(self.q)*var)**0.5
        W = U[:,:self.q] @ w_1

        m =  (W.T@ W) + np.ones(self.q)*var

        z =  np.linalg.inv(m) @ W.T @ self.Dm
        print(z.shape)

        return var, W, z, U, L

    def applyDimensionality(self,U,L):
        return U[:,:self.q] * -L[:self.q]

    def _C(self,W):
        eps = np.zeros((self.q,self.q),dtype=float)
        np.fill_diagonal(a = eps, val = np.random.normal(0,1))
        return np.dot(W.T,W) + eps

    def log_like(self,W):
        C = self._C(W)
        return -(self.N/2) * (self.d * np.log(2 * np.pi) + np.log( np.linalg.det(C) ) + np.trace( np.dot( np.linalg.inv(C), C) ) ) # The last variable should be S but C is also described as the covariance
    
    def fit(self):
        if not self.centered:
            self.center_data()

        # Maximum Likelihood Estimate
        var, W, z, U, L = self.MLE()

        x_new = self.applyDimensionality(U,L)
        
        # Loglike
        ll = self.log_like(W)

        return var, W, z, x_new, ll

if __name__ == '__main__':
    
    from sklearn import datasets

    ############# iris data
    x = datasets.load_iris().data
    y = datasets.load_iris().target

    ############# toy DATA
    # n_samples = 5
    # p = 4    
    # x = np.random.normal(size=(n_samples, p)).astype(np.float32)
    # step = 4. * np.pi / n_samples    
    # for i in range(x.shape[0]):
    #     a = i * step - 6.
    #     x[i, 0] = a + np.random.normal(0, 0.1)
    #     x[i, 1] = 3. * (np.sin(a) + np.random.normal(0, .2))
    #     x[i, 3] =  np.random.normal(20, 0.1) *  x[i, 0]
    
    #############

    model = mlePCA(x,3,verbose=False)
    var, W, z, x_new, ll = model.fit()
    
    pca = decomposition.PCA(n_components=3)
    pca.fit(x)
    X = pca.transform(x)

    print('scikit PC variance:\n', pca.noise_variance_,'\nMy PC variance:\n', var,'\nDifference in variance:\n', var-pca.noise_variance_)
    print('Scikit transform:\n', X, '\nMy transform:\n', x_new)
    print('loglikelihood of solution: ', ll)
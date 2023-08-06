from ..cunnData import cunnData
from anndata import AnnData

from cuml.decomposition import PCA, TruncatedSVD
from typing import Optional, Union

from cupy.sparse import issparse
import math
import numpy as np


def pca(
    cudata: Union[cunnData, AnnData],
    layer: str = None,
    n_comps: Optional[int] = None,
    zero_center: bool = True,
    random_state: Union[int, None] = 0,
    use_highly_variable: Optional[bool] = None,
    chunked: bool = False,
    chunk_size: int = None,
) -> None:
    """
    Performs PCA using the cuML decomposition function for the :class:`~rapids_singlecell.cunnData.cunnData` object.

    Parameters
    ----------
        cudata :
            cunnData, AnnData object

        layer
            If provided, use `cudata.layers[layer]` for expression values instead of `cudata.X`.

        n_comps
            Number of principal components to compute. Defaults to 50, or 1 - minimum
            dimension size of selected representation

        zero_center
            If `True`, compute standard PCA from covariance matrix.
            If `False`, omit zero-centering variables

        random_state
            Change to use different initial states for the optimization.

        use_highly_variable
            Whether to use highly variable genes only, stored in
            `.var['highly_variable']`.
            By default uses them if they have been determined beforehand.

        chunked
            If `True`, perform an incremental PCA on segments of `chunk_size`.
            The incremental PCA automatically zero centers and ignores settings of
            `random_seed` and `svd_solver`. If `False`, perform a full PCA.

        chunk_size
            Number of observations to include in each chunk.
            Required if `chunked=True` was passed.

    Returns
    -------
        adds fields to `cudata` :
            `.obsm['X_pca']`
                PCA representation of data.
            `.varm['PCs']`
                The principal components containing the loadings.
            `.uns['pca']['variance_ratio']`
                Ratio of explained variance.
            `.uns['pca']['variance']`
                Explained variance, equivalent to the eigenvalues of the
                covariance matrix.
    """

    if use_highly_variable is True and "highly_variable" not in cudata.var.keys():
        raise ValueError(
            "Did not find cudata.var['highly_variable']. "
            "Either your data already only consists of highly-variable genes "
            "or consider running `highly_variable_genes` first."
        )

    X = cudata.layers[layer] if layer is not None else cudata.X

    if use_highly_variable is None:
        use_highly_variable = True if "highly_variable" in cudata.var.keys() else False

    if use_highly_variable:
        X = X[:, cudata.var["highly_variable"]]

    if n_comps is None:
        min_dim = min(X.shape[0], X.shape[1])
        if 50 >= min_dim:
            n_comps = min_dim - 1
        else:
            n_comps = 50

    if chunked:
        from cuml.decomposition import IncrementalPCA

        X_pca = np.zeros((X.shape[0], n_comps), X.dtype)

        pca_func = IncrementalPCA(
            n_components=n_comps, output_type="numpy", batch_size=chunk_size
        )
        pca_func.fit(X)

        n_batches = math.ceil(X.shape[0] / chunk_size)
        for batch in range(n_batches):
            start_idx = batch * chunk_size
            stop_idx = min(batch * chunk_size + chunk_size, X.shape[0])
            chunk = X[start_idx:stop_idx, :]
            chunk = chunk.toarray() if issparse(chunk) else chunk
            X_pca[start_idx:stop_idx] = pca_func.transform(chunk)
    else:
        if zero_center:
            pca_func = PCA(
                n_components=n_comps, random_state=random_state, output_type="numpy"
            )
            X_pca = pca_func.fit_transform(X)

        elif not zero_center:
            pca_func = TruncatedSVD(
                n_components=n_comps, random_state=random_state, output_type="numpy"
            )
            X_pca = pca_func.fit_transform(X)

    cudata.obsm["X_pca"] = X_pca
    cudata.uns["pca"] = {
        "variance": pca_func.explained_variance_,
        "variance_ratio": pca_func.explained_variance_ratio_,
    }
    if use_highly_variable:
        cudata.varm["PCs"] = np.zeros(shape=(cudata.n_vars, n_comps))
        cudata.varm["PCs"][cudata.var["highly_variable"]] = pca_func.components_.T
    else:
        cudata.varm["PCs"] = pca_func.components_.T

import pandas as pd
import pkg_resources

import numpy as np
from scipy.special import log1p
from scipy.sparse import issparse


class id_map(object):
    '''
    initialize the id mapping object
    
    species : string
        required. Name of species: human or mouse
        
    key: string (default: ensembl)
        The id type you are using as input keys.
        Options: symbol, ensembl, entrez
    
    target : string (default: symbol)
        The id type you want returned.
        Options: symbol, ensembl, entrez
        
    '''
    
    
    def __init__(self, species = None, key = 'ensembl', target = 'symbol'):
        
        self.key = key
        
        self.target = target
        
        self.species = species
        
        if self.species not in ['human', 'mouse']:
            raise Exception("set species to one of the following: human, mouse")
        
        
        if self.species == 'human':
            stream = pkg_resources.resource_stream(__name__, 'data/human_ids.csv')
            self.dataframe = pd.read_csv(stream)
            self.dataframe = self.dataframe.rename(columns={'hgnc_symbol': 'symbol',
                                                            'ensembl_gene_id':'ensembl',
                                                            'entrezgene_id':'entrez'})
        else:
            stream = pkg_resources.resource_stream(__name__, 'data/mouse_ids.csv')
            self.dataframe = pd.read_csv(stream)
            self.dataframe = self.dataframe.rename(columns={'uniprot_gn_symbol': 'symbol',
                                                            'ensembl_gene_id':'ensembl',
                                                            'entrezgene_id':'entrez'})
        
        
        self.mapper = self.dataframe[(self.dataframe[self.key].notna()) &\
                                     (self.dataframe[self.target].notna())]
        
        
        if target != 'entrez':
            self.mapper = dict(zip(self.mapper[self.key], self.mapper[self.target]))
        else: #because entrez is imported as floats
            self.mapper = dict(zip(self.mapper[self.key],
                                   self.mapper[self.target].map(lambda x: str(round(x)))))
            
            
    def map_column(self, df, column = None):
        '''
        map your mapping object to a pandas dataframe column.
        
        Returns a dataframe with an appended column (target + _map) containing mapped ids.
        
        df: pandas.DataFrame
        
        column: string
            Name of column containing the keys
        
        '''
        df[self.target + '_map'] = df[column].map(self.mapper)
        return df
    
    def map_list(self, l):
        '''
        Returns a mapped list with 'NA' for unmappable keys
        
        l: list
        
        '''
        def mini_mapper(x):
            try:
                return self.mapper[x]
            except:
                return 'NA'
        return [mini_mapper(x) for x in l]





######################################### DEVIANT FEATURE SELECTION START ######################


def sparseBinomialDev(X):
    """
    Function to calculate deviance for sparse data.

    Parameters:
    ----------
    X : sparse matrix
        Input data in sparse matrix format

    Returns:
    -------
    deviance : array
        Deviance calculated for each feature across all cells
    """
    sz = np.sum(X, axis = 1) 
    LP = X.multiply(1 / sz)
    LP.data = np.log(LP.data)
    L1P = X.multiply(1 / sz)
    L1P.data = log1p(-L1P.data)
    ll_sat = np.array((X.multiply(LP - L1P) + L1P.multiply(sz)).sum(axis=0)).flatten()
    sz_sum = sz.sum()
    feature_sums = np.array(X.sum(axis=0)).flatten()
    p = feature_sums / sz_sum
    l1p = log1p(-p)

    with np.errstate(divide='ignore', invalid='ignore'):
        ll_null = feature_sums * (np.log(p) - l1p) + sz_sum * l1p

    return 2 * (ll_sat - ll_null)

def denseBinomialDev(X):
    """
    Function to calculate deviance for dense data.

    Parameters:
    ----------
    X : ndarray
        Input data in numpy ndarray format

    Returns:
    -------
    deviance : array
        Deviance calculated for each feature across all cells
    """
    
    sz = np.sum(X, axis = 1)
    P = X / sz[:, np.newaxis]
    L1P = np.log1p(-P)
    with np.errstate(divide='ignore', invalid='ignore'):
        term = X * (np.log(P) - L1P) + (sz[:, np.newaxis] * L1P)
    nan_mask = np.isnan(term)
    term[nan_mask] = 0
    ll_sat = np.sum(term, axis=0)
    sz_sum = sz.sum()
    feature_sums  = X.sum(axis = 0)
    p = feature_sums / sz_sum
    l1p = np.log1p(-p)
    with np.errstate(divide='ignore', invalid='ignore'):
        ll_null = feature_sums*(np.log(p)-l1p)+sz_sum*l1p
        
    return 2*(ll_sat-ll_null)



def deviance_feature_selection(adata, batch_key=None, ntop=4000, inplace = True, subset = False):
    """
    Feature selection based on deviance. Adds columns to adata.var and optionally subsets adata to highly deviant features.

    This is a python implementation the R scry package. Please cite them (not me):
    https://bioconductor.org/packages/release/bioc/html/scry.html
        
    Parameters:
    ----------
    adata : AnnData
        Annotated data matrix
    batch_key : str, optional
        Key to a categorical annotation from adata.obs that will be used for batch effect. 
        If None, function will not account for batch effects. Deviance is caclulated for each
        batch separately then summed.
    ntop : int, optional
        Number of top features with highest deviance to mark and/or retain.
    inplace : bool, optional
        Whether to modify the original adata object. If False, a copy is made and modified.
    subset : bool, optional
        Whether to subset the adata object or only add 'highly_deviant' column to .var.

    Returns:
    -------
    If `inplace` is False, returns an AnnData object, else None.
    """
    if batch_key is None:
        if issparse(adata.X):
            deviance = sparseBinomialDev(adata.X)
        else:
            deviance = denseBinomialDev(adata.X)
    else:
        batches = adata.obs[batch_key].unique()
        deviances = []
        for batch in batches:
            batch_data = adata[adata.obs[batch_key] == batch].X
            if issparse(batch_data):
                deviance = sparseBinomialDev(batch_data)
            else:
                deviance = denseBinomialDev(batch_data)
        
            deviances.append(deviance)
        
        deviance = np.sum(deviances, axis=0)
        

    deviance[np.isnan(deviance)] = 0
    
    
    if inplace:
        adata.var['deviance'] = deviance
        top_vars = adata.var.sort_values('deviance', ascending=False).index[:ntop]
        
        adata.var['highly_deviant'] = adata.var.index.isin(top_vars)
        
        
        if subset:
            return adata[:, adata.var.highly_deviant]
        
    
        
    else:
        adata_copy = adata.copy()
        adata_copy.var['deviance'] = deviance
        top_vars = adata_copy.var.sort_values('deviance', ascending=False).index[:ntop]
    
        adata_copy.var['highly_deviant'] = adata_copy.var.index.isin(top_vars)
        
        if subset:
            return adata_copy[:, adata_copy.var.highly_deviant]
        else:
            return adata_copy



######################################### DEVIANT FEATURE SELECTION END ####################################








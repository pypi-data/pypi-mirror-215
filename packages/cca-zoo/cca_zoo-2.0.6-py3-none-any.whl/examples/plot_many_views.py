"""
More than 2 views
===========================

This will compare MCCA, GCCA, TCCA for linear classical with more than 2 views
"""
import numpy as np

from cca_zoo.data.simulated import LinearSimulatedData
from cca_zoo.classical import GCCA, KCCA, KGCCA, KTCCA, MCCA, SCCA_PMD, TCCA

"""
Data
-----
"""
# %%
np.random.seed(42)
n = 30
p = 3
q = 3
r = 3
latent_dims = 1
cv = 3

(X, Y, Z) = LinearSimulatedData(
    view_features=[p, q, r], latent_dims=latent_dims, correlation=[0.9]
).sample(n)

# %%
# Eigendecomposition-Based Methods
# ---------------------------------

# %%
# Linear
# ^^^^^^^^

# %%
mcca = MCCA(latent_dimensions=latent_dims).fit((X, Y, X)).score((X, Y, Z))

# %%
gcca = GCCA(latent_dimensions=latent_dims).fit((X, Y, X)).score((X, Y, Z))

# %%
# Kernel
# ^^^^^^^^

# %%
kcca = KCCA(latent_dimensions=latent_dims).fit((X, Y, X)).score((X, Y, Z))

# %%
kgcca = KGCCA(latent_dimensions=latent_dims).fit((X, Y, X)).score((X, Y, Z))

# %%
# Iterative Methods
# ^^^^^^^^^^^^^^^^^^

# Most of the _iterative methods can also use multiple views e.g.

pmd = (
    SCCA_PMD(latent_dimensions=latent_dims, tau=0.1, tol=1e-5)
    .fit((X, Y, X))
    .score((X, Y, Z))
)

# %%
# Higher Order Correlations
# -------------------------

# %%
# Tensor CCA finds higher order correlations so scores are not comparable (but TCCA is equivalent for 2 views)
tcca = TCCA(latent_dimensions=latent_dims).fit((X, Y, X)).score((X, Y, Z))

# %%
ktcca = KTCCA(latent_dimensions=latent_dims).fit((X, Y, X)).score((X, Y, Z))

"""Load some data, fit Discover(), predict on validation data, make some plots, and save the model."""
# %% imports
import pandas as pd
from crabnet.data.materials_data import elasticity
from mat_discover.mat_discover_ import Discover

# %% setup
# set dummy to True for a quicker run --> small dataset, MDS instead of UMAP
dummy = False
# set gcv to False for a quicker run --> group-cross validation can take a while
gcv = False
disc = Discover(dummy_run=dummy, device="cuda", target_unit="GPa")
train_df, val_df = disc.data(elasticity, fname="train.csv", dummy=dummy)
cat_df = pd.concat((train_df, val_df), axis=0)

# %% fit
disc.fit(train_df)

# %% predict
score = disc.predict(val_df, umap_random_state=42)

# %% leave-one-cluster-out cross-validation
if gcv:
    disc.group_cross_val(cat_df, umap_random_state=42)
    print("scaled test error = ", disc.scaled_error)

# %% plot and save
disc.plot()
disc.save(dummy=dummy)

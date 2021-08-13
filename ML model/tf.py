!pip install tensorflow_decision_forests
!pip install wurlitzer
import tensorflow_decision_forests as tfdf

import os
import numpy as np
import pandas as pd
import tensorflow as tf
import math

try:
  from wurlitzer import sys_pipes
except:
  from colabtools.googlelog import CaptureLog as sys_pipes

from IPython.core.magic import register_line_magic
from IPython.display import Javascript

dataset_df = pd.read_csv("ClimateVars (cleaned).csv")
def split_dataset(dataset, test_ratio=0.10):
  """Splits a panda dataframe in two."""
  test_indices = np.random.rand(len(dataset)) < test_ratio
  return dataset[~test_indices], dataset[test_indices]


train_ds_pd, test_ds_pd = split_dataset(dataset_df)
print("{} examples in training, {} examples for testing.".format(
    len(train_ds_pd), len(test_ds_pd)))
label = "Presence"
train_ds = tfdf.keras.pd_dataframe_to_tf_dataset(train_ds_pd, label=label)
test_ds = tfdf.keras.pd_dataframe_to_tf_dataset(test_ds_pd, label=label)

# Specify the model.
model_1 = tfdf.keras.RandomForestModel()

# Optionally, add evaluation metrics.
model_1.compile(
    metrics=["accuracy"])

# Train the model.
# "sys_pipes" is optional. It enables the display of the training logs.
with sys_pipes():
  model_1.fit(x=train_ds)
evaluation = model_1.evaluate(test_ds, return_dict=True)
print()

for name, value in evaluation.items():
  print(f"{name}: {value:.4f}")
model_1.save("tfmodelmosquito1")
tfdf.model_plotter.plot_model_in_colab(model_1, tree_idx=0, max_depth=3)
a = [17, 88, 1000, 0.47, 95]
df=pd.DataFrame (columns=["Temperature", "Humidity", "Pressure", "Precipitation", "Cloud Cover"])
df.loc[len(df)] = a
print (df)
df_ds=tfdf.keras.pd_dataframe_to_tf_dataset(df)
import numpy as np
model_1=tf.keras.models.load_model("tfmodelmosquito")


prediction = model_1.predict(df_ds)
print (prediction)

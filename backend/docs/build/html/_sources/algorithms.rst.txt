ALGORITHMS
==========

This section documents the internal code used for building and executing the Artificial Intelligence models within the VITA Platform.
All modules are organized inside the `algorithms` directory in a modular way to facilitate maintenance, testing, and extensibility.

General Structure
`core` – Contains utility functions, data preprocessing routines, normalization methods, and shared components for all models.

`hybrid_model` – Implements the hybrid model, which combines different forecasting approaches to improve accuracy.

`lstm` – Implementation of the Long Short-Term Memory model, used for multivariate time series forecasting.

`pycaret` – Integrates the PyCaret framework, enabling rapid experimentation with multiple algorithms.

`rc` – Implements Reservoir Computing, a recurrent neural network-based technique for time series forecasting.

--------

**Module Documentation**
----------------------------------------

`Core`

.. automodule:: algorithms.core
   :members:

`Hybrid Model`

.. automodule:: algorithms.hybrid_model
   :members:

`LSTM`

.. automodule:: algorithms.lstm
   :members:

`PyCaret`

.. automodule:: algorithms.pycaret
   :members:

`Reservoir Computing (RC)`

.. automodule:: algorithms.rc
   :members:
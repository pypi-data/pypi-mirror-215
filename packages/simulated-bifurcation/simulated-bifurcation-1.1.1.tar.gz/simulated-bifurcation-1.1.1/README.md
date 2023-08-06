# Simulated Bifurcation for Python

[![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?logo=PyTorch&logoColor=white)](https://pytorch.org/)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1xtse4sLIDAh8nsQ6HcIr7BzM7sft88WA?usp=sharing)
![GitHub stars](https://img.shields.io/github/stars/bqth29/simulated-bifurcation-algorithm.svg?style=social&label=Star)

Python implementation of the _Simulated Bifurcation_ algorithm in order to approximize the optimal solution of **Ising problems**. The last accuracy tests showed a median optimality gap of less than 1% on high-dimensional instances.

## ⚙️ Install

```
pip install simulated-bifurcation
```

## 🧪 Scientific background

_Simulated bifurcation_ is a state-of-the-art algorithm based on quantum physics theory and used to approximize very accurately and quickly the optimal solution of Ising problems. 
>You can read about the scientific theories at stake and the engineering of the algorithm by Goto *et al.* here: https://www.nature.com/articles/s42005-022-00929-9

Ising problems can be used in many sectors such as finance, transportation or chemistry or derived as other well-know optimization problems (QUBO, Knapsack problem, ...).

## 🚀 Optimization of an Ising model

### Definition

An Ising problem, given a **square symmetric** matrix `J` of size `n x n` and a vector `h` of size `n`, consists in finding the spin vector `s = [s_1, s_2, ..., s_n]`, called the *ground state*, (each `s_i` is either `1` or `-1`) such that the value `E = - 0.5 * ∑∑ J_ij*s_i*s_j + ∑ h_i*s_i`, called *Ising energy*, is minimal.

### Create an instance

Given `J` and `h`, creating an Ising model is done as follows:

```python
import simulated_bifurcation as sb

ising = sb.Ising(J, h)
```

### Optimize a model

To optimize an Ising model using the Simulated Bifurcation algorithm, you simply need to run:

```python
ising.optimize()
```

The `optimize` methods takes several parameters that are presented in the dedicated section.

### Retrieve the ground state / Ising energy

Once the model is optimized, you can get the best found Ising features using model's attributes

```python
ising.energy # Ising energy -> float
ising.ground_state # Ground state (best spin vector) -> torch.Tensor
```

## 📊 Optimization parameters

The `optimize` methods uses a lot of parameters but only some of them may be changes since the biggest part has been set after reserach and fine-tuning work.

### Quantum parameters

These parameters stem from the quantum theory Their purpose is described in the paper cited above.

> The parameters marked with ⚠️ should not be changed to ensure a good accuracy of the algorithm.

- `pressure_slope` ⚠️
- `gerschgorin`: if `True` then uses the Gerschgorin's theorem to set the scale value; else uses the uses the value defined by Goto *et al.*
- `heat_parameter` ⚠️
- `time_step` ⚠️

### Simulated Bifurcation modes

There are four modes of the algorithm (ballistic v. discrete + heated v. non-heated) that result in small variations in the algorithm general operation. These mode can be selected setting the parameters `ballistic` and `heated` to `True` or `False`.

> The ballistic mode is supposed to give a slighter less satisfying accuracy but to converge faster in comparison to the discrete mode which is generally more accurate but also a bit slower.

### Early stopping

One particularity of our implementation of the Simulated Bifurcation algorithm is the possibility to perform an early stopping and save computation time. The sampling frequence and window size for deciding whether to stop or continue can be set through the parameters `sampling_period` and `convergence_threshold`. 

> Yet, the default parameters have been set as the result of a good trade-off betwwen computation time and accurary so it is not recommanded to change them.

To use early stopping, the `use_window` parameter must be set to `True`. Both ways, the algorithm will stop after a certain number of iterations (if early stopping conditions were not met or if `use_window` was set to `False`) that is defined by the `max_steps` parameter.

### Multi-agent optimization

This version of the Simulated Bifurcation algorithm also allows a multi-agent search of the optimal solution which benefits from the parallelization of the computations. The number of agents is set by the `agents` parameter.

> **💡 Tip:** it is faster to run once the algorithm with N agents than to run N times the algorithm with only one agent.

### Displaying the state of evolution

Finally, you can choose to show or hide the evolution of the algorithm setting the `verbose` parameter to either `True` or `False`.

> If you choose to set `verbose = True`, the evolution will be displayed as `tqdm` progress bar(s) in your terminal.

## 🔀 Derive the algorithm for other problems using the IsingInterface API

A lot of mathematical problems ([QUBO](https://en.wikipedia.org/wiki/Quadratic_unconstrained_binary_optimization), [TSP](https://en.wikipedia.org/wiki/Travelling_salesman_problem), ...) can be written as Ising problems, and thus can be solved using the Simulated Bifurcation algorithm. Some of them are already implemented in the `models` folder but you are free to create your own models using our API.

To do so, you need to create a subclass of the abstract class `IsingInterface` present in the `interface` submodule. The `IsingInterface` has only two attributes `dtype` and `device` which allow you to set the type of the data and the device with which you wish to work.

```python
from simulated_bifurcation.interface import IsingInterface


class YourModel(IsingInterface):

    def __init__(self, dtype, device, *args, **kwargs):
        super().__init__(dtype, device) # Mandatory
        # YOUR CODE HERE
        ...
```

Once created, such an object can be optimized using the same principle as an `Ising` object, using the `optimize` methods which uses the same parameters as the `Ising`'s one:

```python
your_model = YourModel(...)
your_model.optimize()
```

Yet, to make it work, you will first have to overwrite two abstract methods of the `IsingInterface` class (`to_ising` and `from_ising`) that are called by the `optimize` method. Otherwise you will get a `NotImplementedError` error message.

When the `optimize` method is called, an equivalent Ising model will first be created using `to_ising` and then optimized using the exact same parameters you provided as input for the `IsingInterface.optimize` method. Once it is optimized, information for your own model will be derived from the optimal features of this equivalent Ising model using `from_ising`.

### `to_ising` method

The `to_ising` is meant to create an instance of an Ising model based on the data of your problem. It takes no argument and must only return an `Ising` object. The idea is to rely on the parameters of your problems to derive an Ising representation of it. At some point in the definition of the method, you will have to create the `J` matrix and the `h` vector and eventually return `Ising(J, h)`.

```python
def to_ising(self) -> sb.Ising:
    # YOUR CODE HERE
    J = ...
    h = ...
    return sb.Ising(J, h, dtype=self.dtype, device=self.device)
```

> Do not forget to set the `device` attribute when you instantiate the class if you are working on a GPU because all the tensors must be set on the same device.

### `from_ising` method

The `from_ising` is the reciprocal method. Once the equivalent Ising model of your problem has been optimized, you can retrieve information from its ground state and/or energy and adapt them to your own problem. It must only take an `Ising` object for input and return `None`.

```python
def from_ising(self, ising: sb.Ising) -> None:
    # YOUR CODE HERE
    return 
```

### Binary and integer formulations

Note that many problems that can be represented as Ising models are not based on spin vectors but rather on binary or integer vectors. The `interface` submodule thus has two additional classes, `Binary` and `Integer`, both of which inherit from `IsingInterface` in order to generalize these cases more easily.

> 🔎 You can check [Andrew Lucas' paper](https://arxiv.org/pdf/1302.5843.pdf) on Ising formulations of NP-complete and NP-hard problems, including all of Karp's 21 NP-complete problems.

## 🔗 Cite this work

If you are using this code for your own projects please cite our work:

```bibtex
@software{Ageron_Simulated_Bifurcation_SB_2022,
    author = {Ageron, Romain and Bouquet, Thomas and Pugliese, Lorenzo},
    month = {4},
    title = {{Simulated Bifurcation (SB) algorithm for Python}},
    version = {1.1.0},
    year = {2023}
}
```

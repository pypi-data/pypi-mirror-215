import torch
from src.simulated_bifurcation.optimizer import SymplecticIntegrator, OptimizerMode


def test_init_ballistic_symplectic_integrator():
    symplectic_integrator = SymplecticIntegrator((3, 2), OptimizerMode.BALLISTIC, torch.float32, 'cpu')
    symplectic_integrator.momentum = torch.Tensor([[-0.7894, -0.4610], [-0.2343, 0.9186], [-0.2191, 0.2018]])
    assert torch.all(symplectic_integrator.sample_spins() == torch.Tensor([[-1, -1], [-1, 1], [-1, 1]]))

def test_init_discrete_symplectic_integrator():
    symplectic_integrator = SymplecticIntegrator((3, 2), OptimizerMode.DISCRETE, torch.float32, 'cpu')
    symplectic_integrator.momentum = torch.Tensor([[-0.7894, -0.4610], [-0.2343, 0.9186], [-0.2191, 0.2018]])
    assert torch.all(symplectic_integrator.sample_spins() == torch.Tensor([[-1, -1], [-1, 1], [-1, 1]]))

def test_momentum_update():
    symplectic_integrator = SymplecticIntegrator((3, 2), OptimizerMode.BALLISTIC, torch.float32, 'cpu')
    symplectic_integrator.momentum = torch.Tensor([[-0.7894, -0.4610], [-0.2343, 0.9186], [-0.2191, 0.2018]])
    symplectic_integrator.position = torch.Tensor([[-0.4869, 0.5873], [0.8815, -0.7336], [0.8692, 0.1872]])
    symplectic_integrator.momentum_update(.2)
    assert torch.all(torch.abs(symplectic_integrator.momentum - torch.Tensor([[-0.8868, -0.3435], [-0.0580, 0.7719], [-0.0453, 0.2392]])) < 1e-4)

def test_position_update():
    symplectic_integrator = SymplecticIntegrator((3, 2), OptimizerMode.BALLISTIC, torch.float32, 'cpu')
    symplectic_integrator.momentum = torch.Tensor([[-0.7894, -0.4610], [-0.2343, 0.9186], [-0.2191, 0.2018]])
    symplectic_integrator.position = torch.Tensor([[-0.4869, 0.5873], [0.8815, -0.7336], [0.8692, 0.1872]])
    symplectic_integrator.position_update(.2)
    assert torch.all(torch.abs(symplectic_integrator.position - torch.Tensor([[-0.6448, 0.4951], [0.8346, -0.5499], [0.8254, 0.2276]])) < 1e-4)

def test_quadratic_position_update():
    symplectic_integrator = SymplecticIntegrator((3, 2), OptimizerMode.BALLISTIC, torch.float32, 'cpu')
    symplectic_integrator.momentum = torch.Tensor([[-0.7894, -0.4610], [-0.2343, 0.9186], [-0.2191, 0.2018]])
    symplectic_integrator.position = torch.Tensor([[-0.4869, 0.5873], [0.8815, -0.7336], [0.8692, 0.1872]])
    symplectic_integrator.quadratic_position_update(.2, torch.Tensor([[0, .2, .3], [.2, 0, .1], [.3, .1, 0]]))
    assert torch.all(torch.abs(symplectic_integrator.position - torch.Tensor([[-0.5094, 0.6362], [0.8455, -0.7480], [0.8171, 0.1779]])) < 1e-4)

def test_inelastic_walls_simulation():
    symplectic_integrator = SymplecticIntegrator((3, 2), OptimizerMode.BALLISTIC, torch.float32, 'cpu')
    symplectic_integrator.momentum = torch.Tensor([[-2.7894, -0.4610], [-1.2343, 1.9186], [-0.2191, 0.2018]])
    symplectic_integrator.position = torch.Tensor([[-0.4869, 0.5873], [0.8815, -0.7336], [0.8692, 0.1872]])
    symplectic_integrator.simulate_inelastic_walls()
    assert torch.all(torch.abs(symplectic_integrator.momentum - torch.Tensor([[-1, -0.4610], [-1, 1], [-0.2191, 0.2018]])) < 1e-4)
    assert torch.all(torch.abs(symplectic_integrator.position - torch.Tensor([[0, 0.5873], [0, 0], [0.8692, 0.1872]])) < 1e-4)

def test_full_step():
    symplectic_integrator = SymplecticIntegrator((3, 2), OptimizerMode.BALLISTIC, torch.float32, 'cpu')
    symplectic_integrator.momentum = torch.Tensor([[-2.7894, -0.4610], [-1.2343, 1.9186], [-0.2191, 0.2018]])
    symplectic_integrator.position = torch.Tensor([[-0.4869, 0.5873], [0.8815, -0.7336], [0.8692, 0.1872]])
    symplectic_integrator.step(.2, .2, .2, torch.Tensor([[0, .2, .3], [.2, 0, .1], [.3, .1, 0]]))
    assert torch.all(torch.abs(symplectic_integrator.momentum - torch.Tensor([[-1, -0.3435], [-1, 1], [-0.0453,  0.2392]])) < 1e-4)
    assert torch.all(torch.abs(symplectic_integrator.position - torch.Tensor([[0, 0.6038], [0, 0], [0.6658, 0.2449]])) < 1e-2)

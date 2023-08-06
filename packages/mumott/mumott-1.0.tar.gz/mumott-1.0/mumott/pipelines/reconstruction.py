import logging

import numpy as np

from ..data_handling import DataContainer
from ..data_handling.utilities import get_absorbances
from ..methods.basis_sets import TrivialBasis, SphericalHarmonics
from ..methods.residual_calculators import GradientResidualCalculator
from ..methods.projectors import SAXSProjectorCUDA, SAXSProjectorNumba
from ..methods.utilities import get_sirt_weights, get_sirt_preconditioner
from ..optimization.loss_functions import SquaredLoss
from ..optimization.optimizers import GradientDescent, LBFGS
from ..optimization.regularizers import Laplacian

logger = logging.getLogger(__name__)


def run_sirt(data_container: DataContainer,
             use_absorbances: bool = True,
             use_gpu: bool = False,
             maxiter: int = 20,
             ftol: float = None,
             **kwargs):
    """A reconstruction pipeline for the :term:`SIRT` algorithm, which uses
    a gradient preconditioner and a set of weights for the projections
    to achieve fast convergence.

    Parameters
    ----------
    data_container
        The data container from loading the data set of interst.
    use_absorbances
        If ``True``, the reconstruction will use the absorbances
        calculated from the diode, or absorbances provided via a keyword argument.
        If ``False``, the data in :attr:`data_container.data` will be used.
    use_gpu
        Whether to use GPU resources in computing the projections.
        Default is ``False``. If set to ``True``, the method will use
        :class:`SAXSProjectorCUDA <mumott.methods.projectors.SAXSProjectorCUDA>`.
    maxiter
        Maximum number of iterations for the gradient descent solution.
    ftol
        Tolerance for the change in the loss function. Default is ``None``,
        in which case the reconstruction will terminate once the maximum
        number of iterations have been performed.
    kwargs
        Miscellaneous keyword arguments. See notes for details.

    Notes
    -----
    Many options can be specified through ``kwargs``. These include:

        Projector
            The :ref:`projector class <projectors>` to use.
        preconditioner_cutoff
            The cutoff to use when computing the :term:`SIRT` preconditioner.
            Default value is ``0.75 * len(data_container.geometry)``,
            which will lead to a roughly ellipsoidal mask.
        weights_cutoff
            The cutoff to use when computing the :term:`SIRT` weights.
            Default value is ``0.75 * data_container.geometry.volume_shape.mean()``,
            which will clip some projection edges.
        absorbances
            If :attr:`use_absorbances` is set to ``True``, these absorbances
            will be used instead of ones calculated from the diode.
        BasisSet
            The :ref:`basis set class <basis_sets>` to use. If not provided
            :class:`TrivialBasis <mumott.methods.basis_sets.TrivialBasis>`
            will be used for absorbances and
            :class:`SphericalHarmonics <mumott.methods.basis_sets.SphericalHarmonics>`
            for other data.
        basis_set_kwargs
            Keyword arguments for :attr:`BasisSet`.
        ResidualCalculator
            The :ref:`residual calculator class <residual_calculators>` to use.
            If not provided, then
            :class:`GradientResidualCalculator
            <mumott.methods.residual_calculators.GradientResidualCalculator>`
            will be used.
        residual_calculator_kwargs
            Keyword arguments for :attr:`ResidualCalculator`.
        LossFunction
            The :ref:`loss function class <loss_functions>` to use. If not provided
            :class:`SquaredLoss <mumott.optimization.loss_functions.SquaredLoss>`
            will be used.
        loss_function_kwargs
            Keyword arguments for :attr:`LossFunction`.
        Regularizers
            A list of dictionaries with three entries, a name
            (``str``), a :ref:`regularizer object <regularizers>`, and
            a regularization weight (``float``); used by
            :func:`loss_function.add_regularizer()
            <mumott.optimization.loss_functions.SquaredLoss.add_regularizer>`.
        Optimizer
            The optimizer class to use. If not provided
            :class:`GradientDescent <mumott.optimization.optimizers.GradientDescent>`
            will be used.
        optimizer_kwargs
            Keyword arguments for :attr:`Optimizer`.

    """
    if 'Projector' in kwargs:
        Projector = kwargs.pop('Projector')
    else:
        if use_gpu:
            Projector = SAXSProjectorCUDA
        else:
            Projector = SAXSProjectorNumba
    projector = Projector(data_container.geometry)

    if 'preconditioner_cutoff' in kwargs:
        preconditioner_cutoff = kwargs.pop('preconditioner_cutoff')
    else:
        preconditioner_cutoff = 0.75 * len(data_container.geometry)
    if 'weights_cutoff' in kwargs:
        weights_cutoff = kwargs.pop('weights_cutoff')
    else:
        weights_cutoff = 0.75 * data_container.geometry.volume_shape.mean()
    preconditioner = get_sirt_preconditioner(projector, cutoff=preconditioner_cutoff)
    sirt_weights = get_sirt_weights(projector, cutoff=weights_cutoff)

    # Save previous weights to avoid accumulation.
    old_weights = data_container.projections.weights.copy()
    # Respect previous masking in data container
    data_container.projections.weights = sirt_weights * np.ceil(data_container.projections.weights)

    if use_absorbances:
        if 'absorbances' in kwargs:
            absorbances = kwargs.pop('absorbances')
        else:
            abs_dict = get_absorbances(data_container.diode, normalize_per_projection=True)
            absorbances = abs_dict['absorbances']
            transmittivity_cutoff_mask = abs_dict['cutoff_mask']
            data_container.projections.weights *= transmittivity_cutoff_mask
    else:
        absorbances = None

    if 'basis_set_kwargs' in kwargs:
        basis_set_kwargs = kwargs.pop('basis_set_kwargs')
    else:
        basis_set_kwargs = dict()
    if 'BasisSet' in kwargs:
        BasisSet = kwargs.pop('BasisSet')
    else:
        if use_absorbances:
            BasisSet = TrivialBasis
            if 'channels' not in basis_set_kwargs:
                basis_set_kwargs['channels'] = 1
        else:
            # ell_max from largest even number smaller than the number of segments.
            if 'ell_max' not in basis_set_kwargs:
                basis_set_kwargs['ell_max'] = 2 * ((data_container.data.shape[-1] - 1) // 2)
            BasisSet = SphericalHarmonics

    basis_set = BasisSet(**basis_set_kwargs)

    if 'ResidualCalculator' in kwargs:
        ResidualCalculator = kwargs.pop('ResidualCalculator')
    else:
        ResidualCalculator = GradientResidualCalculator
    if 'residual_calculator_kwargs' in kwargs:
        residual_calculator_kwargs = kwargs.pop('residual_calculator_kwargs')
    else:
        residual_calculator_kwargs = dict()
    if 'use_scalar_projections' not in residual_calculator_kwargs:
        residual_calculator_kwargs['use_scalar_projections'] = use_absorbances
    if 'scalar_projections' not in residual_calculator_kwargs:
        residual_calculator_kwargs['scalar_projections'] = absorbances
    residual_calculator = ResidualCalculator(data_container,
                                             basis_set,
                                             projector,
                                             **residual_calculator_kwargs)

    if 'Regularizers' in kwargs:
        Regularizers = kwargs.pop('Regularizers')
    else:
        Regularizers = []

    if 'LossFunction' in kwargs:
        LossFunction = kwargs.pop('LossFunction')
    else:
        LossFunction = SquaredLoss
    if 'loss_function_kwargs' in kwargs:
        loss_function_kwargs = kwargs.pop('loss_function_kwargs')
    else:
        loss_function_kwargs = dict()
    if 'use_weights' not in loss_function_kwargs:
        loss_function_kwargs['use_weights'] = True
    if 'preconditioner' not in loss_function_kwargs:
        loss_function_kwargs['preconditioner'] = preconditioner

    loss_function = LossFunction(residual_calculator,
                                 **loss_function_kwargs)

    for reg in Regularizers:
        loss_function.add_regularizer(**reg)

    if 'Optimizer' in kwargs:
        Optimizer = kwargs.pop('Optimizer')
    else:
        Optimizer = GradientDescent
    if 'optimizer_kwargs' in kwargs:
        optimizer_kwargs = kwargs.pop('optimizer_kwargs')
    else:
        optimizer_kwargs = dict()
    if 'maxiter' not in optimizer_kwargs:
        optimizer_kwargs['maxiter'] = maxiter
    if 'ftol' not in optimizer_kwargs:
        optimizer_kwargs['ftol'] = ftol
    optimizer = Optimizer(loss_function,
                          **optimizer_kwargs)

    # Catch KeyboardInterrupt so we can return partial results and restore data_container state
    try:
        result = optimizer.optimize()
    except KeyboardInterrupt:
        logger.info('Optimization interrupted, returning partial result...')
        result = dict(x=residual_calculator.coefficients.copy())

    weights = data_container.weights.copy()
    data_container.projections.weights = old_weights

    return dict(result=result, optimizer=optimizer, loss_function=loss_function,
                residual_calculator=residual_calculator, basis_set=basis_set, projector=projector,
                absorbances=absorbances, weights=weights)


def run_sigtt(data_container: DataContainer,
              use_gpu: bool = False,
              maxiter: int = 20,
              ftol: float = 1e-2,
              regularization_weight: float = 1e-4,
              **kwargs):
    """A reconstruction pipeline for the :term:`SIGTT` algorithm, which uses
    a gradient and a regularizer to accomplish reconstruction.

    Parameters
    ----------
    data_container
        The data container from loading the data set of interest.
    use_gpu
        Whether to use GPU resources in computing the projections.
        Default is ``False``. If set to ``True``, the method will use
        :class:`SAXSProjectorCUDA <mumott.methods.projectors.SAXSProjectorCUDA>`.
    maxiter
        Maximum number of iterations for the gradient descent solution.
    ftol
        Tolerance for the change in the loss function. Default is ``None``,
        in which case the reconstruction will terminate once the maximum
        number of iterations have been performed.
    regularization_weight
        Regularization weight for the default
        :class:`Laplacian <mumott.optimization.regularizers.Laplacian>` regularizer.
        Ignored if a loss function is provided.
    kwargs
        Miscellaneous keyword arguments. See notes for details.

    Notes
    -----
    Many options can be specified through :attr:`kwargs`. Miscellaneous ones are passed to the optimizer.
    Specific keywords include:

        Projector
            The :ref:`projector class <projectors>` to use.
        BasisSet
            The :ref:`basis set class <basis_sets>` to use. If not provided
            :class:`SphericalHarmonics <mumott.methods.basis_sets.SphericalHarmonics>`
            will be used.
        basis_set_kwargs
            Keyword arguments for :attr:`BasisSet`.
        ResidualCalculator
            The :ref:`residual_calculator class <residual_calculators>` to use. If not provided
            :class:`GradientResidualCalculator
            <mumott.methods.residual_calculators.GradientResidualCalculator>`
            will be used.
        residual_calculator_kwargs
            Keyword arguments for :attr:`ResidualCalculator`.
        LossFunction
            The :ref:`loss function class <loss_functions>` to use. If not provided
            :class:`SquaredLoss <mumott.optimization.loss_functions.SquaredLoss>`
            will be used.
        loss_function_kwargs
            Keyword arguments for :attr:`LossFunction`.
        Regularizers
            A list of dictionaries with three entries, a name
            (``str``), a :ref:`regularizer object <regularizers>`, and
            a regularization weight (``float``); used by
            :func:`loss_function.add_regularizer()
            <mumott.optimization.loss_functions.SquaredLoss.add_regularizer>`.
            By default, a :class:`Laplacian
            <mumott.optimization.regularizers.Laplacian>` with the
            weight :attr:`regularization_weight` will be used. If
            other regularizers are specified, this will be overridden.
        Optimizer
            The :ref:`optimizer class <optimizers>` to use. If not provided
            :class:`LBFGS <mumott.optimization.optimizers.LBFGS>` will be used.
        optimizer_kwargs
            Keyword arguments for :attr:`Optimizer`.

    """
    if 'Projector' in kwargs:
        Projector = kwargs.pop('Projector')
    else:
        if use_gpu:
            Projector = SAXSProjectorCUDA
        else:
            Projector = SAXSProjectorNumba
    projector = Projector(data_container.geometry)

    if 'basis_set_kwargs' in kwargs:
        basis_set_kwargs = kwargs.pop('basis_set_kwargs')
    else:
        basis_set_kwargs = dict()
    if 'BasisSet' in kwargs:
        BasisSet = kwargs.pop('BasisSet')
    else:
        if 'ell_max' not in basis_set_kwargs:
            basis_set_kwargs['ell_max'] = 2 * ((data_container.data.shape[-1] - 1) // 2)
        BasisSet = SphericalHarmonics
    basis_set = BasisSet(**basis_set_kwargs)

    if 'ResidualCalculator' in kwargs:
        ResidualCalculator = kwargs.pop('ResidualCalculator')
    else:
        ResidualCalculator = GradientResidualCalculator
    if 'residual_calculator_kwargs' in kwargs:
        residual_calculator_kwargs = kwargs.pop('residual_calculator_kwargs')
    else:
        residual_calculator_kwargs = dict()
    residual_calculator = ResidualCalculator(data_container,
                                             basis_set,
                                             projector,
                                             **residual_calculator_kwargs)

    if 'Regularizers' in kwargs:
        Regularizers = kwargs.pop('Regularizers')
    else:
        Regularizers = [dict(name='laplacian',
                        regularizer=Laplacian(),
                        regularization_weight=regularization_weight)]
    if 'LossFunction' in kwargs:
        LossFunction = kwargs.pop('LossFunction')
    else:
        LossFunction = SquaredLoss
    if 'loss_function_kwargs' in kwargs:
        loss_function_kwargs = kwargs.pop('loss_function_kwargs')
    else:
        loss_function_kwargs = dict()
    loss_function = LossFunction(residual_calculator,
                                 **loss_function_kwargs)
    for reg in Regularizers:
        loss_function.add_regularizer(**reg)

    if 'Optimizer' in kwargs:
        Optimizer = kwargs.pop('Optimizer')
    else:
        Optimizer = LBFGS
    if 'optimizer_kwargs' in kwargs:
        optimizer_kwargs = kwargs.pop('optimizer_kwargs')
    else:
        optimizer_kwargs = dict()
    if 'maxiter' not in optimizer_kwargs:
        optimizer_kwargs['maxiter'] = maxiter
    if 'ftol' not in optimizer_kwargs:
        optimizer_kwargs['ftol'] = ftol
    optimizer = Optimizer(loss_function,
                          **optimizer_kwargs)

    try:
        result = optimizer.optimize()
    except KeyboardInterrupt:
        logger.info('Optimization interrupted, returning partial result...')
        result = dict(x=residual_calculator.coefficients.copy())

    return dict(result=result, optimizer=optimizer, loss_function=loss_function,
                residual_calculator=residual_calculator, basis_set=basis_set, projector=projector)

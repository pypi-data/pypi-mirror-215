import numpy as np
from decimal import Decimal
from warnings import warn

"""Adapted from numpy-financial package: https://github.com/numpy/numpy-financial
"""


def irr(values, guess=0.1, tol=1e-12, maxiter=100):
    """
    Return the Internal Rate of Return (IRR).
    This is the "average" periodically compounded rate of return
    that gives a net present value of 0.0; for a more complete explanation,
    see Notes below.
    :class:`decimal.Decimal` type is not supported.
    Parameters
    ----------
    values : array_like, shape(N,)
        Input cash flows per time period.  By convention, net "deposits"
        are negative and net "withdrawals" are positive.  Thus, for
        example, at least the first element of `values`, which represents
        the initial investment, will typically be negative.
    guess : float, optional
        Initial guess of the IRR for the iterative solver. If no guess is
        given an initial guess of 0.1 (i.e. 10%) is assumed instead.
    tol : float, optional
        Required tolerance to accept solution. Default is 1e-12.
    maxiter : int, optional
        Maximum iterations to perform in finding a solution. Default is 100.
    Returns
    -------
    out : float
        Internal Rate of Return for periodic input values.
    Notes
    -----
    The IRR is perhaps best understood through an example (illustrated
    using np.irr in the Examples section below). Suppose one invests 100
    units and then makes the following withdrawals at regular (fixed)
    intervals: 39, 59, 55, 20.  Assuming the ending value is 0, one's 100
    unit investment yields 173 units; however, due to the combination of
    compounding and the periodic withdrawals, the "average" rate of return
    is neither simply 0.73/4 nor (1.73)^0.25-1.  Rather, it is the solution
    (for :math:`r`) of the equation:
    .. math:: -100 + \\frac{39}{1+r} + \\frac{59}{(1+r)^2}
     + \\frac{55}{(1+r)^3} + \\frac{20}{(1+r)^4} = 0
    In general, for `values` :math:`= [v_0, v_1, ... v_M]`,
    irr is the solution of the equation: [G]_
    .. math:: \\sum_{t=0}^M{\\frac{v_t}{(1+irr)^{t}}} = 0
    References
    ----------
    .. [G] L. J. Gitman, "Principles of Managerial Finance, Brief," 3rd ed.,
       Addison-Wesley, 2003, pg. 348.
    Examples
    --------
    >>> round(irr([-100, 39, 59, 55, 20]), 5)
    0.28095
    >>> round(irr([-100, 0, 0, 74]), 5)
    -0.0955
    >>> round(irr([-100, 100, 0, -7]), 5)
    -0.0833
    >>> round(irr([-100, 100, 0, 7]), 5)
    0.06206
    >>> round(irr([-5, 10.5, 1, -8, 1]), 5)
    0.0886
    """
    values = np.atleast_1d(values)
    if values.ndim != 1:
        raise ValueError("Cashflows must be a rank-1 array")

    # If all values are of the same sign no solution exists
    # we don't perform any further calculations and exit early
    same_sign = np.all(values > 0) if values[0] > 0 else np.all(values < 0)
    if same_sign:
        warn("Given values are all of the same sign, no IRR solution exists")
        return np.nan

    # We aim to solve eirr such that NPV is exactly zero. This can be framed as
    # simply finding the closest root of a polynomial to a given initial guess
    # as follows:
    #           V0           V1           V2           V3
    # NPV = ---------- + ---------- + ---------- + ---------- + ...
    #       (1+eirr)^0   (1+eirr)^1   (1+eirr)^2   (1+eirr)^3
    #
    # by letting x = 1 / (1+eirr), we substitute to get
    #
    # NPV = V0 * x^0   + V1 * x^1   +  V2 * x^2  +  V3 * x^3  + ...
    #
    # which we solve using Newton-Raphson and then reverse out the solution
    # as eirr = 1/x - 1 (if we are close enough to a solution)
    npv_ = np.polynomial.Polynomial(values)
    d_npv = npv_.deriv()
    x = 1 / (1 + guess)

    for _ in range(maxiter):
        x_new = x - (npv_(x) / d_npv(x))
        if abs(x_new - x) < tol:
            return 1 / x_new - 1
        x = x_new

    return np.nan


def npv(rate, values):
    """
    Returns the NPV (Net Present Value) of a cash flow series.
    Parameters
    ----------
    rate : scalar
        The discount rate.
    values : array_like, shape(M, )
        The values of the time series of cash flows.  The (fixed) time
        interval between cash flow "events" must be the same as that for
        which `rate` is given (i.e., if `rate` is per year, then precisely
        a year is understood to elapse between each cash flow event).  By
        convention, investments or "deposits" are negative, income or
        "withdrawals" are positive; `values` must begin with the initial
        investment, thus `values[0]` will typically be negative.
    Returns
    -------
    out : float
        The NPV of the input cash flow series `values` at the discount
        `rate`.
    Warnings
    --------
    ``npv`` considers a series of cash_flows starting in the present (t = 0).
    NPV can also be defined with a series of future cash_flows, paid at the
    end, rather than the start, of each period. If future cash_flows are used,
    the first cash_flow `values[0]` must be zeroed and added to the net
    present value of the future cash_flows. This is demonstrated in the
    examples.
    Notes
    -----
    Returns the result of: [G]_
    .. math :: \\sum_{t=0}^{M-1}{\\frac{values_t}{(1+rate)^{t}}}
    References
    ----------
    .. [G] L. J. Gitman, "Principles of Managerial Finance, Brief," 3rd ed.,
       Addison-Wesley, 2003, pg. 346.
    Examples
    --------
    >>> import numpy as np
    Consider a potential project with an initial investment of $40 000 and
    projected cash_flows of $5 000, $8 000, $12 000 and $30 000 at the end of
    each period discounted at a rate of 8% per period. To find the project's
    net present value:
    >>> rate, cash_flows = 0.08, [-40_000, 5_000, 8_000, 12_000, 30_000]
    >>> np.round(npv(rate, cash_flows), 5)
    3065.22267
    It may be preferable to split the projected cash_flow into an initial
    investment and expected future cash_flows. In this case, the value of
    the initial cash_flow is zero and the initial investment is later added
    to the future cash_flows net present value:
    >>> initial_cash_flow = cash_flows[0]
    >>> cash_flows[0] = 0
    >>> np.round(npv(rate, cash_flows) + initial_cash_flow, 5)
    3065.22267
    """
    values = np.atleast_2d(values)
    timestep_array = np.arange(0, values.shape[1])
    npv_ = (values / (1 + rate) ** timestep_array).sum(axis=1)
    try:
        # If size of array is one, return scalar
        return npv_.item()
    except ValueError:
        # Otherwise, return entire array
        return npv_


def mirr(values, finance_rate, reinvest_rate):
    """
    Modified internal rate of return.
    Parameters
    ----------
    values : array_like
        Cash flows (must contain at least one positive and one negative
        value) or nan is returned.  The first value is considered a sunk
        cost at time zero.
    finance_rate : scalar
        Interest rate paid on the cash flows
    reinvest_rate : scalar
        Interest rate received on the cash flows upon reinvestment
    Returns
    -------
    out : float
        Modified internal rate of return
    """
    values = np.asarray(values)
    n = values.size

    # Without this explicit cast the 1/(n - 1) computation below
    # becomes a float, which causes TypeError when using Decimal
    # values.
    if isinstance(finance_rate, Decimal):
        n = Decimal(n)

    pos = values > 0
    neg = values < 0
    if not (pos.any() and neg.any()):
        return np.nan
    numer = np.abs(npv(reinvest_rate, values * pos))
    denom = np.abs(npv(finance_rate, values * neg))
    return (numer / denom) ** (1 / (n - 1)) * (1 + reinvest_rate) - 1

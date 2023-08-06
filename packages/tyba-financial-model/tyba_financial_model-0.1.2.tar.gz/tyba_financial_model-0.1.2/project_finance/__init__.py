import numpy as np
from pydantic import BaseModel, root_validator, validator
from project_finance import finance
import typing as t


valid_frequencies = {"annual": 1, "monthly": 12, "quarterly": 4}


def cash_flow(capex: float, opex: np.ndarray, revenue: np.ndarray) -> np.ndarray:
    """Build cash_flow array

    :param capex: total project capital expenditures, in $
    :param opex: series of operating expenses for each period, in $
    :param revenue: series of revenue generated for each period in $
    :return: series of cash_flow values

    - Positive sign assumed for all arguments
    - Cashflows are assumed to occur at the end of the period, i.e. the capital expenditures are assumed to occur at the
    end of period "0", and revenue and operating expenses first hit the project account at the end of year 1, etc.

    :meta private:
    """

    return np.array([-capex] + (revenue - opex).tolist())


class BaseFinanceInputs(BaseModel):
    """_"""

    frequency: str

    class Config:
        arbitrary_types_allowed = True

    @validator("frequency")
    def check_freq(cls, v):
        assert (
            v in valid_frequencies
        ), f"frequency must be one of {list(valid_frequencies.keys())}"
        return v

    def get_cash_flow(self) -> np.ndarray:
        return cash_flow(capex=self.capex, opex=self.opex, revenue=self.revenue)


class SolarInputs(BaseModel):
    """_"""

    array_capacity_wdc: float
    capex_cost_per_wdc: float = 0.80
    opex_cost_per_wdc: float = 0.01

    @property
    def capex(self):
        return self.array_capacity_wdc * self.capex_cost_per_wdc

    def _opex_per_period(self, periods_per_year):
        return self.array_capacity_wdc * self.opex_cost_per_wdc / periods_per_year


class SolarFinanceInputs(BaseFinanceInputs, SolarInputs):
    """_"""

    revenue: np.ndarray

    @property
    def opex(self):
        return np.array(
            [self._opex_per_period(valid_frequencies[self.frequency])]
            * len(self.revenue)
        )


class StorageInputs(BaseModel):
    """_"""

    capacity_kwh: float
    capex_cost_per_kwh: float = 200.00
    opex_cost_per_kwh: float = 7.00

    @property
    def capex(self):
        return self.capacity_kwh * self.capex_cost_per_kwh

    def _opex_per_period(self, periods_per_year):
        return self.capacity_kwh * self.opex_cost_per_kwh / periods_per_year


class StorageFinanceInputs(BaseFinanceInputs, StorageInputs):
    """_"""

    revenue: np.ndarray

    @property
    def opex(self):
        return np.array(
            [self._opex_per_period(valid_frequencies[self.frequency])]
            * len(self.revenue)
        )


class HybridFinanceInputsSingleRev(BaseFinanceInputs):
    """_"""

    revenue: np.ndarray
    solar: SolarInputs
    storage: StorageInputs

    @property
    def capex(self):
        return self.solar.capex + self.storage.capex

    @property
    def opex(self):
        return np.array(
            [
                self.solar._opex_per_period(valid_frequencies[self.frequency])
                + self.storage._opex_per_period(valid_frequencies[self.frequency])
            ]
            * len(self.revenue)
        )


class HybridFinanceInputs(BaseModel):
    """_"""

    solar: SolarFinanceInputs
    storage: StorageFinanceInputs

    @root_validator(skip_on_failure=True)
    def check_revs_and_freqs(cls, values):
        try:
            assert len(values["solar"].revenue) == len(values["storage"].revenue)
            assert values["solar"].frequency == values["storage"].frequency
        except AssertionError:
            raise AssertionError(
                "solar and storage revenue inputs must have the same frequency and length"
            )
        return values

    @property
    def capex(self):
        return self.solar.capex + self.storage.capex

    @property
    def opex(self):
        return self.solar.opex + self.storage.opex

    @property
    def revenue(self):
        return self.solar.revenue + self.storage.revenue

    @property
    def frequency(self):
        return self.solar.frequency

    def get_cash_flow(self) -> np.ndarray:
        return cash_flow(capex=self.capex, opex=self.opex, revenue=self.revenue)


def npv(
    inputs: t.Union[BaseFinanceInputs, HybridFinanceInputs],
    annual_discount_rate: float,
) -> float:
    """Net Present Value

    :param inputs: BaseFinanceInputs
    :param annual_discount_rate: in decimal
    :return: net present value in $
    """

    return finance.npv(
        rate=annual_discount_rate / valid_frequencies[inputs.frequency],
        values=inputs.get_cash_flow(),
    )


class HybridDetailResults(BaseModel):
    """_"""

    solar: float
    storage: float
    project: float


def hybrid_detailed_npv(
    inputs: HybridFinanceInputs, annual_discount_rate: float
) -> HybridDetailResults:
    """Net Present Value

    :param inputs: HybridDetailFinanceInputs
    :param annual_discount_rate: in decimal
    :return: HybridDetailResults object containing net present values in $
    """
    return HybridDetailResults(
        solar=npv(inputs=inputs.solar, annual_discount_rate=annual_discount_rate),
        storage=npv(inputs=inputs.storage, annual_discount_rate=annual_discount_rate),
        project=npv(inputs=inputs, annual_discount_rate=annual_discount_rate),
    )


def irr(
    inputs: t.Union[BaseFinanceInputs, HybridFinanceInputs],
    guess: float = 0.1,
    tol: float = 1e-12,
    maxiter: int = 100,
) -> float:
    """Internal Rate of Return

    :param inputs: BaseFinanceInputs
    :param guess: initial guess of the IRR for the iterative solver
    :param tol: required tolerance to accept solution
    :param maxiter: maximum iterations to perform in finding a solution
    :return: average rate of return for given revenue, capex and opex in decimal form
    """
    return finance.irr(
        values=inputs.get_cash_flow(), guess=guess, tol=tol, maxiter=maxiter
    )


def hybrid_detailed_irr(
    inputs: HybridFinanceInputs,
    guess: float = 0.1,
    tol: float = 1e-12,
    maxiter: int = 100,
) -> HybridDetailResults:
    """Internal Rate of Return

    :param inputs: HybridDetailFinanceInputs object that contains solar and storage attributes, each with their own
        revenue: series of revenue generated for each period in $ and an associated frequency
        capex: total project capital expenditures, in $
        annual_opex: annual operating expenses, assumed constant for all years, in $
    :param guess: initial guess of the IRR for the iterative solver
    :param tol: required tolerance to accept solution
    :param maxiter: maximum iterations to perform in finding a solution
    :return: HybridDetailResults object containing average rates of return
    """
    return HybridDetailResults(
        solar=irr(inputs=inputs.solar, guess=guess, tol=tol, maxiter=maxiter),
        storage=irr(inputs=inputs.storage, guess=guess, tol=tol, maxiter=maxiter),
        project=irr(inputs=inputs, guess=guess, tol=tol, maxiter=maxiter),
    )

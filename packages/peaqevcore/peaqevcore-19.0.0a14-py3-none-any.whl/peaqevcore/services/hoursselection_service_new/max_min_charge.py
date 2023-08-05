from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import datetime, timedelta

if TYPE_CHECKING:
    from .hourselection_service import HourSelectionService
from typing import Tuple
from .models.max_min_model import MaxMinModel

MINIMUM_DIFFERENCE = 0.1


class MaxMinCharge:
    def __init__(self, service: HourSelectionService, min_price: float | None) -> None:
        self.model = MaxMinModel(min_price=min_price)
        self.parent = service
        self.active: bool = False

    @property
    def total_charge(self) -> float:
        return self.model.total_charge

    @property
    def average_price(self) -> float | None:
        return self.model.average_price

    @property
    def original_total_charge(self) -> float:
        return sum(
            [
                hp.permittance * self.model.expected_hourly_charge
                for hp in self.parent.future_hours
            ]
        )

    @property
    def non_hours(self) -> list:
        print(self.parent.dtmodel.dt)
        return [
            k
            for k, v in self.model.input_hours.items()
            if v[1] == 0 and k >= self.parent.dtmodel.dt
        ]

    @property
    def dynamic_caution_hours(self) -> dict:
        return {
            k: v[1]
            for k, v in self.model.input_hours.items()
            if 0 < v[1] < 1 and k >= self.parent.dtmodel.dt
        }

    async def async_allow_decrease(self, car_connected: bool | None = None) -> bool:
        if car_connected is not None:
            return all(
                [
                    not car_connected,
                    len([k for k, v in self.model.input_hours.items() if v[1] > 0])
                    != 1,
                ]
            )
        return len([k for k, v in self.model.input_hours.items() if v[1] > 0]) != 1

    async def async_update(
        self,
        avg24,
        peak,
        max_desired: float,
        session_energy: float | None = None,
        car_connected: bool | None = None,
    ) -> None:
        allow_decrease: bool = False
        if await self.async_allow_decrease(car_connected):
            allow_decrease = True
            await self.async_setup(max_charge=peak)
        _session = session_energy or 0
        _desired = max_desired - _session
        _avg24 = round((avg24 / 1000), 1)
        self.model.expected_hourly_charge = peak - _avg24
        await self.async_increase_decrease(_desired, _avg24, peak, allow_decrease)

    async def async_increase_decrease(
        self, desired, avg24, peak, allow_decrease: bool
    ) -> None:
        for i in range(len(self.model.original_input_hours.items())):
            _load = self.total_charge - desired
            if _load > MINIMUM_DIFFERENCE and allow_decrease:
                await self.async_decrease()
            elif _load < MINIMUM_DIFFERENCE * -1:
                expected_charge = (desired - self.total_charge) / (peak - avg24)
                await self.async_increase(expected_charge)
            if abs(_load) < MINIMUM_DIFFERENCE:
                break

    async def async_initial_charge(self, avg24, peak) -> float:
        _avg24 = round((avg24 / 1000), 1)
        self.model.expected_hourly_charge = peak - _avg24
        total = 24 * (peak - _avg24)  # todo: fix 24 to be dynamic
        total -= len(self.non_hours) * (peak - _avg24)
        total -= sum(self.dynamic_caution_hours.values()) * (peak - _avg24)
        return total

    async def async_sum_charge(self, avg24, peak) -> float:
        total = 0
        for k, v in self.model.input_hours.items():
            total += (peak - avg24) * v[1]
        return total

    async def async_decrease(self):
        max_key = max(
            self.model.input_hours,
            key=lambda k: self.model.input_hours[k][0]
            if self.model.input_hours[k][1] != 0
            and self.model.input_hours[k][0] > self.model.min_price
            else -1,
        )
        self.model.input_hours[max_key] = (self.model.input_hours[max_key][0], 0)

    async def async_increase(self, expected_charge):
        min_key = min(
            self.model.input_hours,
            key=lambda k: self.model.input_hours[k][0]
            if self.model.input_hours[k][1] < 1
            and self.model.original_input_hours[k][1] > 0
            else 999,
        )
        self.model.input_hours[min_key] = (
            self.model.input_hours[min_key][0],
            min(min(1, expected_charge), self.model.original_input_hours[min_key][1]),
        )

    async def async_setup(
        self,
        max_charge: float,
        non_hours: list | None = None,
        dynamic_caution_hours: dict | None = None,
        prices: list | None = None,
        prices_tomorrow: list | None = None,
    ) -> None:
        if max_charge == 0:
            self.active = False
            return
        hour = self.parent.dtmodel.hour
        dt = self.parent.dtmodel.dt
        _non_hours = self.parent.non_hours if non_hours is None else non_hours
        _dynamic_caution_hours = (
            self.parent.dynamic_caution_hours
            if dynamic_caution_hours is None
            else dynamic_caution_hours
        )
        _prices = self.parent.model.prices_today if prices is None else prices
        _prices_tomorrow = (
            self.parent.model.prices_tomorrow
            if prices_tomorrow is None
            else prices_tomorrow
        )
        ret_today, ret_tomorrow = await self.async_loop_nonhours(
            dt, _non_hours, _prices, _prices_tomorrow
        )
        await self.async_loop_caution_hours(
            dt,
            _dynamic_caution_hours,
            _prices,
            _prices_tomorrow,
            ret_today,
            ret_tomorrow,
        )
        await self.async_add_available_hours(
            dt, _prices, _prices_tomorrow, ret_today, ret_tomorrow
        )
        self.model.input_hours = self._sort_dicts(ret_today, ret_tomorrow)
        self.model.original_input_hours = self.model.input_hours.copy()
        self.active = True

    @staticmethod
    async def async_add_available_hours(
        dt: datetime,
        prices: list,
        prices_tomorrow: list,
        ret_today: dict,
        ret_tomorrow: dict,
    ) -> None:
        _hour = dt.hour
        _range = (
            len(prices) - dt.hour + len(prices_tomorrow)
            if len(prices_tomorrow) > 0
            else len(prices) - dt.hour
        )

        for i in range(_range):
            if _hour < dt.hour and _hour not in ret_tomorrow.keys():
                ret_tomorrow[
                    (dt + timedelta(days=1))
                    .replace(hour=_hour)
                    .replace(minute=0)
                    .replace(second=0)
                ] = (
                    prices_tomorrow[_hour],
                    1,
                )
                # todo: must test this without valid prices tomorrow.
            elif _hour >= dt.hour and _hour not in ret_today.keys():
                ret_today[dt.replace(hour=_hour)] = (prices[_hour], 1)
            _hour += 1
            if _hour > 23:
                _hour = 0

    @staticmethod
    async def async_loop_caution_hours(
        dt: datetime,
        caution_hours: dict,
        prices: list,
        prices_tomorrow: list,
        ret_today: dict,
        ret_tomorrow: dict,
    ) -> None:
        for k, v in caution_hours.items():
            if k.day == dt.day and k.hour >= dt.hour:
                ret_today[k] = (prices[k.hour], v)
            elif len(prices_tomorrow) > 0:
                ret_tomorrow[k] = (prices_tomorrow[k.hour], v)

    @staticmethod
    async def async_loop_nonhours(
        dt: datetime, non_hours: list, prices: list, prices_tomorrow: list
    ) -> Tuple[dict, dict]:
        ret_today = {}
        ret_tomorrow = {}
        for n in non_hours:
            if n.day == dt.day and n.hour >= dt.hour:
                ret_today[n] = (prices[n.hour], 0)
            elif len(prices_tomorrow) > 0:
                ret_tomorrow[n] = (prices_tomorrow[n.hour], 0)
        return ret_today, ret_tomorrow

    @staticmethod
    def _sort_dicts(ret_today: dict, ret_tomorrow: dict) -> dict:
        ret = {}
        for k in sorted(ret_today.keys()):
            ret[k] = ret_today[k]
        for k in sorted(ret_tomorrow.keys()):
            ret[k] = ret_tomorrow[k]
        return ret

import numpy as np
from dataclasses import dataclass, fields
from typing import Optional, Union
from telebot.types import Message
from fsm import cache_storage


@dataclass
class Results:
    hist_path_regions: Optional[str]
    comp_high_regions: Optional[Union[float, int]]
    comp_low_regions: Optional[Union[float, int]]
    comp_flat_max_regions: Optional[int]
    comp_flat_min_regions: Optional[int]
    comp_flat_av_regions: Optional[int]
    
    hist_path_streets: Optional[str]
    comp_high_streets: Optional[Union[float, int]]
    comp_low_streets: Optional[Union[float, int]]
    comp_flat_max_streets: Optional[int]
    comp_flat_min_streets: Optional[int]
    comp_flat_av_streets: Optional[int]
    
    min_flat_cost_price: Optional[int]
    max_flat_cost_price: Optional[int]
    av_flat_cost_price: Optional[int]
    
    av_flat_price: Optional[int]
    comb_results_max: Optional[int]
    comb_results_min: Optional[int]
    
    def values(self):
        return [getattr(self, field.name) for field in fields(self) \
            if getattr(self, field.name) is not None]

    @classmethod
    def merge_results(cls, *results_list: 'Results') -> 'Results':
        merged = cls()
        for result in results_list:
            for field in fields(cls):
                value = getattr(result, field.name)
                if value is not None:
                    setattr(merged, field.name, value)
        return merged


class ImmutableList(list):
    def __setitem__(self, key, value):
        raise TypeError("Cannot modify immutable list")

@dataclass 
class UserData:
    chosen_region_name: Optional[str]
    chosen_street_name: Optional[str]
    house_info1: Optional[str]
    house_info2: Optional[str]
    number_of_rooms: Optional[int]
    cac_age: Optional[int]
    area: Optional[Union[int, float]]
    price_of_finishing: Optional[Union[int, float]]
    repair_coef: Optional[Union[int, float]]
    furniture_cost: Optional[Union[int, float]]


@dataclass
class UserBid:
    user_link: str
    name: str
    surname: str
    phone: str

    @classmethod
    def from_message(cls, message: 'Message') -> 'UserBid':
        return cls(
            user_link=f'https://t.me/{message.from_user.username}',
            name=message.contact.first_name,
            surname=message.contact.last_name,
            phone=message.contact.phone_number
        )

    @classmethod
    def save_bid(cls, instance: 'UserBid', chat_id: int, user_id: int) -> None:
        param_dict = {}
        for field in fields(cls):
            value = getattr(instance, field.name)
            param_dict |= {field: value}
        cache_storage.set_value(user_id, chat_id, 'user_bid', param_dict)

    @classmethod
    def load_user_bid(cls, chat_id: int, user_id: int) -> 'UserBid':
        param_dict = cache_storage.get_value(user_id, chat_id, 'user_bid')
        if param_dict is None:
            raise ValueError("No data found in cache for the given user_id and chat_id")
        init_args = {field.name: param_dict.get(field.name) for field in fields(cls)}
        return cls(**init_args)


class CostCompDataClass:
    @property
    def comp_list(self) -> list:
        return self._comp_list_regions if self.regions else self._comp_list_streets

    @comp_list.setter
    def comp_list(self, value: list):
        if self.regions:
            self._comp_list_regions = value
        else:
            self._comp_list_streets = value


    @property
    def values(self) -> np.ndarray:
        if self.regions:
            return self.__set_values(self._comp_list_regions)
        return self.__set_values(self._comp_list_streets)


    def __set_values(self, comp_list:list) -> np.ndarray:
        return np.array(comp_list).sort()


    @property
    def regions(self) -> bool:
        return self._regions


    @regions.setter
    def regions(self, value: bool):
        self._regions = value


    def toggle_regions(self):
        self.regions = not self.regions

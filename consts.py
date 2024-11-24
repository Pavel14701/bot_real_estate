from dataclasses import dataclass, field
from decimal import Decimal
from typing import TypeVar

T = TypeVar('T')

@dataclass
class Consts:
    price_panel_brezh = field(default=(Decimal('625'), Decimal('675')), init=False)
    price_panel_hruzh = field(default=(Decimal('600'), Decimal('650')), init=False)
    price_panel_standart_project = field(default=(Decimal('700'), Decimal('725')), init=False)
    price_panel_upgrade = field(default=(Decimal('675'), Decimal('700')), init=False)
    price_brick_stalin = field(default=(Decimal('750'), Decimal('800')), init=False)
    price_brick_hruzh = field(default=(Decimal('650'), Decimal('675')), init=False)
    price_brick_brezh = field(default=(Decimal('675'), Decimal('700')), init=False)
    price_brick_standart = field(default=(Decimal('725'), Decimal('750')), init=False)
    price_brick_upgrade = field(default=(Decimal('750'), Decimal('775')), init=False)
    price_monolith_brick = field(default=(Decimal('750'), Decimal('800')), init=False)
    price_monolith_frame_and_block = field(default=(Decimal('725'), Decimal('775')), init=False)
    price_monolith_panel = field(default=(Decimal('700'), Decimal('750')), init=False)
    lifespan_panel = field(default=Decimal('100'), init=False)
    lifespan_brick = field(default=Decimal('125'), init=False)
    lifespan_monolith = field(default=Decimal('150'), init=False)
    kad_price_average_minsk = field(default=Decimal('184'), init=False)
    price_finishing_m2 = field(default=(Decimal('115'), Decimal('130')), init=False)
    price_big_repair_m2 = field(default=(Decimal('90'), Decimal('105')), init=False)
    price_cosmetic_m2 = field(default=(Decimal('135'), Decimal('150')), init=False)
    price_good_m2 = field(default=Decimal('175, 190'), init=False)
    price_perfect_m2 = field(default=(Decimal('195'), Decimal('210')), init=False)
    price_design_m2 = field(default=(Decimal('265'), Decimal('285')), init=False)
    base_value = field(default=Decimal('22'), init=False)
    currency_api = field(default='https://api.nbrb.by/exrates/rates?periodicity=0', init=False)
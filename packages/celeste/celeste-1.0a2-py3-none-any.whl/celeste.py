"""
Create blueprint to define data structure, use blueprint to validate data.

    >>> from celeste import Celeste
    >>> celeste = Celeste({'name': {type: str}})
    >>> celeste.validate({'name': 'Tom'})
"""  # 1.0alpha2


class Celeste:

    def __init__(self, blueprint: dict, /):
        self.blueprint = blueprint

    def validate(self, data: dict, /) -> ...:
        raise NotImplementedError


class _xe6_xad_x8c_xe7_x90_xaa_xe6_x80_xa1_xe7_x8e_xb2_xe8_x90_x8d_xe4_xba_x91:
    pass

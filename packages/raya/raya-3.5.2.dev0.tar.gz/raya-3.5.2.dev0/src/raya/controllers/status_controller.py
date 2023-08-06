from rclpy.node import Node
from raya.enumerations import ANG_UNIT, POS_UNIT
from raya.controllers.base_controller import BaseController


class StatusController(BaseController):

    def __init__(self, name: str, node: Node, interface, extra_info):
        pass

    async def get_raya_status(self) -> dict:
        return

    async def get_available_arms(self) -> dict:
        return

    async def get_battery_status(self) -> dict:
        return

    async def get_localization_status(self, ang_unit: ANG_UNIT,
                                      pos_unit: POS_UNIT) -> dict:
        return

    async def get_manipulation_status(self) -> dict:
        return

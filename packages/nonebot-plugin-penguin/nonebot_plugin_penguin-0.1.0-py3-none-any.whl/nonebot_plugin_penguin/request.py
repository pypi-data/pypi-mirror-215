import json
from typing import Any

from httpx import AsyncClient

from .config import plugin_config
from .utils import PenguinDataParser
from .types import (
    Item,
    Zone,
    Stage,
    Matrix,
    Request,
    T_Query,
    T_Server,
    T_Respond,
    lang_map,
)


class Penguin:
    raw: tuple[T_Query, dict[str, Any]]

    async def fetch(self, request: Request) -> int:
        """请求penguin-stats的widget数据, 存储到raw中

        参数:
            server: 服务器类型，可选(cn, kr, us, jp)
            type: 掉落物查询类型，可选(item, stage, exact)
            ids: 掉落物id列表, 当type为(item | stage)时,
                ids需传入一个对应id的长度为1的tuple;
                当type为exact时, ids需传入(stageId, ItemId)顺序的tuple
            参考：https://widget.penguin-stats.io/

        返回值:
            html状态码
        """
        async with AsyncClient() as client:
            widget_url = f"{plugin_config.penguin_widget}/result/{request.server.upper()}/{request.type}"  # noqa: E501
            match request.type:
                case "item" | "stage":
                    widget_url += f"/{request.ids[0]}"
                case "exact":
                    assert (
                        len(request.ids) == 2
                    ), "当type为exact时, ids需要(StageId, ItemId)的长度为2的tuple)"
                    widget_url += f"/{request.ids[0]}/{request.ids[1]}"

            res = await client.get(widget_url)
            html_obj = PenguinDataParser()
            html_obj.feed(res.text)
            assert html_obj.data
            data: dict = json.loads(html_obj.data)

            if data.get("error"):
                raise ValueError(data["error"])

            self.raw = (request.type, data)

        return res.status_code

    def all(self) -> tuple[T_Query, dict[str, Any]]:
        """返回一个元组，包含请求的类型和请求的结果"""

        return self.raw

    def by_item_id(self, item_id: str) -> Item:
        """返回和item_id匹配的第一个元素"""
        items = self.all()[1].get("items")
        assert isinstance(items, list), "items的值应该是列表而非其他！"
        item_dict = next((item for item in items if item.get("itemId") == item_id), {})
        if item_dict.get("spriteCoord") is None:
            # 家具没有spriteCoord，这里手动指定一个
            item_dict["spriteCoord"] = [2, 16]
        return Item.parse_obj(item_dict)

    def by_stage_id(self, stage_id: str) -> Stage:
        """返回和stage_id匹配的第一个元素"""
        matrix = self.all()[1].get("stages")
        assert isinstance(matrix, list), "stages的值应该是列表而非其他！"
        stage_dict = next(
            (item for item in matrix if item.get("stageId") == stage_id), {}
        )
        return Stage.parse_obj(stage_dict)

    def by_zone_id(self, zone_id: str) -> Zone:
        """返回和zone_id匹配的第一个元素"""
        zones = self.all()[1].get("zones")
        assert isinstance(zones, list), "zones的值应该是列表而非其他！"
        zone = next((item for item in zones if item.get("zoneId") == zone_id), {})
        return Zone.parse_obj(zone)

    def matrix(self) -> list[Matrix]:
        raw = self.all()
        _cache = raw[1].get("matrix")
        assert isinstance(_cache, list), "matrix的值应该是列表而非其他！"

        def gen_dict(raw_item: dict[str, str | int]) -> Matrix:
            assert isinstance(
                (stage_id := raw_item.get("stageId")), str
            ), "stageId的值应该是字符串而非其他！"
            stage = self.by_stage_id(stage_id)

            assert isinstance(
                (item_id := raw_item.get("itemId")), str
            ), "itemId的值应该是字符串而非其他！"
            item = self.by_item_id(item_id)

            zone = self.by_zone_id(stage.zoneId)

            assert isinstance(
                (quantity := raw_item.get("quantity")), int
            ), "quantity的值应该是整数而非其他！"
            assert isinstance(
                (times := raw_item.get("times")), int
            ), "times的值应该是整数而非其他！"

            percentage = round(quantity / times * 100, 2)
            apPPR = round(stage.apCost / percentage, 2)
            start: int = raw_item.get("start", 0)  # type: ignore
            end: int | None = raw_item.get("end", None)  # type: ignore

            return Matrix(
                stage=stage,
                zone=zone,
                item=item,
                percentage=percentage,
                apPPR=apPPR,
                quantity=quantity,
                times=times,
                start=start,
                end=end,
            )

        _cache = map(gen_dict, _cache)
        return list(_cache)

    def translate(self, server: T_Server, type: T_Respond, id: str) -> str:
        match type:
            case "item":
                item = self.by_item_id(id)
                return item.name_i18n.get(lang_map[server], id)
            case "stage":
                stage = self.by_stage_id(id)
                return stage.code_i18n.get(lang_map[server], id)
            case "zone":
                zone = self.by_zone_id(id)
                return zone.zoneName_i18n.get(lang_map[server], id)
            case _:
                return "暂不支持"

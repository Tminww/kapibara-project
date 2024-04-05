from parser.external_api.request import request
from utils import utils
import json


logger = utils.get_logger("api_service")


class ApiService:

    @staticmethod
    def get_all_types() -> list:

        response = request.api.types_in_block()
        all_types: list = []

        for type in response["response"].json():
            all_types.append(
                dict(
                    name=type["name"],
                    external_id=type["id"],
                    # FIXME: ЭТО КОСТЫЛЬ
                    # id_dl=1,
                )
            )

        print(json.dumps(all_types[0], ensure_ascii=False, indent=4))
        logger.debug(json.dumps(all_types[0], indent=4, ensure_ascii=False))
        return all_types

    @staticmethod
    def get_block_types(block: str) -> list:

        response = request.api.types_in_block(block=block)
        block_types: list = []

        for type in response["response"].json():
            block_types.append(
                dict(
                    name=type["name"],
                    external_id=type["id"],
                    # FIXME: ЭТО КОСТЫЛЬ
                    # id_dl=1,
                )
            )

        print(json.dumps(block_types[0], ensure_ascii=False, indent=4))
        logger.debug(json.dumps(block_types[0], indent=4, ensure_ascii=False))
        return block_types

    @staticmethod
    def get_subblocks_public_blocks(parent) -> list:
        response = request.api.public_blocks(parent=parent)
        subblocks: list = []

        for subblock in response["response"].json():
            subblocks.append(
                dict(
                    name=subblock["name"],
                    short_name=subblock["shortName"],
                    external_id=subblock["id"],
                    code=subblock["code"],
                    has_children=subblock["hasChildren"],
                    parent_id=subblock["parentId"],
                    categories=subblock["categories"],
                )
            )

        print(json.dumps(subblocks[0], ensure_ascii=False, indent=4))
        logger.debug(json.dumps(subblocks[0], indent=4, ensure_ascii=False))
        return subblocks

    @staticmethod
    def get_public_blocks() -> list:
        response = request.api.public_blocks()
        blocks: list = []

        for block in response["response"].json():
            blocks.append(
                dict(
                    name=block["name"],
                    short_name=block["shortName"],
                    external_id=block["id"],
                    code=block["code"],
                    has_children=block["hasChildren"],
                    parent_id=block["parentId"],
                    categories=block["categories"],
                )
            )

        print(json.dumps(blocks[0], ensure_ascii=False, indent=4))
        logger.debug(json.dumps(blocks[0], indent=4, ensure_ascii=False))
        return blocks

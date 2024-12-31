from model.responses.vault_response import VaultResponse


def parse_db_response(response: VaultResponse) -> dict:
    _id, *rest = response.items()
    id_dict = {"id": str(_id[1])}
    data_dict = {key: value for key, value in rest}
    result_dict = {**id_dict, **data_dict}
    return result_dict

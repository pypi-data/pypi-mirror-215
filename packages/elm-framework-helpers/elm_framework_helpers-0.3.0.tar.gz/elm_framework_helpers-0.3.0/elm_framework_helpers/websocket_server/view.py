def websocket_view(
    ids: str | list[str],
    values: str | list[str],
    hx_swap_oob: str | list[str] | None = None,
):
    """Simple view function which combines a list of ids and values into HTML understood by htmx websockets. This allows to update multiple divs at once.

    Args:
        ids (str | list[str]): List of ids to use for the divs.
        values (str | list[str]): List of values that go into the divs.
        hx_swap_oob (str | list[str] | None, optional): Out of bands swap value refer to https://htmx.org/attributes/hx-swap-oob/. Defaults to None, which will be converted to "innerHTML" for all divs. If provided, must have same length as ids and values

    Returns:
        _type_: _description_
    """
    if isinstance(ids, str):
        ids = [ids]
    if isinstance(values, str):
        values = [values]
    if not hx_swap_oob:
        hx_swap_oob = ["innerHTML"] * len(ids)
    return "".join(
        [
            f'<div id="{id}" hx-swap-oob="{oob}">{value}</div>'
            for id, value, oob in zip(ids, values, hx_swap_oob)
        ]
    )

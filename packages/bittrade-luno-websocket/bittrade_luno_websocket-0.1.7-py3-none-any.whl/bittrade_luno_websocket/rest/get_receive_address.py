from typing import Any, Callable
import reactivex
from bittrade_luno_websocket.models.rest.receive_address import *
from bittrade_luno_websocket.connection.http import prepare_request, send_request
from bittrade_luno_websocket.models import RequestMessage
from bittrade_luno_websocket.models import endpoints


def get_receive_address_http_factory(
    add_token: Callable,
) -> Callable[[str], reactivex.Observable[Any]]:
    def get_receive_address_http(asset: str) -> reactivex.Observable[Any]:
        return send_request(
            add_token(
                prepare_request(
                    RequestMessage(
                        method="GET",
                        endpoint=endpoints.Endpoints.GET_RECEIVE_ADDRESS,
                        params={"asset": asset},
                    )
                )
            )
        )

    return get_receive_address_http

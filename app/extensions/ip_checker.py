# No validation for inputs, no logging

from flask import request, abort
import geoip2.database, geoip2.errors
from typing import Union, List, Tuple


def check_ip_whitelist(geoip_db: str, whitelist: Union[str, List[str], Tuple[str]]) -> None:
    if isinstance(whitelist, str):
        if whitelist == 'all':
            return

    client_ip = get_client_ip()

    try:
        with geoip2.database.Reader(geoip_db) as geoip_reader:
            response = geoip_reader.country(client_ip)
            country_code = response.country.iso_code

            if country_code not in whitelist:
                abort(403, "IP from your country is not allowed.")
    except geoip2.errors.AddressNotFoundError:
        abort(403, "Could not determine your IP location.")


def get_client_ip() -> str:
    # Check for the 'X-Forwarded-For' header (used in case of proxies or load balancers)
    if 'X-Forwarded-For' in request.headers:
        # It's a comma-separated list of IPs; the first one is the original client IP
        client_ip = request.headers['X-Forwarded-For'].split(',')[0].strip()
    else:
        # Fallback to remote_addr if no proxy is involved
        client_ip = request.remote_addr

    if not client_ip:
        abort(400, "Could not retrieve the client IP.")

    return client_ip

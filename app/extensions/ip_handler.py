from flask import request, abort
import geoip2.database, geoip2.errors
from typing import Any, Union, List, Tuple


class IPHandler:
    _instance = None

    def __new__(cls, geoip_db: Any = None, allowed_countries: Union[str, List[str], Tuple[str]] = 'all'):
        if cls._instance is None:
            cls._instance = super(IPHandler, cls).__new__(cls)
            cls._instance.geoip_db = geoip_db
            cls._instance.allowed_countries = allowed_countries
            cls._instance.ip_address = ''
            cls._instance.country_code = ''
            cls._instance.local = True
            cls._instance.error = False
        return cls._instance

    def update_client_info(self):
        self.get_client_ip()
        self.get_client_country()

    def get_client_ip(self):
        # Check for the 'X-Forwarded-For' header (used in case of proxies or load balancers)
        if 'X-Forwarded-For' in request.headers:
            # It's a comma-separated list of IPs; the first one is the original client IP
            client_ip = request.headers['X-Forwarded-For'].split(',')[0].strip()
        else:
            # Fallback to remote_addr if no proxy is involved
            client_ip = request.remote_addr

        if not client_ip:
            self._instance.error = True

        if client_ip != '127.0.0.1':
            self._instance.local = False

        self._instance.ip_address = client_ip

    def get_client_country(self):
        try:
            with geoip2.database.Reader(self.geoip_db) as geoip_reader:
                response = geoip_reader.country(self.ip_address)
                self._instance.country_code = response.country.iso_code

        except geoip2.errors.AddressNotFoundError:
            self._instance.error = True

    def check_allowed_countries(self) -> bool:
        if isinstance(self.allowed_countries, str):
            if self.allowed_countries == 'all':
                return True

        if self.country_code not in self.allowed_countries:
            return False

        return True

    def check_ip(self):
        self.update_client_info()
        if not self.local:
            if not self.check_allowed_countries():
                abort(403, "IP from your country is not allowed.")

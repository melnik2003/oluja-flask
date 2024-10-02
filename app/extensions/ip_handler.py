from flask import Flask, request, abort
import geoip2.database
import geoip2.errors
import threading
import atexit
from typing import Any, Union, List
from functools import wraps


def ensure_initialized(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self._initialized:
            raise RuntimeError("IPHandler is not initialized. Call `init` or `init_app` beforehand.")
        return method(self, *args, **kwargs)
    return wrapper


class IPHandler:
    _instance = None
    _initialized = False
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(IPHandler, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.geoip_db = ''
        self.allowed_countries = 'all'
        self.ip_address = ''
        self.country_code = ''
        self.local = True
        self.error = False
        self.geoip_reader = None

    def init_app(self, app: Flask):
        geoip_db = app.config.get('GEOIP_DB')
        allowed_countries = app.config.get('ALLOWED_COUNTRIES')
        self.init(geoip_db, allowed_countries)

    def init(self, geoip_db: str = None, allowed_countries: Union[str, List[str]] = 'all'):
        with self._lock:
            if not self._initialized:
                self.geoip_db = geoip_db
                self.allowed_countries = [allowed_countries] if isinstance(allowed_countries, str) else list(allowed_countries)
                self.geoip_reader = geoip2.database.Reader(self.geoip_db)
                atexit.register(self.cleanup)
                IPHandler._initialized = True

    @ensure_initialized
    def update_client_info(self):
        with self._lock:
            self.get_client_ip()
            self.get_client_country()

    @ensure_initialized
    def get_client_ip(self):
        client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        if client_ip:
            client_ip = client_ip.split(',')[0].strip()

        self.local = client_ip in ('127.0.0.1', '::1')
        self.ip_address = client_ip if client_ip else ''

        if not self.ip_address:
            self.error = True

    @ensure_initialized
    def get_client_country(self):
        try:
            response = self.geoip_reader.country(self.ip_address)
            self.country_code = response.country.iso_code
        except geoip2.errors.AddressNotFoundError:
            self.error = True

    @ensure_initialized
    def is_country_allowed(self) -> bool:
        return 'all' in self.allowed_countries or self.country_code in self.allowed_countries

    @ensure_initialized
    def check_ip(self):
        self.update_client_info()
        if not self.local and not self.is_country_allowed():
            abort(403, "IP from your country is not allowed.")

    @ensure_initialized
    def cleanup(self):
        if self.geoip_reader:
            self.geoip_reader.close()
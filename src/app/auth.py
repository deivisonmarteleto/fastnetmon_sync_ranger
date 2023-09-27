"""
Module responsible for logging into ipam.
"""
from typing import Dict

import requests
from dynaconf import settings
from requests.auth import HTTPBasicAuth

from .database import RedisDB


class IpamAuth:
    """
    class Ipam Auth
    """

    @staticmethod
    def login() -> Dict:
        """
        login ipam func
        :params: None
        :return:  Token (6h)
        """

        try:
            print("Inicando busca de token...")
            cache = RedisDB(2)

            url = f"{settings.IPAM_URL}/api/app/user"

            request_ipam = requests.post(url, auth=HTTPBasicAuth(settings.IPAM_USER,settings.IPAM_PASS), timeout=5)
            if request_ipam.status_code == 200:
                get_token = request_ipam.json().get("data")
                print("Token gerado com sucesso: %s" % get_token)

                token = get_token["token"]
                cache.save("STI", token, 21600)
                return  {"status": "success","code":request_ipam.status_code, "data":token}

            raise Exception("Erro para logar no Ipam...") from request_ipam.text

        except Exception as err:
            print(err)
            raise Exception("error interno: Login Ipam") from err

class IpamSession:
    """
    class Ipam session
    """

    @staticmethod
    def session() -> Dict:
        """
        session ipm
        """

        try:
            print("Abrindo sessão com ipam...")
            cache = RedisDB(2)

            token_cache = cache.search("STI")
            if token_cache is None:
                print("Token não encontrado, gerando novo token...")
                session_ipam = IpamAuth.login()
                token = session_ipam["data"]
            else:
                token = token_cache

            print("Login realizado com sucesso...")
            return token

        except Exception as err:
            print(err)
            raise Exception("error interno: Session Ipam") from err

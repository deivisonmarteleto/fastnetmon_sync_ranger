"""
Service object by Collections.
"""
import json
from typing import Dict

import requests
from dynaconf import settings


class IpamService:
    """
    class Ipam Service
    """

    @staticmethod
    def get_filter_object(controller: str, params: dict, token: str) -> Dict:
        """
        Func get  ipam
        :params str: ex.: Id Device
        :return Dict: Dict
        """

        headers = {
            "Content-Type": "application/json",
            "token": token
        }

        try:
            print("Iniciango service get com filtro controler: %s" % controller)
            url = f"{settings.IPAM_URL}/api/app/{controller}"
            parse_json = json.dumps(params)

            response = requests.get(url, headers=headers,  data=parse_json ,timeout=5)
            if response.status_code == 200:

                return {
                    "data":response.json().get("data"),
                    "status":"success",
                    "status_code":response.status_code
                }

            raise Exception("Error para realizar get com filto no Ipam...") from response.text

        except Exception as err:
            print(err)
            raise Exception("error interno: .get_filter_object") from err

    @staticmethod
    def get(controller: str, token: str) -> Dict:
        """
        Metodo realiza um GET na API do IPAM, para buscar todos os itens de uma determinada controller.
        :params controller: ex.: vrf, sections, subnets
        :return Dict: Dict
        """

        headers = {
            "Content-Type": "application/json",
            "token": token
        }

        try:
            print("Iniciango service get controler: %s" % controller)
            url = f"{settings.IPAM_URL}/api/app/{controller}"
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                return {
                    "data":response.json().get("data"),
                    "status":"success",
                    "status_code":response.status_code
                }

            raise Exception("Error para realizar get no Ipam...") from response.text

        except Exception as err:
            print(err)
            raise Exception("error interno: Service get Ipam") from err

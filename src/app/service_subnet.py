import ipaddress

class ServiceSubnet:
    """
    Class responsavel por subneting service"""

    @staticmethod
    def granerSubneting(subneting: list):
        """"
        Metodo responsavel por quebrar o bloco /24 em 4 blocos /26
        :params list: ex:. [10.0.0.1,10.2.0.0]
        :return dict:
        """

        try:
            print("Iniciando quebra de bloco 24 para bloco 26...")
            mask_26_subneting = []

            for subnet in subneting:
                broker_subnet = ipaddress.ip_network(f'{subnet}/24').subnets(prefixlen_diff=2)
                for net in broker_subnet:
                    mask_26_subneting.append(str(net))

            print("Bloco /26 preparado com sucesso.")
            return mask_26_subneting

        except Exception as err:
            print(err)
            raise Exception("error interno: .granerSubneting") from err


    @staticmethod
    def save_file(subneting: list, file=str):
        """
        Metodo responsavel por salvar os blocos /26 no arquivo network_lis e network_whitelist
        :params subneting list: [10.0.0.0/26,10.0.0.128/26]
        :params file str: path file /tmp/network_list
        """

        net_list = []
        try:
            print("Preparando para salvar lista de bloco: %s" % file)

            for net in subneting:
                net_list.append(net + '\n')

            with open(file, 'w+') as f:
                f.writelines(net_list)
                f.truncate()

            print("Lista de bloco 26 salva com sucesso.")

        except Exception as err:
            print(err)
            raise Exception("error interno: .save_file") from err

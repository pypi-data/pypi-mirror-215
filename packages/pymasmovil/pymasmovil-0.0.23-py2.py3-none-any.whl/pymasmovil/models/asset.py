from datetime import datetime, date

from pymasmovil.client import Client
from pymasmovil.models.contract import Contract
from pymasmovil.errors.exceptions import WrongFormattedDate, UnknownMMError


class Asset(Contract):
    _route = "/v2/assets"

    maxNumTariff = ""
    numTariff = ""
    assetType = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def get(cls, session, asset_id):
        contract = super().get(session, asset_id)

        return cls(**contract["asset"])

    @classmethod
    def get_by_phone(cls, session, phone):
        """
        Retrieve the asset associated to a given phone number from the MM sytem.

        :param:
            phone (str): Phone number of the contract we expect
        :return: dict containing the asset from the MM response
        """
        params = {"rowsPerPage": 1, "actualPage": 1, "phone": phone}

        response = Client(session).get(cls._route, **params)

        return cls(**response["rows"][0])

    @classmethod
    def update_product(
        cls,
        session,
        asset_id,
        transaction_id,
        product_id="",
        execute_date="",
        additional_bonds=[],
        bonds_to_remove=[],
        promotions=[],
        promotions_to_remove=[],
        shared_bond_product_id="",
        shared_bond_id="",
    ):
        """
        Modify asset request:
            - change tariff
            - add one-shot bonds

        :param:
            asset_id (str): MM Asset ID
            transaction_id (str): Unique and correlative 18-length numeric code
            productId (str): ID from the new tariff we want to apply
                            [only for change tariff]
            execute_date (str): request date [only for change tariff]
            additional_bonds (list): additional bonds to add
            bonds_to_remove (list): additional bonds to delete
            promotions (list): promotions to add
            bonds_to_remove (list): promotions to delete
            shared_bond_product_id (str): MM product ID from the shared bond
                                        [only for change tariff]
            shared_bond_id (str): MM ID for an existing instance of a shared bond
                                to which we want to add another mobile line sharing
                                its data [only for change tariff]

        :return: modified asset
        """

        route = "{}/{}/change-asset".format(cls._route.replace("v2", "v1"), asset_id)

        active_change = {
            "transactionId": transaction_id,
            "assetInfo": {
                "executeDate": execute_date,
                "productId": product_id,
                "additionalBonds": additional_bonds,
                "removeBonds": [{"assetId": bond_id} for bond_id in bonds_to_remove],
                "promotions": promotions,
                "removePromotions": [
                    {"assetId": bond_id} for bond_id in promotions_to_remove
                ],
            },
        }
        if shared_bond_product_id:
            if shared_bond_id:
                # Existing shared bond to add a line to
                shared_bond_data = {
                    "productRelation": shared_bond_id,
                    "percentConsumption": "100",
                }
            else:
                # New shared bond to create
                shared_bond_data = {
                    "productId": shared_bond_product_id,
                    "percentConsumption": "100",
                }
            active_change["sharedBond"] = shared_bond_data

        response = Client(session).patch(route, (), active_change)

        if response == "Petición aceptada":
            return response
        else:
            raise UnknownMMError(response)

    @classmethod
    def get_consumption(cls, session, asset_id, init_date="", end_date=""):
        """
        Retrieve the asset consumption from current month

        :param:
            asset_id (str): MM Asset ID
            init_date (str): [YYYY-MM-DD] Date from which we want to consult the consumption.
                            Default value: first day of current month
            end_date (str): [YYYY-MM-DD] Date up to which we want to consult the consumption
                            Default value: today

        :return: dict containing the consumption (voice and data) from the MM response
        """

        route = "{}/{}/consumption".format(cls._route.replace("v2", "v1"), asset_id)
        expected_format = "%Y-%m-%d"  # (ex: 2022-06-05)
        today = date.today()

        if init_date and cls._check_date(init_date, expected_format):
            init_date = init_date
        else:
            init_date = datetime(today.year, today.month, 1).strftime(expected_format)

        if end_date and cls._check_date(end_date, expected_format):
            end_date = end_date
        else:
            end_date = today.strftime(expected_format)

        params = {"iniDate": init_date, "endDate": end_date}

        response = Client(session).get(route, **params)

        consumption_dct = response[0]["listBonos"][0]["listConsumos"][0]
        key_list = ["vozNacionalTotal", "vozNacional", "volumenTotal", "volumen"]

        return dict(
            (key, consumption_dct[key]) for key in key_list if key in consumption_dct
        )

    def _check_date(str_date, expected_format):
        """
        Checks if string date matches the expected format
        If it does not, a custom WrongFormattedDate exception is raised

        :param:
            str_date (str): input string formatted date
            expected_format (str): expected date format code
        """
        try:
            datetime.strptime(str_date, expected_format)
        except ValueError:
            raise WrongFormattedDate(str_date, expected_format)
        return True

import requests as r
import pandas as pd
import sys
import time
from b4s_abstract.b4s_abstractor import B4SApartmentExtractor
from b4s_abstract.b4s_abstractor_soup import B4SApartmentExtractorSoup
from loggin_abstract.log_status import logger
class GetApartmentsInfo:

    def __init__(self):
        self.page_number=1
        self.price=[]
        self.address=[]
        self.condominium=[]
        self.floor_size=[]
        self.iptu=[]
        self.number_of_rooms=[]
        self.number_of_bathrooms=[]
        self.parking_spots=[]
        self.description=[]
        

    def _get_apartment_page(self):
        logger(f"Making request number {self.page_number}",status="INFO")
        self.url = f'https://www.zapimoveis.com.br/aluguel/apartamentos/sp+sao-paulo/?onde=,S%C3%A3o%20Paulo,S%C3%A3o%20Paulo,,,,,city,BR%3ESao%20Paulo%3ENULL%3ESao%20Paulo,-23.555771,-46.639557,%2Faluguel%2Fimoveis%2Fsp%2Bsao-paulo%2F&transacao=Aluguel&tipo=Im%C3%B3vel%20usado&tipos=apartamento_residencial,studio_residencial,kitnet_residencial,casa_residencial,,condominio_residencial,casa-vila_residencial,cobertura_residencial,flat_residencial,loft_residencial,lote-terreno_residencial,granja_residencial&pagina={self.page_number}'
        self.headers = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}
        self.apartments_page=r.get(self.url,headers=self.headers)
        

    def _generate_html_page(self):
        logger(f"Getting the HTML page",status="INFO")
        self.apartment_html=self.apartments_page.text
        self.b4s_object=B4SApartmentExtractorSoup(self.apartment_html)
        self.soup = self.b4s_object.get_apartment_html_soup()

    def _extract_apartment_info_columns(self):
        """
        Extracts and returns the websites apartments and its infos in columns for each of them.
        """
        logger(f"Initializing extraction of apartment renting pages",status="INFO")
        for page in range(1,100):
            self.page_number=page
            self._get_apartment_page()
            self._generate_html_page()
            total_rent_infos=self.b4s_object.get_general_apartment_info()
            for rent_info in total_rent_infos:
                b4s_apartment_infos=B4SApartmentExtractor(rent_info)

                self.price.append(b4s_apartment_infos.find_apartment_rent_price())
                self.address.append(b4s_apartment_infos.find_apartment_address())
                self.condominium.append(b4s_apartment_infos.find_apartment_codominium())
                self.floor_size.append(b4s_apartment_infos.find_apartment_floor_size())
                self.iptu.append(b4s_apartment_infos.find_apartment_iptu())
                self.number_of_rooms.append(b4s_apartment_infos.find_apartment_number_of_rooms())
                self.number_of_bathrooms.append(b4s_apartment_infos.find_apartment_number_of_bathrooms())
                self.parking_spots.append(b4s_apartment_infos.find_apartment_parking_spots())
                # self.description.append(b4s_apartment_infos.find_apartment_description())
                # break
                time.sleep(5)

    def generate_pandas_apartment_info(self) -> pd.DataFrame:
        """
        Generate, from the _extract_apartment_info_columns function, a pandas Dataframe with each list as a column.
        """
        logger(f"Initializing transformation to Pandas",status="INFO")

        self._extract_apartment_info_columns()
        apartment_infos_dict={
            "price":self.price,
            "address":self.address,
            "condominium":self.condominium,
            "floor_size":self.floor_size,
            "iptu":self.iptu,
            "number_of_rooms":self.number_of_rooms,
            "number_of_bathrooms":self.number_of_bathrooms,
            "parking_spots":self.parking_spots,
            # "description":self.description
        }
        apartment_infos_df=pd.DataFrame(apartment_infos_dict)
        return apartment_infos_df
    
# def apartment_extractor():
#     ap=GetApartmentsInfo()
#     print(ap.generate_pandas_apartment_info())


# if __name__=="__main__":
#     apartment_extractor()        







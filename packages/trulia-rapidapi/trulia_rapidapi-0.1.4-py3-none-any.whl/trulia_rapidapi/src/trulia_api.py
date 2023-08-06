"""
LetsScrape, email: hello@letsscrape.com
"""
import asyncio
import time
from typing import List, Optional, Union, Dict, AnyStr
from urllib.parse import urlencode
from purl import URL
import aiohttp

from src.trulia_models.enums import *
from src.trulia_models.listing_model import ListingModel
from src.trulia_models.search_token_model import SearchTokenModel
from src.trulia_models.details_model import DetailsModel



class TruliaAPI(object):
    def __init__(self, rapid_api_key: AnyStr):
        """
        To obtain your rapid_api key, you first need to sign up on RapidAPI. You can do so by visiting this link: https://rapidapi.com/auth/sign-up.
        After registering, navigate to the Trulia Real Estate Scraper API page at https://rapidapi.com/letsscrape/api/trulia-real-estate-scraper.
        Click on "Subscribe to Test" to get access to the API.
        After subscribing, you will find your X-RapidAPI-Key. It's located on the right side of the screen, within the "Code Snippets" section.
        Remember, this key is vital for accessing the API, so keep it safe.        
        """
        self.rapidapi_host = 'trulia-real-estate-scraper.p.rapidapi.com'
        self.headers = {
            "X-RapidAPI-Key": rapid_api_key,
            "X-RapidAPI-Host": self.rapidapi_host,
        }

    async def __get_request(self, path: AnyStr, params: Optional[Dict] = None) -> Dict:
        """
        :param path: Request path
        :param params: Request query parameters
        :return: JSON Response Dictionary
        """
        if params:
            query_string = urlencode(params)
        else:
            query_string = ""

        url = URL(
            host=self.rapidapi_host,
            path=path,
            query=query_string,
            scheme="https"
        ).as_string()

        session_timeout = aiohttp.ClientTimeout(total=45.0)
        is_ok = False

        while True:
            async with aiohttp.ClientSession(headers=self.headers, timeout=session_timeout) as session:
                async with session.get(url=url) as response:
                    try:
                        json_response = await response.json()  
                        if response.status == 200 or response.status == 400:  
                            is_ok = True
                    except aiohttp.client.ContentTypeError:
                        continue
                    if is_ok:
                        break
            await asyncio.sleep(0.3)

        return json_response
    


    async def get_search_token(self, search_type: TruliaSearchType, place: str) -> SearchTokenModel:
        """
        This function generates a token (or tokens in some cases) based on the variable {place}.
        For example, if we pass a part of {place} instead of 'Scottsdale', say 'Scot', we'll receive 
        several tokens along with the matched {places}, from which we can select the token to use
        in the search_by_token function.
        """
        path = f"/search/token?search_type={search_type.name}&place={place}"
        response_data = await self.__get_request(path=path)
        response = SearchTokenModel.parse_obj(response_data)
        return response

    async def get_listing_by_url(self, url: str, page: int) -> ListingModel:
        """
        This function retrieves properties from the listing. Simply visit https://www.trulia.com/, choose the listing that interests you, such as https://www.trulia.com/AZ/Scottsdale/, and then input that URL into the query.
        """
        path = f"/homes/listing_by_url?url={url}&page={page}"
        response_data = await self.__get_request(path=path)
        response = ListingModel.parse_obj(response_data)
        return response
    
    async def details_by_url(self, url:str) -> DetailsModel:
        """
        This function retrieves property details from trulia.com by using a specific URL.
        For example, you can input the URL https://www.trulia.com/p/az/paradise-valley/9316-n-58th-st-paradise-valley-az-85253--2113546226 to obtain details about that particular property.    
        """
        path = f"/homes/details_by_url?url={url}"
        response_data = await self.__get_request(path=path)
        response = DetailsModel.parse_obj(response_data)
        return response
   
    async def search_for_sale_by_place(self, place: str, page: int, 
        sort: TruliaSort=None, beds: TruliaBeds=None,
        min_price: TruliaPriceRange=None, max_price: TruliaPriceRange=None,
        house_type: TruliaHouseType=None, for_sale_by_agent: bool=None, for_sale_by_owner: bool=None,
        new_construction: bool=None) -> ListingModel:
        """
        This function automatically generates a search token based on the variable {place}. 
        If {place} returns multiple search tokens, the first element will be passed to 
        the search query. Therefore, in this function, full control is not assured since we 
        might want to use, for example, the second token that matches a different place. 
        At the same time, this function will often be sufficient for the user.

        Parameters:
        page (int): The page number you want to work with. If you want the first page, pass in 1.
        """
        token = await self.get_search_token(TruliaSearchType.ForSale, place)

        if len(token.data.places) == 0:
            return ListingModel(data=None, status=200, description="No places have been found!")

        search_token = token.get_first_token()

        return await self.search_for_sale_by_token(search_token, page, sort, beds, min_price, max_price,
            house_type, for_sale_by_agent, for_sale_by_owner, new_construction)

    async def search_for_sale_by_token(self, token: str, page: int, 
        sort: TruliaSort=None, beds: TruliaBeds=None,
        min_price: TruliaPriceRange=None, max_price: TruliaPriceRange=None,
        house_type: TruliaHouseType=None, for_sale_by_agent: bool=None, 
        for_sale_by_owner: bool=None, new_construction: bool=None) -> ListingModel:
        """
        This function accepts a token, in contrast to the search_for_sale_by_place, 
        where we have to manually pass the token. Hence, it's necessary 
        to first generate it with get_search_token, choose the appropriate token,
        and then pass it to the function.

        Parameters:
        page (int): The page number you want to work with. If you want the first page, pass in 1.
        """
        path = f"/search/for_sale?search_token={token}&page={page}&sort={sort}&beds={beds}&min_price={min_price}&max_price={max_price}&house_type={house_type}&for_sale_by_agent={for_sale_by_agent}&for_sale_by_owner={for_sale_by_owner}&new_construction={new_construction}"
        path = path.replace('=None', '=')
        response_data = await self.__get_request(path=path)
        response = ListingModel.parse_obj(response_data)
        return response
     
    async def search_for_sold_by_place(self, place: str, page: int, beds: TruliaBeds=None, sold_date: TruliaSoldDate=None) -> ListingModel:
        """
        This function automatically generates a search token based on the variable {place}. 
        If {place} returns multiple search tokens, the first element will be passed to 
        the search query. Therefore, in this function, full control is not assured since we 
        might want to use, for example, the second token that matches a different place. 
        At the same time, this function will often be sufficient for the user.

        Parameters:
        page (int): The page number you want to work with. If you want the first page, pass in 1.
        """
        token = await self.get_search_token(TruliaSearchType.Sold, place)

        if len(token.data.places) == 0:
            return ListingModel(data=None, status=200, description="No places have been found!")

        search_token = token.get_first_token()

        return await self.search_for_sold_by_token(search_token, page, beds, sold_date)

    async def search_for_sold_by_token(self, token: str, page: int, beds: TruliaBeds=None, sold_date: TruliaSoldDate=None) -> ListingModel:
        """
        This function accepts a token, in contrast to the search_for_sold_by_place, 
        where we have to manually pass the token. Hence, it's necessary 
        to first generate it with get_search_token, choose the appropriate token,
        and then pass it to the function.

        Parameters:
        page (int): The page number you want to work with. If you want the first page, pass in 1.
        """
        path = f"/search/for_sold?search_token={token}&page={page}&beds={beds}&sold_date={sold_date}"
        path = path.replace('=None', '=')
        response_data = await self.__get_request(path=path)
        response = ListingModel.parse_obj(response_data)
        return response
    
    async def search_for_rent_by_place(self, place: str, page: int, 
        sort: TruliaSort=None, beds: TruliaBeds=None, sold_date: TruliaSoldDate=None) -> ListingModel:
        """
        This function automatically generates a search token based on the variable {place}. 
        If {place} returns multiple search tokens, the first element will be passed to 
        the search query. Therefore, in this function, full control is not assured since we 
        might want to use, for example, the second token that matches a different place. 
        At the same time, this function will often be sufficient for the user.

        Parameters:
        page (int): The page number you want to work with. If you want the first page, pass in 1.
        """
        token = await self.get_search_token(TruliaSearchType.ForRent, place)

        if len(token.data.places) == 0:
            return ListingModel(data=None, status=200, description="No places have been found!")

        search_token = token.get_first_token()

        return await self.search_for_rent_by_token(search_token, page, sort, beds, sold_date)

    async def search_for_rent_by_token(self, token: str, page: int, 
        sort: TruliaSort=None, beds: TruliaBeds=None, min_price: TruliaPriceRangeForRent=None,
        max_price: TruliaPriceRangeForRent=None, cats_allowed: bool=None, dogs_allowed: bool=None, 
        rental_type: TruliaRentalType=None) -> ListingModel:
        """
        This function accepts a token, in contrast to the search_for_rent_by_place, 
        where we have to manually pass the token. Hence, it's necessary 
        to first generate it with get_search_token, choose the appropriate token,
        and then pass it to the function.

        Parameters:
        page (int): The page number you want to work with. If you want the first page, pass in 1.
        """
        path = f"/search/for_rent?search_token={token}&page={page}&sort={sort}&beds={beds}&min_price={min_price}&max_price={max_price}&cats_allowed={cats_allowed}&dogs_allowed={dogs_allowed}&rental_type={rental_type}"
        path = path.replace('=None', '=')
        response_data = await self.__get_request(path=path)
        response = ListingModel.parse_obj(response_data)
        return response
    
 
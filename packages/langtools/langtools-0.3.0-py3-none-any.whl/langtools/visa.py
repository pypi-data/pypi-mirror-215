import json
from datetime import datetime, timedelta
from time import sleep
from typing import Optional, Type

import cloudscraper
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from retry import retry


class OriginalValues(BaseModel):
    fromCurrency: str
    fromCurrencyName: str
    toCurrency: str
    toCurrencyName: str
    asOfDate: int
    fromAmount: str
    toAmountWithVisaRate: str
    toAmountWithAdditionalFee: str
    fxRateVisa: str
    fxRateWithAdditionalFee: str
    lastUpdatedVisaRate: int
    benchmarks: list


class FxRate(BaseModel):
    originalValues: OriginalValues
    conversionAmountValue: str
    conversionBankFee: str
    conversionInputDate: str
    conversionFromCurrency: str
    conversionToCurrency: str
    fromCurrencyName: str
    toCurrencyName: str
    convertedAmount: str
    benchMarkAmount: str
    fxRateWithAdditionalFee: str
    reverseAmount: str
    disclaimerDate: str
    status: str


@retry(tries=100, delay=1)
def get_visa_fx_rate(amount: float = 1.0,
                     from_curr: str = 'TWD',
                     to_curr: str = 'USD',
                     fee: float = 0.0,
                     date: datetime = None) -> FxRate:
    url = 'http://www.visa.com.tw/cmsapi/fx/rates'

    if date is None:
        date = datetime.now()

    params = dict(
        amount=amount,
        utcConvertedDate=date.strftime('%m/%d/%Y'),
        exchangedate=date.strftime('%m/%d/%Y'),
        fromCurr=from_curr,
        toCurr=to_curr,
        fee=fee,
    )

    scraper = cloudscraper.create_scraper()

    resp = scraper.get(url=url, params=params)

    try:
        fx_rate = FxRate.parse_obj(resp.json())
    except json.decoder.JSONDecodeError:
        fx_rate = get_visa_fx_rate(amount, from_curr, to_curr, fee, date - timedelta(days=1))

    sleep(0.1)
    return fx_rate


class VISAFXRateInput(BaseModel):
    amount: float = Field(description='The amount to convert.')
    from_curr: str = Field(description='The currency to convert from.')
    to_curr: str = Field(description='The currency to convert to.')


class VISAFXRate(BaseTool):

    name = "visa_fx_rate"
    description = ('A Visa FX rate tool.'
                   'Input should be an amount, a currency to convert from, and a currency to convert to. '
                   'The output will be the converted amount and the FX rate.')

    args_schema: Optional[Type[BaseModel]] = VISAFXRateInput

    def _run(self, amount: str, from_curr: str, to_curr: str) -> str:
        # the from_curr and to_curr are reversed in the API
        r = get_visa_fx_rate(amount, from_curr=to_curr, to_curr=from_curr)
        return (f'Amount: {amount}\n'
                f'From: {from_curr}\n'
                f'To: {to_curr}\n'
                f'Converted Amount: {r.convertedAmount}\n'
                f'FX Rate: {r.fxRateWithAdditionalFee}\n')

    async def _arun(self, url: str) -> str:
        raise NotImplementedError("This tool does not support async")

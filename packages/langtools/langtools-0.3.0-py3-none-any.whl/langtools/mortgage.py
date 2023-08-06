from enum import Enum
from typing import Optional, Type, Union

from langchain.tools import BaseTool
from mortgage import Loan
from pydantic import BaseModel, Field


class TermUnitEnum(str, Enum):
    days = 'days'
    months = 'months'
    years = 'years'


class CompoundedEnum(str, Enum):
    daily = 'daily'
    monthly = 'monthly'
    annually = 'annually'


class LoanInput(BaseModel):
    principal: str = Field(description='The original sum of money borrowed.')
    interest: str = Field(description='The amount charged by lender for use of the assets.')
    term: str = Field(description='The lifespan of the loan.')
    term_unit: TermUnitEnum = Field(description='Unit for the lifespan of the loan.')
    # compounded: str = Field(description='Frequency that interest is compounded')
    # currency: str = Field(description='Set the currency symbol for use with summarize')


def summarize(loan: Loan) -> str:
    return (f'Original Balance: {loan.principal}\n'
            f'Interest Rate: {loan.interest}\n'
            f'APY: {loan.apy}\n'
            f'APR: {loan.apr}\n'
            f'Term: {loan.term}\n'
            f'Monthly Payment: {loan.monthly_payment}\n'
            f'Total principal payments: {loan.total_principal}\n'
            f'Total interest payments: {loan.total_interest}\n'
            f'Total payments: {loan.total_paid}\n'
            f'Interest to principal: {loan.interest_to_principle}\n'
            f'Years to pay: {loan.years_to_pay}\n')


def parse_interest(interest: Union[str, float]) -> float:
    if isinstance(interest, str):
        if interest.endswith('%'):
            interest = float(interest.rstrip('%')) / 100
        interest = float(interest)

    if interest > 1:
        interest = interest / 100

    return interest


class LoanCalculator(BaseTool):

    name = "loan_calculator"
    description = ('A loan calculator tool.'
                   'Input should be the principal, interest, and term. '
                   'The output will be a summary of the loan.')

    args_schema: Optional[Type[BaseModel]] = LoanInput

    def _run(self, principal: str, interest: str, term: str, term_unit: str) -> str:

        loan = Loan(float(principal), parse_interest(interest), int(term), term_unit)
        return summarize(loan)

    async def _arun(self, *args, **kwargs) -> str:
        raise NotImplementedError("This tool does not support async")

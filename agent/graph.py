from dotenv import  load_dotenv
from langchain.agents.structured_output import SchemaT
from pydantic import BaseModel

load_dotenv()

from langchain_groq import ChatGroq

llm = ChatGroq(model="openai/gpt-oss-120b")

class Schema(BaseModel):
    price: float
    eps: float
    revenue: float | None = None
    market_cap: float | None = None
    company_name: str | None = None

input_text = {
    "NVIDIA released its latest quarterly financial report yesterday. "
    "The company announced a revenue of $28.3 billion, marking significant YOY growth. "
    "The quarterly EPS came in at 2.3, beating analyst expectations. "
    "As of today, the share price is $100, with a market cap over $2 trillion. "
    "The report also highlighted strong data-center performance."
}

response = llm.with_structured_output(Schema).invoke(f"Extract all financial data from this report: {input_text}")

print(response)
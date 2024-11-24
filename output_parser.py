from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

class Correction(BaseModel):
    dpi_per : float = Field(description="보정비율")

    def to_dict(self):
        return {"dpi_per" : self.dpi_per}
correction = PydanticOutputParser(pydantic_object=Correction)
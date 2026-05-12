from pydantic import BaseModel, ConfigDict, Field


class VehicleBase(BaseModel):
    license_plate: str = Field(min_length=3, max_length=20)
    driver_name: str = Field(min_length=1, max_length=120)
    brand: str = Field(min_length=1, max_length=80)
    model: str = Field(min_length=1, max_length=80)
    color: str = Field(min_length=1, max_length=80)


class VehicleCreateRequest(VehicleBase):
    pass


class VehicleResponse(VehicleBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

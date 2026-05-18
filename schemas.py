from pydantic import BaseModel

# ======================
# USER SCHEMAS
# ======================

class SignupModel(BaseModel):
    username: str
    email: str
    password: str

class LoginModel(BaseModel):
    username: str
    password: str

# ======================
# PRODUCT SCHEMAS
# ======================

class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    quantity: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True

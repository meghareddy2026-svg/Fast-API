from datetime import datetime, timedelta

from fastapi import FastAPI, Depends, HTTPException, Header
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

import models
import schemas

from database import SessionLocal, engine

# =========================
# DATABASE
# =========================

models.Base.metadata.create_all(bind=engine)

# =========================
# APP
# =========================

app = FastAPI()

# =========================
# JWT CONFIG
# =========================

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# =========================
# DATABASE SESSION
# =========================

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

# =========================
# TOKEN CREATION
# =========================

def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

# =========================
# HOME
# =========================

@app.get("/")
def home():
    return {"message": "Product API Running"}

# =========================
# SIGNUP
# =========================

@app.post("/signup")
def signup(
    user: schemas.SignupModel,
    db: Session = Depends(get_db)
):

    existing_user = db.query(models.User).filter(
        models.User.username == user.username
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    hashed_password = pwd_context.hash(user.password)

    new_user = models.User(
        username=user.username,
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()

    return {"message": "User created successfully"}

# =========================
# LOGIN
# =========================

@app.post("/login")
def login(
    user: schemas.LoginModel,
    db: Session = Depends(get_db)
):

    db_user = db.query(models.User).filter(
        models.User.username == user.username
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=400,
            detail="Invalid username"
        )

    if not pwd_context.verify(
        user.password,
        db_user.password
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid password"
        )

    token = create_access_token(
        {"sub": user.username}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

# =========================
# VERIFY TOKEN
# =========================

def verify_token(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):

    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Token missing"
        )

    try:

        token = authorization.split(" ")[1]

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        user = db.query(models.User).filter(
            models.User.username == username
        ).first()

        if not user:
            raise HTTPException(
                status_code=401,
                detail="User not found"
            )

        return user

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

# =========================
# CREATE PRODUCT
# =========================

@app.post("/products/")
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    user=Depends(verify_token)
):

    new_product = models.Product(**product.dict())

    db.add(new_product)
    db.commit()

    return {
        "message": "Product created successfully"
    }

# =========================
# GET PRODUCTS
# =========================

@app.get("/products/")
def get_products(
    db: Session = Depends(get_db)
):

    return db.query(models.Product).all()

# =========================
# DELETE PRODUCT
# =========================

@app.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    user=Depends(verify_token)
):

    product = db.query(models.Product).filter(
        models.Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    db.delete(product)
    db.commit()

    return {
        "message": "Product deleted successfully"
    }

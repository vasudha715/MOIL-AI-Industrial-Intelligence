from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from database import get_db

import models
import schemas

from auth import (
    hash_password,
    verify_password,
    create_access_token,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


# =========================================================
# REGISTER
# =========================================================

@router.post(
    "/register",
    response_model=schemas.Token,
)
def register(

    payload: schemas.UserRegister,

    db: Session = Depends(get_db),

):

    existing = (
        db.query(models.User)
        .filter(
            models.User.email == payload.email
        )
        .first()
    )

    if existing:

        raise HTTPException(

            status_code=400,

            detail=(
                "An account with this email "
                "already exists"
            ),

        )


    user = models.User(

        name=payload.name,

        email=payload.email,

        password_hash=hash_password(
            payload.password
        ),

        role=(
            payload.role
            or "industrialist"
        ),

    )


    db.add(user)

    db.commit()

    db.refresh(user)


    token = create_access_token(

        {

            "sub": str(user.id),

            "role": user.role,

        }

    )


    return schemas.Token(

        access_token=token,

        user=user,

    )



# =========================================================
# NORMAL WEBSITE LOGIN
# =========================================================

@router.post(
    "/login",
    response_model=schemas.Token,
)
def login(

    payload: schemas.UserLogin,

    db: Session = Depends(get_db),

):

    user = (
        db.query(models.User)
        .filter(
            models.User.email == payload.email
        )
        .first()
    )


    if (

        not user

        or

        not verify_password(

            payload.password,

            user.password_hash,

        )

    ):

        raise HTTPException(

            status_code=
            status.HTTP_401_UNAUTHORIZED,

            detail=
            "Incorrect email or password",

        )


    token = create_access_token(

        {

            "sub": str(user.id),

            "role": user.role,

        }

    )


    return schemas.Token(

        access_token=token,

        user=user,

    )



# =========================================================
# SWAGGER OAUTH2 TOKEN LOGIN
# =========================================================

@router.post(
    "/token",
)
def swagger_token(

    form_data:
    OAuth2PasswordRequestForm =
    Depends(),

    db: Session = Depends(get_db),

):

    # Swagger calls the email field "username"
    email = form_data.username


    user = (
        db.query(models.User)
        .filter(
            models.User.email == email
        )
        .first()
    )


    if (

        not user

        or

        not verify_password(

            form_data.password,

            user.password_hash,

        )

    ):

        raise HTTPException(

            status_code=
            status.HTTP_401_UNAUTHORIZED,

            detail=
            "Incorrect email or password",

        )


    token = create_access_token(

        {

            "sub": str(user.id),

            "role": user.role,

        }

    )


    # OAuth2 requires these fields
    return {

        "access_token": token,

        "token_type": "bearer",

    }
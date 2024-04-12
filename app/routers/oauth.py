# Import necessary modules and functions from FastAPI and the standard library
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES  # Custom configuration setting
from app.schema import Token  # Import the Token model from our application
from app.utils.common import user_authentication, create_access_token

# Initialize OAuth2PasswordBearer for handling OAuth2 Password Flow security
oauth2 = OAuth2PasswordBearer(tokenUrl="token")

# Create an API router object for registering the endpoint(s)
router = APIRouter()

# Define an endpoint for the login that issues access tokens
# This endpoint responds to POST requests at "/token" and returns data matching the Token model
@router.post("/token", response_model=Token)
async def get_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # Attempt user authentication with provided credentials
    user = user_authentication(form_data.username, form_data.password)
    
    # If authentication fails, raise an HTTPException with status 401 Unauthorized
    if user:
        # Define the token's validity duration using the application's configuration
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        # Generate an access token for the authenticated user
        accessToken = create_access_token(
            data={"sub": user["username"]},  # Set the token subject as the username
            expires_delta=access_token_expires  # Specify token validity duration
        )
        
        # Return the access token and the token type (Bearer) to the client
        return {"access_token": accessToken, "token_type": "bearer"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Please check your username and password",
        headers={"WWW-Authenticate": "Bearer"},  # Prompt the client to authenticate using Bearer token
    )

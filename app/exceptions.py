from fastapi import status, HTTPException


TypeIsNotExistException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Type does not exist...'
)


CookieNotSetException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Session cookie is not set, please add package to create...'
)


WrongIDsFormatException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Something wrong with your cookie data...'
)
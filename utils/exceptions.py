from fastapi import HTTPException, status


class NotFoundException(HTTPException):

    def __init__(self, message='Item not found'):
        super(NotFoundException, self).__init__(status_code=status.HTTP_404_NOT_FOUND, detail=message)

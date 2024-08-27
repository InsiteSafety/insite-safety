from server.resources._dry_resource import DRYResource
from models.user import User

class Users(DRYResource):
    """Resource tied to the User model. Handles fetch requests for all User instances.

    Args:
        DRYResource (DRYResource): simplify RESTFul API building.
    """
    
    def __init__(self):
        super().__init__(User)
        
class UserById(DRYResource):
    """Resource tied to the User model. Handles fetch requests for single User instances.

    Args:
        DRYResource (DRYResource): simplify RESTFul API building.
    """
    
    def __init__(self):
        super().__init__(User)
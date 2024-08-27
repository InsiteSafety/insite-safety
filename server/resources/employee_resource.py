from server.resources._dry_resource import DRYResource
from models.employee import Employee

class Employees(DRYResource):
    """Resource tied to the Employee model. Handles fetch requests for all Employee instances.

    Args:
        DRYResource (DRYResource): simplify RESTFul API building.
    """
    
    def __init__(self):
        super().__init__(Employee)
        
class EmployeeById(DRYResource):
    """Resource tied to the Employee model. Handles fetch requests for single Employee instances.

    Args:
        DRYResource (DRYResource): simplify RESTFul API building.
    """
    
    def __init__(self):
        super().__init__(Employee)
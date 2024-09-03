from resources._dry_resource import DRYResource
from models.company import Company

class Companies(DRYResource):
    """Resource tied to the Company model. Handles fetch requests for all Company instances.

    Args:
        DRYResource (DRYResource): simplify RESTFul API building.
    """
    
    def __init__(self):
        super().__init__(Company)
        
class CompanyById(DRYResource):
    """Resource tied to the Company model. Handles fetch requests for single Company instances.

    Args:
        DRYResource (DRYResource): simplify RESTFul API building.
    """
    
    def __init__(self):
        super().__init__(Company)
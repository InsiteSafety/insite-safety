from server.resources._dry_resource import DRYResource
from models.incident import Incident

class Incidents(DRYResource):
    """Resource tied to the Incident model. Handles fetch requests for all Incident instances.

    Args:
        DRYResource (DRYResource): simplify RESTFul API building.
    """
    
    def __init__(self):
        super().__init__(Incident)
        
class IncidentById(DRYResource):
    """Resource tied to the Incident model. Handles fetch requests for single Incident instances.

    Args:
        DRYResource (DRYResource): simplify RESTFul API building.
    """
    
    def __init__(self):
        super().__init__(Incident)
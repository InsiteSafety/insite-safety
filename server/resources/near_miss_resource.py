from resources._dry_resource import DRYResource
from models.near_miss import NearMiss

class NearMisses(DRYResource):
    """Resource tied to the NearMiss model. Handles fetch requests for all NearMiss instances.

    Args:
        DRYResource (DRYResource): simplify RESTFul API building.
    """
    
    def __init__(self):
        super().__init__(NearMiss)
        
class NearMissById(DRYResource):
    """Resource tied to the NearMiss model. Handles fetch requests for single NearMiss instances.

    Args:
        DRYResource (DRYResource): simplify RESTFul API building.
    """
    
    def __init__(self):
        super().__init__(NearMiss)
from app.crud.crudBase import CRUDBase
from app.models import ProductionBatch


class CRUDBatch(CRUDBase):
    pass


batch_crud = CRUDBatch(ProductionBatch)

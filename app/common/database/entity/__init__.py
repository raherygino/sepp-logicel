from .entity import Entity
from .student import Student
from .mouvement import Mouvement

class EntityFactory:
    """ Entity factory """

    @staticmethod
    def create(table: str):
        """ create an entity instance

        Parameters
        ----------
        table: str
            database table name corresponding to entity

        Returns
        -------
        entity:
            entity instance
        """
        tables = {
            "tbl_student": Student,
            "tbl_mouvement": Mouvement
        }
        if table not in tables:
            raise ValueError(f"Table name `{table}` is illegal")

        return tables[table]()

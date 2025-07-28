"""Module for functions associated with states at streamlit."""
import pandas as pd
from abc import ABC


class StreamlitDataFrameState(ABC):
    """Class to help organization of streamlit states."""

    STATE: str = None
    """Name of the state that will be used at streamlit."""
    COLUMNS_TYPES: dict = None
    """A dictionary with types associated with state that will be saved."""

    def __init_subclass__(cls, **kwargs):
        """Function used to guaranty that class attributes are set.

        Raises:
            TypeError:
                If STATE or COLUMNS_TYPES attributes are not set when
                using ABC class for inheritance.
        """
        super().__init_subclass__(**kwargs)
        msg_template = (
            "{cls_name} must define a class attribute '{attribute}'")
        state = getattr(cls, 'STATE', None)
        if state is None:
            raise TypeError(msg_template.format(
                cls_name=cls.__name__, attribute='STATE'))

        columns_types = getattr(cls, 'COLUMNS_TYPES', None)
        if columns_types is None:
            raise TypeError(msg_template.format(
                cls_name=cls.__name__, attribute='COLUMNS_TYPES'))

    @classmethod
    def convert_dataframe_types(cls, data: pd.DataFrame | list
                                ) -> pd.DataFrame:
        """Convert columns type and fill with NA missing data.

        Convert dataframe column types and fill missing columns with NA if
        necessary
        """
        columns = cls.COLUMNS_TYPES.keys()
        return pd.DataFrame(data, columns=columns)\
            .astype(cls.COLUMNS_TYPES)

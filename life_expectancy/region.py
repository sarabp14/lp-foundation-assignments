from enum import Enum
from typing import List

class Region(Enum):
    """Enum representing various regions and countries in Europe and surrounding areas."""
    AT = "AT"
    BE = "BE"
    BG = "BG"
    CH = "CH"
    CY = "CY"
    CZ = "CZ"
    DK = "DK"
    EE = "EE"
    EL = "EL"
    ES = "ES"
    EU27_2020 = "EU27_2020"
    FI = "FI"
    FR = "FR"
    HR = "HR"
    HU = "HU"
    IS = "IS"
    IT = "IT"
    LI = "LI"
    LT = "LT"
    LU = "LU"
    LV = "LV"
    MT = "MT"
    NL = "NL"
    NO = "NO"
    PL = "PL"
    PT = "PT"
    RO = "RO"
    SE = "SE"
    SI = "SI"
    SK = "SK"
    DE = "DE"
    DE_TOT = "DE_TOT"
    AL = "AL"
    EA18 = "EA18"
    EA19 = "EA19"
    EFTA = "EFTA"
    IE = "IE"
    ME = "ME"
    MK = "MK"
    RS = "RS"
    AM = "AM"
    AZ = "AZ"
    GE = "GE"
    TR = "TR"
    UA = "UA"
    BY = "BY"
    EEA30_2007 = "EEA30_2007"
    EEA31 = "EEA31"
    EU27_2007 = "EU27_2007"
    EU28 = "EU28"
    UK = "UK"
    XK = "XK"
    FX = "FX"
    MD = "MD"
    SM = "SM"
    RU = "RU"

    @classmethod
    def countries(cls) -> List["Region"]:
        """        Returns a list of regions excluding aggregates like EU, EEA, and EA.
        """
         # Exclude aggregate regions
         # These are the regions that are not individual countries
         # but rather aggregates or unions of multiple countries.
         # They are not suitable for country-specific analysis.
         # The excluded regions are:
        excluded = {
            cls.DE_TOT,
            cls.EU27_2020,
            cls.EU27_2007,
            cls.EU28,
            cls.EEA30_2007,
            cls.EEA31,
            cls.EFTA,
            cls.EA18,
            cls.EA19,
        }
        return [r for r in cls if r not in excluded]

print(dir(Region))
print(hasattr(Region, "countries"))

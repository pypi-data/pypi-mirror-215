from typing import Any, Dict

import requests
from pydantic import BaseModel

from entityshape.exceptions import ApiError, EidError, LangError, QidError


class EntityShape(BaseModel):
    """This class models the entityshape API
    It has a default timeout of 10 seconds

    The API currently only support items"""

    qid = ""  # item
    eid = ""  # entityshape
    lang = ""  # language
    timeout: int = 10
    result: Dict[Any, Any] = {}

    def __check__(self):
        if not self.lang:
            raise LangError("We only support 2 and 3 letter language codes")
        if not self.eid:
            raise EidError("We need an entityshape EID")
        if not self.qid:
            raise QidError("We need an item QID")

    def get_result(self) -> Dict[Any, Any]:
        """This method checks if we got the 3 parameters we need and
        gets the results and return them"""
        self.__check__()
        url = f"http://entityshape.toolforge.org/api?entity={self.qid}&entityschema={self.eid}&language={self.lang}"
        response = requests.get(url, timeout=self.timeout)
        if response.status_code == 200:
            self.result = response.json()
            # print(self.result)
            return self.result
        else:
            raise ApiError(f"Got {response.status_code} from the entityshape API")

    # def check_lang(self):
    #     if not self.lang or 4 > len(self.lang) > 1:
    #         raise LangError("We only support 2 and 3 letter language codes")
    #
    # def check_eid(self):
    #     if not self.eid or :
    #         raise LangError("We only support 2 and 3 letter language codes")

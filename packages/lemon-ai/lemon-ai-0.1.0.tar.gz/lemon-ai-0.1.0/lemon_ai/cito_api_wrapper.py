import json
import requests
from requests import Request, Session
from typing import List, Dict, Optional

class CitoAPIWrapper():

    api_base_url: str = "http://localhost:1313/api/v0/"

    def _get_session(self) -> Session:
        
        session = requests.session()
        session.headers.update(
            {
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )

        return session

    def get_tool_list(self) -> List[Dict]:

        session = self._get_session()
        url = f"{self.api_base_url}tools"
        response = session.get(url)
        response.raise_for_status()

        return response.json()
    
    def _get_action_request(
        self, id: str, action_input: str, params: Optional[Dict]
    ) -> Request:
        
        data = params if params else {}
        json_obj = json.loads(action_input.replace("'", "\""))

        data.update(json_obj)

        return Request(
            method="POST",
            url=f"{self.api_base_url}tool/{id}/execute",
            json=data,
        )

    def run(self, id: str, action_input: str, params: Optional[Dict], api_key: Optional[str]) -> Dict:
        
        session = self._get_session()
        if api_key:
            session.params = {"api_key": api_key}

        request = self._get_action_request(id, action_input, params)

        response = session.send(session.prepare_request(request))
        response.raise_for_status()
        return response.json()   

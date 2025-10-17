from typing import Optional

class GigachatClientContext:
    def __init__(self):
        self._token: Optional[str] = None
        self._site_name: Optional[str] = None
        self._model: Optional[str] = None
        self._temperature: Optional[str] = None
        self._api_uri: Optional[str] = None
        self._repetition_penalty: Optional[float] = None

    # Token
    @property
    def token(self) -> Optional[str]:
        return self._token

    @token.setter
    def token(self, value: Optional[str]) -> None:
        self._token = value

    # Model
    @property
    def model(self) -> Optional[str]:
        return self._model

    @model.setter
    def model(self, value: Optional[str]) -> None:
        self._model = value

    # Temperature
    @property
    def temperature(self) -> Optional[str]:
        return self._temperature

    @temperature.setter
    def temperature(self, value: Optional[str]) -> None:
        self._temperature = value

    # API URI
    @property
    def api_uri(self) -> Optional[str]:
        return self._api_uri

    @api_uri.setter
    def api_uri(self, value: Optional[str]) -> None:
        self._api_uri = value

    @property
    def repetition_penalty(self) -> Optional[str]:
        return self._repetition_penalty

    @repetition_penalty.setter
    def repetition_penalty(self, value: Optional[str]) -> None:
        self._repetition_penalty = value
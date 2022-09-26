from typing import Optional

from .base import Base
from .key_helper import KeyHelper
from .paths import CREATE_ACCOUNT_SMS_PATH, VERIFY_ACCOUNT_CODE_PATH
from .utils import Singleton


class AccountManager(Base, metaclass=Singleton):

    def unique_log_id(self) -> str:
        return self.store.config.KEY_ACCOUNT_PHONE_NUMBER

    @property
    def path(self):
        return CREATE_ACCOUNT_SMS_PATH % (self.store.config.KEY_ACCOUNT_PHONE_NUMBER, "android")

    async def register_with_verification_code(
            self, captcha_token: str = None,
            code: str = None,
            pin: int = None
    ) -> Optional[str]:
        if code:
            return await self.__verify_with_code(code, pin)
        client, err = await self.client.instance()
        if err:
            return err
        addl_path = ''
        if captcha_token:
            captcha_token = captcha_token.replace("signalcaptcha://", "");
            addl_path += f"&captcha={captcha_token}"
        resp, err = await client.get(self.path + addl_path)

        if err:
            self.logger.error(err)
        else:
            self.logger.warning(resp)
        return err

    async def __verify_with_code(self, code: str, pin: int) -> Optional[str]:
        code = code.replace("-", "")
        path = VERIFY_ACCOUNT_CODE_PATH % code
        registration_id = KeyHelper.generate_registration_id()
        if not self.store.config.KEY_KEYS_IDENTITY_PAIR:
            self.store.config.generate_keys()

        body = {

            "registrationId": registration_id,
            "voice": True,
            "video": True,
            "unrestrictedUnidentifiedAccess": False,

        }
        client, err = await self.client.instance()
        if err:
            return err

        data, err = await client.put(path, body)
        if err:
            return err
        self.store.config.KEY_ACCOUNT_REGISTRATION_ID = registration_id
        self.store.config.KEY_ACCOUNT_UUID = data["uuid"]
        self.store.config.KEY_ACCOUNT_PNI = data["pni"]

        self.logger.warning("DDDDD {} === {}", data, err)
        if err:
            self.logger.error(err)

        return err

from typing import Optional
from .account_manager import AccountManager
from .key_helper import KeyHelper
from .http_client import HttpClient
from .paths import CREATE_ACCOUNT_SMS_PATH, VERIFY_ACCOUNT_CODE_PATH
from .store import Store
from .utils import Singleton, Logger


class DeviceManager(AccountManager, metaclass=Singleton):
    
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
        path = CREATE_ACCOUNT_SMS_PATH % (self.store.KEY_ACCOUNT_PHONE_NUMBER, "android")
        if captcha_token:
            captcha_token = captcha_token.replace("signalcaptcha://", "");
            path += f"&captcha={captcha_token}"
        _, err = await client.get(path)

        if err:
            self.logger.error(err)
        return err

    async def __verify_with_code(self, code: str, pin: int) -> Optional[str]:
        code = code.replace("-", "")
        path = VERIFY_ACCOUNT_CODE_PATH % code
        registration_id = KeyHelper.generate_registration_id()
        signaling_key = KeyHelper.generate_signaling_key()
        self.store.set_identity_key_pair()
        
        pair = self.store.get_identity_key_pair()
        raise Exception(pair)
        self.logger.info("ddddd {} === {}", registration_id, signaling_key)
        # false, 1234, null, null, true, null
        body = {

            "registrationId": registration_id,
            "voice": True,
            "video": True,
            "unrestrictedUnidentifiedAccess": False,
            # this.capabilities = capabilities;
            # this.discoverableByPhoneNumber = discoverableByPhoneNumber;
            # this.name = name;
            # this.pniRegistrationId = pniRegistrationId;
        }
        client, err = await self.client.instance()
        if err:
            return err

        data, err = await client.put(path, body)
        if err:
            return err
        self.store.KEY_ACCOUNT_REGISTRATION_ID = registration_id
        self.store.KEY_ACCOUNT_UUID = date["uuid"]
        self.store.KEY_ACCOUNT_PNI = date["pni"]
        
        self.logger.warning("DDDDD {} === {}", data, err)
        if err:
            self.logger.error(err)
            
        return err

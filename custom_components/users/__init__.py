from custom_components.users.const import   DOMAIN,CONFIG_LIST_USERS
from homeassistant.core import (HomeAssistant,Config)
from homeassistant.auth.providers import homeassistant as auth_ha
import logging


_LOGGER = logging.Logger(__name__)


async def async_setup(hass:HomeAssistant, config:Config):    
    users = config[DOMAIN][CONFIG_LIST_USERS]

    auth_provider = auth_ha.async_get_provider(hass)

    if auth_provider is None:
       _LOGGER.warn("Can't find Home Assistant auth")

    for user in users:
        found_user = None
        
        try:
            credentials = auth_provider.async_create_credentials(user)
            credentials.id = user["username"]
            credentials.is_new = False

            found_user = await hass.auth.async_get_or_create_user(credentials)
                    
            await auth_provider.async_add_auth(user["username"], user["password"])
            
            break
        except auth_ha.InvalidUser as error:
            pass
        except ValueError as error:
            # When not found credentials, Will create one new credencial and new user 
            if found_user is None:
                credentials = auth_provider.async_create_credentials(user)
                credentials.id = user["username"]
                credentials.is_new = True

                await hass.auth._store.async_create_user( 
                    name=user["username"],
                    is_owner=False,
                    is_active=True,
                    system_generated=False,
                    credentials=credentials,
                    group_ids=["system-users"]
                )
                
                await auth_provider.async_add_auth(user["username"], user["password"])
            pass

    return True

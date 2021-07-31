from smarthome.custom_components.users.const import  CONFIG_SCHEMA, DOMAIN,CONFIG_LIST_USERS
from homeassistant.core import (HomeAssistant,Config)
from homeassistant.auth.providers import homeassistant as auth_ha
import logging


_LOGGER = logging.Logger(__name__)


async def async_setup(hass:HomeAssistant, config:Config):    

    CONFIG_SCHEMA(config[DOMAIN])

    users = hass.data.get(config[DOMAIN][CONFIG_LIST_USERS], [])

    auth_provider = auth_ha.async_get_provider(hass)

    #users = [
    #    { "username": 'financeiro', "password": 'financeiro' },
    #    { "username": 'portaria', "password": 'portaria' },
    #    { "username": 'rh', "password": 'rh' },
    #    { "username": 'compras', "password": 'compras' },
    #    { "username": 'engenharia', "password": 'engenharia' },
    #    { "username": 'contabilidade', "password": 'contabilidade' },
    #    { "username": 'aluguel', "password": 'aluguel' },
    #    { "username": 'diretoria', "password": 'diretoria' },
    #    { "username": 'comercial', "password": 'comercial' },
    #    { "username": 'advocacia', "password": 'advocacia' },
    #]

    if auth_provider is None:
       _LOGGER.warn("Can't find Home Assistant auth")

    for user in users:
        try:

            await auth_provider.async_add_auth(user["username"], user["password"])
            
        except auth_ha.InvalidUser:
            return

    return True

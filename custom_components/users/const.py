import voluptuous as vol
from homeassistant.helpers import config_validation as cv


DOMAIN = "users"

CONFIG_LIST_USERS = "list_users"


CONFIG_SCHEMA = vol.Schema(
    {   
        vol.Optional(CONFIG_LIST_USERS): cv.List, 
    }
)
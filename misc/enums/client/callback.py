from enum import Enum


class ClientMainMenuEnum(str, Enum):
    EARN = "toEarn"
    POLITIC = "politicConf"
    ACCEPT_POLITIC = "acceptOurPolitic"
    DONT_ACCEPT_POLITIC = "dontAcceptPolitic"


class ClientBegineMenuEnum(str, Enum):
    SHOW_BETUSX_STRATEGY = "showMeBetusxStrategy"
    SHOW_XUY_STRATEGY = "showMeXuyStrategy"

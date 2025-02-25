from enum import Enum


class AdminMainMenu(str, Enum):
    ADD_PROMO = "addPromoCodeCall"
    DELETE_PROMO = "deletePromoCall"
    CLOSE_PANEL = "closePanelAdminCall"
    SHOW_ACTIVE = "showActivePromoCall"
    ADD_REF = "addReferalLinkCall"
    ADD_STRATEG = "addNewStrategCall"

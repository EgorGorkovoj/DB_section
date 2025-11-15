class LengthConstants:
    """
    Базовый класс констант для ограничения длины символов полей.

    Атрибуты:
    - TITLE_LENGTH (int): Максимальная длина названия.
    - EMAIL_LENGTH (int): Максимальная длина почты.
    """

    TITLE_LENGTH: int = 120
    EMAIL_LENGTH: int = 254


class PriceConstants:
    """
    Базовый класс констант для цен.

    Атрибуты:
    - PRICE_NUMBER_OF_DIGITS (int): целая часть цены.
    - PRICE_FRACTIONAL_PART (int): сколько знаков после запятой у цены.
    """

    PRICE_NUMBER_OF_DIGITS: int = 10
    PRICE_FRACTIONAL_PART: int = 2


class DefaultValueConstants:
    """
    Базовый класс констант для значений по умолчанию в БД.

    Атрибуты:
    - AMOUNT (int): Количество книг.
    """

    AMOUNT: int = 0

# collect.py

from typing import (
    Optional, Dict, Iterable,
    List, Callable, Union, Any, Tuple
)

from represent import BaseModel

from multithreading import Caller, multi_threaded_call

from crypto_screening.process import (
    find_string_value, upper_string_values,
    collect_mutual_string_values, lower_string_values
)
from crypto_screening.exchanges import EXCHANGES, EXCHANGE_NAMES
from crypto_screening.symbols import (
    symbol_to_parts, adjust_symbol, Separator
)

__all__ = [
    "collect_exchanges_assets",
    "collect_exchanges_symbols",
    "collect_mutual_assets",
    "collect_mutual_symbols",
    "is_valid_symbol",
    "validate_symbol",
    "is_valid_exchange",
    "validate_exchange",
    "keep_symbols",
    "filter_symbols",
    "collect_exchange_assets",
    "collect_exchange_quote_assets",
    "collect_exchanges_data",
    "collect_exchange_symbols",
    "collect_exchange_base_assets",
    "collect_all_exchange_symbols",
    "matching_symbol_pair",
    "matching_symbol_pairs",
    "MarketSymbolSignature",
    "matching_symbol_signatures"
]

def keep_symbols(
        symbols: Iterable[str],
        separator: Optional[str] = None,
        adjust: Optional[bool] = True,
        bases: Optional[Iterable[str]] = None,
        quotes: Optional[Iterable[str]] = None,
        included: Optional[Iterable[str]] = None
) -> List[str]:
    """
    Removes all symbols with not matching base or quote.

    :param symbols: The symbols to filter.
    :param separator: The separator for the symbols.
    :param bases: The bases to include.
    :param adjust: The value to adjust the invalid exchanges.
    :param quotes: The quotes to include.
    :param included: The symbols to include.

    :return: The filtered symbols.
    """

    saved = []

    quotes = upper_string_values(quotes or [])
    bases = upper_string_values(bases or [])
    included = upper_string_values(included or [])

    for symbol in symbols:
        symbol = adjust_symbol(symbol=symbol, separator=separator)

        if symbol in included:
            saved.append(symbol)
        # end if

        try:
            base, quote = symbol_to_parts(
                symbol=symbol, separator=separator
            )

        except ValueError as e:
            if adjust:
                continue

            else:
                raise e
            # end if
        # end try

        if (
            (find_string_value(value=base, values=bases) in bases) or
            (find_string_value(value=quote, values=quotes) in quotes)
        ):
            saved.append(symbol)
        # end if
    # end for

    return saved
# end keep_symbols

def filter_symbols(
        symbols: Iterable[str],
        separator: Optional[str] = None,
        adjust: Optional[bool] = True,
        bases: Optional[Iterable[str]] = None,
        quotes: Optional[Iterable[str]] = None,
        excluded: Optional[Iterable[str]] = None
) -> List[str]:
    """
    Removes all symbols with the matching base or quote.

    :param symbols: The symbols to filter.
    :param separator: The separator for the symbols.
    :param bases: The bases to exclude.
    :param quotes: The quotes to exclude.
    :param adjust: The value to adjust the invalid exchanges.
    :param excluded: The symbols to exclude.

    :return: The filtered symbols.
    """

    saved = []

    quotes = upper_string_values(quotes or [])
    bases = upper_string_values(bases or [])
    excluded = upper_string_values(excluded or [])

    for symbol in symbols:
        symbol = adjust_symbol(symbol=symbol, separator=separator)

        if symbol in excluded:
            continue
        # end if

        try:
            base, quote = symbol_to_parts(
                symbol=symbol, separator=separator
            )

        except ValueError as e:
            if adjust:
                continue

            else:
                raise e
            # end if
        # end try

        if (
            (find_string_value(value=base, values=bases) in bases) or
            (find_string_value(value=quote, values=quotes) in quotes)
        ):
            continue
        # end if

        saved.append(symbol)
    # end for

    return saved
# end filter_symbols

def collect_all_exchange_symbols(
        exchange: str,
        separator: Optional[str] = None,
        adjust: Optional[bool] = True,
) -> Iterable[str]:
    """
    Collects the symbols from the exchanges.

    :param exchange: The name of the exchange.
    :param adjust: The value to adjust the invalid exchanges.
    :param separator: The separator of the assets.

    :return: The data of the exchanges.
    """

    validate_exchange(exchange=exchange, exchanges=EXCHANGE_NAMES)

    try:
        exchange_symbols: Iterable[str] = EXCHANGES[exchange].symbols()

    except Exception as e:
        raise RuntimeError(
            f"Cannot fetch symbols of '{exchange}' exchange."
        ) from e
    # end try

    symbols = []

    if separator is None:
        separator = Separator.value
    # end if

    for symbol in exchange_symbols:
        symbol = adjust_symbol(symbol=symbol, separator=separator)

        try:
            if symbol.count(separator) != 1:
                raise ValueError(
                    f"Invalid symbol structure: {symbol}. "
                    f"Symbol must contain only one separator."
                )
            # end if

            base, quote = symbol_to_parts(symbol=symbol, separator=separator)

            if base.startswith("TEST") and quote.startswith("TEST"):
                continue
            # end if

            symbols.append(symbol)

        except ValueError as e:
            if adjust:
                continue

            else:
                raise e
            # end if
        # end try
    # end for

    return symbols
# end collect_all_exchange_symbols

def collect_all_exchange_assets(
        exchange: str,
        separator: Optional[str] = None,
        adjust: Optional[bool] = True,
) -> Iterable[str]:
    """
    Collects the symbols from the exchanges.

    :param exchange: The name of the exchange.
    :param adjust: The value to adjust the invalid exchanges.
    :param separator: The separator of the assets.

    :return: The data of the exchanges.
    """

    symbols = collect_all_exchange_symbols(
        exchange=exchange, adjust=adjust, separator=separator
    )

    assets = []

    for symbol in symbols:
        base, quote = symbol_to_parts(symbol=symbol, separator=separator)

        if base not in assets:
            assets.append(base)
        # end if

        if quote not in assets:
            assets.append(quote)
        # end if
    # end for

    return assets
# end collect_all_exchange_assets

def collect_all_exchange_base_assets(
        exchange: str,
        separator: Optional[str] = None,
        adjust: Optional[bool] = True,
) -> Iterable[str]:
    """
    Collects the symbols from the exchanges.

    :param exchange: The name of the exchange.
    :param adjust: The value to adjust the invalid exchanges.
    :param separator: The separator of the assets.

    :return: The data of the exchanges.
    """

    symbols = collect_all_exchange_symbols(
        exchange=exchange, adjust=adjust, separator=separator
    )

    assets = []

    for symbol in symbols:
        base, _ = symbol_to_parts(symbol=symbol, separator=separator)

        if base not in assets:
            assets.append(base)
        # end if
    # end for

    return assets
# end collect_all_exchange_base_assets

def collect_all_exchange_quote_assets(
        exchange: str,
        separator: Optional[str] = None,
        adjust: Optional[bool] = True,
) -> Iterable[str]:
    """
    Collects the symbols from the exchanges.

    :param exchange: The name of the exchange.
    :param adjust: The value to adjust the invalid exchanges.
    :param separator: The separator of the assets.

    :return: The data of the exchanges.
    """

    symbols = collect_all_exchange_symbols(
        exchange=exchange, adjust=adjust, separator=separator
    )

    assets = []

    for symbol in symbols:
        _, quote = symbol_to_parts(symbol=symbol, separator=separator)

        if quote not in assets:
            assets.append(quote)
        # end if
    # end for

    return assets
# end collect_all_exchange_quote_assets

def collect_exchange_symbols(
        exchange: str,
        separator: Optional[str] = None,
        adjust: Optional[bool] = True,
        bases: Optional[Iterable[str]] = None,
        quotes: Optional[Iterable[str]] = None,
        excluded: Optional[Iterable[str]] = None
) -> Iterable[str]:
    """
    Collects the symbols from the exchanges.

    :param exchange: The name of the exchange.
    :param quotes: The quotes of the asset pairs.
    :param adjust: The value to adjust the invalid exchanges.
    :param bases: The bases of the asset pairs.
    :param separator: The separator of the assets.
    :param excluded: The excluded symbols.

    :return: The data of the exchanges.
    """

    exchange_symbols = collect_all_exchange_symbols(
        exchange=exchange, adjust=adjust, separator=separator
    )

    return list(
        set(
            filter_symbols(
                symbols=keep_symbols(
                    symbols=exchange_symbols,
                    bases=bases, quotes=quotes, separator=separator
                ), excluded=excluded, separator=separator, adjust=adjust
            )
        )
    )
# end collect_exchange_symbols

def collect_exchange_assets(
        exchange: str,
        separator: Optional[str] = None,
        adjust: Optional[bool] = True,
        bases: Optional[Iterable[str]] = None,
        quotes: Optional[Iterable[str]] = None,
        excluded: Optional[Iterable[str]] = None
) -> Iterable[str]:
    """
    Collects the assets from the exchanges.

    :param exchange: The name of the exchange.
    :param bases: The bases of the asset pairs.
    :param quotes: The quotes of the asset pairs.
    :param adjust: The value to adjust the invalid exchanges.
    :param separator: The separator for the symbols.
    :param excluded: The excluded symbols.

    :return: The data of the exchanges.
    """

    symbols = collect_exchange_symbols(
        exchange=exchange, separator=separator, bases=bases,
        quotes=quotes, excluded=excluded, adjust=adjust
    )

    assets = []

    for symbol in symbols:
        base, quote = symbol_to_parts(symbol=symbol, separator=separator)

        if base not in assets:
            assets.append(base)
        # end if

        if quote not in assets:
            assets.append(quote)
        # end if
    # end for

    return assets
# end collect_exchange_assets

def collect_exchange_base_assets(
        exchange: str,
        separator: Optional[str] = None,
        adjust: Optional[bool] = True,
        bases: Optional[Iterable[str]] = None,
        quotes: Optional[Iterable[str]] = None,
        excluded: Optional[Iterable[str]] = None
) -> Iterable[str]:
    """
    Collects the assets from the exchanges.

    :param exchange: The name of the exchange.
    :param bases: The bases of the asset pairs.
    :param adjust: The value to adjust the invalid exchanges.
    :param quotes: The quotes of the asset pairs.
    :param separator: The separator for the symbols.
    :param excluded: The excluded symbols.

    :return: The data of the exchanges.
    """

    symbols = collect_exchange_symbols(
        exchange=exchange, separator=separator, bases=bases,
        quotes=quotes, excluded=excluded, adjust=adjust
    )

    assets = []

    for symbol in symbols:
        base, _ = symbol_to_parts(symbol=symbol, separator=separator)

        if base not in assets:
            assets.append(base)
        # end if
    # end for

    return assets
# end collect_exchange_assets

def collect_exchange_quote_assets(
        exchange: str,
        separator: Optional[str] = None,
        adjust: Optional[bool] = True,
        bases: Optional[Iterable[str]] = None,
        quotes: Optional[Iterable[str]] = None,
        excluded: Optional[Iterable[str]] = None
) -> Iterable[str]:
    """
    Collects the assets from the exchanges.

    :param exchange: The name of the exchange.
    :param bases: The bases of the asset pairs.
    :param adjust: The value to adjust the invalid exchanges.
    :param quotes: The quotes of the asset pairs.
    :param separator: The separator for the symbols.
    :param excluded: The excluded symbols.

    :return: The data of the exchanges.
    """

    symbols = collect_exchange_symbols(
        exchange=exchange, separator=separator, bases=bases,
        quotes=quotes, excluded=excluded, adjust=adjust
    )

    assets = []

    for symbol in symbols:
        _, quote = symbol_to_parts(symbol=symbol, separator=separator)

        if quote not in assets:
            assets.append(quote)
        # end if
    # end for

    return assets
# end collect_exchange_assets

Collector = Callable[
    [
        str,
        Optional[str],
        Optional[bool],
        Optional[Iterable[str]],
        Optional[Iterable[str]],
        Optional[Iterable[str]]
    ], Any
]

def collect_exchanges_data(
        collector: Collector,
        adjust: Optional[bool] = True,
        separator: Optional[str] = None,
        exchanges: Optional[Iterable[str]] = None,
        bases: Optional[Iterable[str]] = None,
        quotes: Optional[Iterable[str]] = None,
        excluded: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None
) -> Dict[str, Any]:
    """
    Collects the symbols from the exchanges.

    :param collector: The collector function to collect data from an exchange.
    :param exchanges: The exchanges.
    :param bases: The bases of the asset pairs.
    :param adjust: The value to adjust the invalid exchanges.
    :param separator: The separator of the assets.
    :param quotes: The quotes of the asset pairs.
    :param excluded: The excluded symbols.

    :return: The data of the exchanges.
    """

    excluded_symbols = []

    excluded = excluded or {}

    if not excluded:
        excluded_symbols = excluded
    # end if

    if (
        excluded and
        all(isinstance(value, str) for value in excluded) and
        not isinstance(excluded, dict)
    ):
        excluded = {exchange: excluded_symbols for exchange in exchanges}
    # end if

    exchanges = lower_string_values(exchanges or EXCHANGE_NAMES)

    markets = []

    for exchange in exchanges:
        exchange = find_string_value(value=exchange, values=EXCHANGE_NAMES)

        if exchange not in EXCHANGE_NAMES:
            if adjust:
                continue

            else:
                validate_exchange(exchange=exchange, exchanges=EXCHANGE_NAMES)
            # end if
        # end if

        markets.append(exchange)
    # end for

    callers = []
    data: Dict[str, Caller] = {}

    for exchange in markets:
        exchange = find_string_value(value=exchange, values=exchanges)

        caller = Caller(
            target=collector,
            kwargs=dict(
                exchange=exchange,
                separator=separator,
                quotes=quotes,
                adjust=adjust,
                bases=bases,
                excluded=excluded[exchange] if exchange in excluded else None
            )
        )

        callers.append(caller)
        data[exchange] = caller
    # end for

    multi_threaded_call(callers=callers)

    return {key: value.results.returns for key, value in data.items() if value}
# end collect_exchanges_symbols

def collect_exchanges_assets(
        exchanges: Optional[Iterable[str]] = None,
        adjust: Optional[bool] = True,
        separator: Optional[str] = None,
        bases: Optional[Iterable[str]] = None,
        quotes: Optional[Iterable[str]] = None,
        excluded: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None
) -> Dict[str, List[str]]:
    """
    Collects the symbols from the exchanges.

    :param exchanges: The exchanges.
    :param quotes: The quotes of the asset pairs.
    :param bases: The bases of the asset pairs.
    :param excluded: The excluded symbols.
    :param adjust: The value to adjust the invalid exchanges.
    :param separator: The separator of the assets.

    :return: The data of the exchanges.
    """

    return collect_exchanges_data(
        collector=collect_exchange_assets,
        exchanges=exchanges, quotes=quotes, excluded=excluded,
        adjust=adjust, separator=separator, bases=bases
    )
# end collect_exchanges_symbols

def collect_mutual_assets(
        exchanges: Optional[Iterable[str]] = None,
        adjust: Optional[bool] = True,
        separator: Optional[str] = None,
        bases: Optional[Iterable[str]] = None,
        quotes: Optional[Iterable[str]] = None,
        excluded: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
        data: Optional[Dict[str, Iterable[str]]] = None
) -> Dict[str, List[str]]:
    """
    Collects the symbols from the exchanges.

    :param exchanges: The exchanges.
    :param quotes: The quotes of the asset pairs.
    :param bases: The bases of the asset pairs.
    :param excluded: The excluded symbols.
    :param adjust: The value to adjust the invalid exchanges.
    :param separator: The separator of the assets.
    :param data: The data to search in.

    :return: The data of the exchanges.
    """

    return collect_mutual_string_values(
        data=data or collect_exchanges_assets(
            exchanges=exchanges, quotes=quotes, bases=bases,
            excluded=excluded, adjust=adjust, separator=separator
        )
    )
# end collect_mutual_assets

def collect_exchanges_symbols(
        exchanges: Optional[Iterable[str]] = None,
        adjust: Optional[bool] = True,
        separator: Optional[str] = None,
        quotes: Optional[Iterable[str]] = None,
        excluded: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None
) -> Dict[str, List[str]]:
    """
    Collects the symbols from the exchanges.

    :param exchanges: The exchanges.
    :param quotes: The quotes of the asset pairs.
    :param excluded: The excluded symbols.
    :param adjust: The value to adjust the invalid exchanges.
    :param separator: The separator of the assets.

    :return: The data of the exchanges.
    """

    return collect_exchanges_data(
        collector=collect_exchange_symbols,
        exchanges=exchanges, quotes=quotes, excluded=excluded,
        adjust=adjust, separator=separator
    )
# end collect_exchanges_symbols

def collect_mutual_symbols(
        exchanges: Optional[Iterable[str]] = None,
        adjust: Optional[bool] = True,
        separator: Optional[str] = None,
        quotes: Optional[Iterable[str]] = None,
        excluded: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
        data: Optional[Dict[str, Iterable[str]]] = None
) -> Dict[str, List[str]]:
    """
    Collects the symbols from the exchanges.

    :param exchanges: The exchanges.
    :param quotes: The quotes of the asset pairs.
    :param excluded: The excluded symbols.
    :param adjust: The value to adjust the invalid exchanges.
    :param separator: The separator of the assets.
    :param data: The data to search in.

    :return: The data of the exchanges.
    """

    return collect_mutual_string_values(
        data=data or collect_exchanges_symbols(
            exchanges=exchanges, quotes=quotes, excluded=excluded,
            adjust=adjust, separator=separator
        )
    )
# end collect_mutual_symbols

def matching_symbol_pair(
        symbol1: str,
        symbol2: str, /, *,
        matches: Optional[Iterable[Iterable[str]]] = None,
        separator: Optional[str] = None
) -> bool:
    """
    Checks if the symbols are valid with the matching currencies.

    :param symbol1: The first ticker.
    :param symbol2: The second ticker.
    :param matches: The currencies.
    :param separator: The separator of the assets.

    :return: The validation value for the symbols.
    """

    symbol1 = adjust_symbol(symbol=symbol1, separator=separator)
    symbol2 = adjust_symbol(symbol=symbol2, separator=separator)

    if symbol1 == symbol2:
        return True
    # end if

    asset1, currency1 = symbol_to_parts(symbol=symbol1, separator=separator)
    asset2, currency2 = symbol_to_parts(symbol=symbol2, separator=separator)

    if asset1 != asset2:
        return False
    # end if

    matches = matches or []

    for matches in matches:
        if (currency1 in matches) and (currency2 in matches):
            return True
        # end if

        if (
            ((currency1 in matches) and (currency2 not in matches)) or
            ((currency1 not in matches) and (currency2 in matches))
        ):
            return False
        # end if
    # end for

    return False
# end matching_symbol_pair

def matching_symbol_pairs(
        data: Dict[str, Iterable[str]],
        matches: Optional[Iterable[Iterable[str]]] = None,
        separator: Optional[str] = None
) -> List[Tuple[Tuple[str, str], Tuple[str, str]]]:
    """
    Checks if the symbols are valid with the matching currencies.

    :param data: The symbols.
    :param matches: The currencies.
    :param separator: The separator of the assets.

    :return: The validation value for the symbols.
    """

    pairs = []
    symbols = []

    for exchange, exchange_symbols in data.items():
        symbols.extend([(exchange, symbol) for symbol in exchange_symbols])
    # end for

    for exchange1, symbol1 in symbols:
        for exchange2, symbol2 in symbols:
            if (
                (exchange1 != exchange2) and
                matching_symbol_pair(
                    symbol1, symbol2, matches=matches,
                    separator=separator
                )
            ):
                pairs.append(((exchange1, symbol1), (exchange2, symbol2)))
            # end if
        # end for
    # end for

    return pairs
# end matching_symbol_pairs

def is_valid_symbol(
        exchange: str,
        symbol: str,
        exchanges: Optional[Iterable[str]] = None,
        symbols: Optional[Iterable[str]] = None
) -> bool:
    """
    Returns a value for the symbol being valid for the source exchange.

    :param exchange: The name of the exchange platform.
    :param symbol: The symbol of the assets.
    :param symbols: The valid symbols.
    :param exchanges: The valid exchanges.

    :return: The validation-value.
    """

    if symbols is None:
        exchange = find_string_value(value=exchange, values=EXCHANGE_NAMES)

        if not is_valid_exchange(
            exchange=exchange, exchanges=exchanges
        ):
            return False
        # end if

        symbols = EXCHANGES[exchange].symbols()
    # end for

    symbols = [adjust_symbol(symbol=s) for s in symbols]

    symbol = find_string_value(value=adjust_symbol(symbol=symbol), values=symbols)

    return symbol in symbols
# end is_valid_symbol

def validate_symbol(
        exchange: str,
        symbol: str,
        exchanges: Optional[Iterable[str]] = None,
        symbols: Optional[Iterable[str]] = None,
        provider: Optional[Any] = None
) -> str:
    """
    Returns a value for the symbol being valid for the source exchange.

    :param exchange: The name of the exchange platform.
    :param symbol: The symbol of the assets.
    :param symbols: The valid symbols.
    :param exchanges: The valid exchanges.
    :param provider: Any provider object.

    :return: The validation-value.
    """

    validate_exchange(
        exchange=exchange, exchanges=exchanges,
        provider=provider
    )

    if not is_valid_symbol(
        exchange=exchange, symbol=symbol, symbols=symbols
    ):
        raise ValueError(
            f"'{symbol}' is not a valid "
            f"symbol for the '{exchange}' exchange. "
            f"Valid symbols: {', '.join(symbols)}"
            f"{f' for {provider}.' if provider else ''}"
        )
    # end if

    return symbol
# end validate_symbol

def is_valid_exchange(exchange: str, exchanges: Optional[Iterable[str]] = None) -> bool:
    """
    checks of the source os a valid exchange name.

    :param exchange: The source name to validate.
    :param exchanges: The valid exchanges.

    :return: The validation value.
    """

    if exchanges is None:
        exchanges = EXCHANGE_NAMES
    # end if

    return find_string_value(value=exchange, values=exchanges) in exchanges
# end is_valid_exchange

def validate_exchange(
        exchange: str,
        exchanges: Optional[Iterable[str]] = None,
        provider: Optional[Any] = None
) -> str:
    """
    Validates the source value.

    :param exchange: The name of the exchange platform.
    :param exchanges: The valid exchanges.
    :param provider: Any provider object.

    :return: The validates symbol.
    """

    if exchanges is None:
        exchanges = EXCHANGE_NAMES
    # end if

    if not is_valid_exchange(exchange=exchange, exchanges=exchanges):
        raise ValueError(
            f"'{exchange}' is not a valid exchange name. "
            f"Valid exchanges: {', '.join(exchanges)}"
            f"{f' for {provider}.' if provider else ''}"
        )
    # end if

    return exchange
# end validate_exchange

class MarketSymbolSignature(BaseModel):
    """A class to represent the data for the execution of a trade."""

    __slots__ = "asset", "currency", "exchange"

    def __init__(
            self,
            asset: str,
            currency: str,
            exchange: str
    ) -> None:
        """
        Defines the class attributes.

        :param asset: The traded asset.
        :param currency: The currency to trade the asset with.
        :param exchange: The exchange platform.
        """

        self.asset = asset
        self.exchange = exchange
        self.currency = currency
    # end __init__
# end MarketPairSignature

def matching_symbol_signatures(
        pairs: Optional[List[Tuple[Tuple[str, str], Tuple[str, str]]]] = None,
        data: Optional[Dict[str, Iterable[str]]] = None,
        matches: Optional[Iterable[Iterable[str]]] = None,
        separator: Optional[str] = None
) -> List[Tuple[MarketSymbolSignature, MarketSymbolSignature]]:
    """
    Checks if the screeners are valid with the matching currencies.

    :param data: The data for the pairs.
    :param pairs: The pairs' data.
    :param matches: The currencies.
    :param separator: The separator of the assets.

    :return: The validation value for the symbols.
    """

    if (data is None) and (pairs is None):
        raise ValueError(
            f"One of 'pairs' and 'data' parameters must be given, "
            f"when 'pairs' is superior to 'data'."
        )

    elif (not pairs) and (not data):
        return []
    # end if

    new_pairs = []

    pairs = pairs or matching_symbol_pairs(
        data=data, matches=matches, separator=separator
    )

    for (exchange1, symbol1), (exchange2, symbol2) in pairs:
        asset1, currency1 = symbol_to_parts(symbol1)
        asset2, currency2 = symbol_to_parts(symbol2)

        new_pairs.append(
            (
                MarketSymbolSignature(
                    asset=asset1, currency=currency1,
                    exchange=exchange1
                ),
                MarketSymbolSignature(
                    asset=asset2, currency=currency2,
                    exchange=exchange2
                )
            )
        )
    # end for

    return new_pairs
# end matching_symbol_signatures
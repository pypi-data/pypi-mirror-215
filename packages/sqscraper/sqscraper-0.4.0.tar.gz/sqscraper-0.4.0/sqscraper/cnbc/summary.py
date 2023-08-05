"""
"""

import datetime
import decimal
import operator
import re
import typing
import urllib.parse

import bs4
import numpy as np
import pandas as pd
from playwright import sync_api
from playwright._impl import _api_types

from ._apps import Apps
from ._apps import PageSection
from sqscraper.utils import expand_value
from sqscraper.utils import normalize_value


class StockSummary(Apps):
    """
    """
    def __init__(self, symbol: str):
        super().__init__(symbol, "stocks/summary")

        with sync_api.sync_playwright() as play:
            browser = play.chromium.launch()
            page = browser.new_page()
            page.goto(self._url)

            self.pricing_momentum = _PricingMomentum(self.symbol, self._soup, page)
            self.growth_rates = _GrowthRates(self.symbol, self._soup, page)
            self.key_measures = _KeyMeasures(self.symbol, self._soup, page)

            browser.close()

    @property
    def shares(self) -> pd.Series:
        """
        """
        data = {
            "Shares Outstanding": self.shares_outstanding,
            "Institutional Ownership (%)": self.institutional_ownership,
            "Market Cap": self.market_cap,
            "Last Stock Split (Date)": self.last_stock_split_date,
            "Last Stock Split (Ratio)": self.last_stock_split_ratio
        }
        return pd.Series(data, name="Shares")

    @property
    def shares_outstanding(self) -> int:
        """
        """
        element = self._soup.select_one("table#shares tr:nth-child(1) > td:nth-child(2)")
        return expand_value(element.text)

    @property
    def institutional_ownership(self) -> float:
        """
        """
        element = self._soup.select_one("table#shares tr:nth-child(2) > td:nth-child(2)")
        return float(element.text.strip("%"))
    
    @property
    def market_cap(self) -> int:
        """
        """
        element = self._soup.select_one("table#shares tr:nth-child(3) > td:nth-child(2)")
        return expand_value(element.text)
    
    @property
    def last_stock_split_date(self) -> typing.Optional[datetime.datetime]:
        """
        """
        element = self._soup.select_one("table#shares tr:nth-child(4) > td:nth-child(1)")
        try:
            return datetime.datetime.strptime(element.text, "Last Stock Split %m/%d/%Y")
        except ValueError:
            return np.nan
        
    @property
    def last_stock_split_ratio(self) -> typing.Optional[float]:
        """
        """
        element = self._soup.select_one("table#sharestr:nth-child(4) > td:nth-child(2)")
        regex = re.compile(r"^(.*):(.*)$")
        try:
            return float(
                operator.truediv(
                    *[decimal.Decimal(x) for x in regex.search(element.text).groups()]
                )
            )
        except AttributeError:
            return np.nan
        
    @property
    def analyst_consensus(self) -> typing.Optional[pd.Series]:
        """
        """
        element = self._soup.select_one("div#trends > img")
        if element is None:
            return

        url_components = urllib.parse.urlparse(element.attrs.get("desturl"))
        query_parameters = dict(x.split("=") for x in url_components.query.split("&"))

        ratings = ("Strong Buy", "Buy", "Hold", "Sell", "Underperform")
        return pd.Series(dict(zip(ratings, map(int, query_parameters["data"].split(",")))))


class _PricingMomentum(PageSection):
    """
    :param page:
    :type page: sync_api._generated.Page
    """
    def __init__(self, symbol: str, soup: bs4.BeautifulSoup, page):
        super().__init__(symbol, soup)

        self._performance = self._scrape_performance(page)

    @property
    def quote(self) -> pd.Series:
        """
        """
        data = {
            "Last": self.last,
            "Change": self.change,
            "Change (%)": self.change_pct,
            "Open": self.open,
            "Day High": self.day_high,
            "Day Low": self.day_low,
            "Volume": self.volume
        }
        return pd.Series(data, name="Quote")

    @property
    def last(self) -> float:
        """
        """
        element = self._soup.select_one("span#quoteTable_last")
        return float(element.text)

    @property
    def change(self) -> float:
        """
        """
        element = self._soup.select_one("span#quoteTable_chg > span")
        if "colUnch" in element.attrs.get("class"):
            return np.nan
        elif "colPos" in element.attrs.get("class"):
            return float(element.text)
        elif "colNeg" in element.attrs.get("class"):
            return -float(element.text)
        else:
            raise ValueError

    @property
    def change_pct(self) -> float:
        """
        """
        element = self._soup.select_one("span#quoteTable_chgPct > span")
        if "colUnch" in element.attrs.get("class"):
            return np.nan
        return float(element.text.strip("%"))

    @property
    def open(self) -> float:
        """
        """
        element = self._soup.select_one("span#quoteTable_open")
        return float(element.text)

    @property
    def day_high(self) -> float:
        """
        """
        element = self._soup.select_one("span#quoteTable_high")
        return float(element.text)

    @property
    def day_low(self) -> float:
        """
        """
        element = self._soup.select_one("span#quoteTable_low")
        return float(element.text)

    @property
    def volume(self) -> int:
        """
        """
        element = self._soup.select_one("span#quoteTable_volume")
        return int("".join(element.text.split(",")))

    @property
    def performance(self) -> typing.Dict[str, str]:
        """
        """
        return self._performance

    def _scrape_performance(self, page) -> typing.Dict[str, str]:
        """
        :param page:
        :type page: sync_api._generated.Page
        :return:
        """
        urls = {}

        element_loading = page.locator("div#divLoading")
        element_chart = page.locator("img#performanceChartImg")
        element_checkbox = page.locator("div#chk0")

        element_loading.wait_for(state="detached")

        urls.setdefault("spx-on", element_chart.get_attribute("src"))
        element_checkbox.click()
        element_loading.wait_for(state="detached")

        urls.setdefault("spx-off", element_chart.get_attribute("src"))
        element_checkbox.click()
        element_loading.wait_for(state="detached")

        return {k: f"https://apps.cnbc.com{v}" for k, v in urls.items()}


class _GrowthRates(PageSection):
    """
    """
    def __init__(self, symbol: str, soup: bs4.BeautifulSoup, page):
        super().__init__(symbol, soup)

        self._earnings_per_share = self._scrape_chart(page, "div#rollMapImg0")
        self._revenue = self._scrape_chart(page, "div#rollMapImg1")
        self._dividend = self._scrape_chart(page, "div#rollMapImg2")

    @property
    def earnings_per_share(self) -> typing.Optional[pd.DataFrame]:
        """
        """
        dataframe = self._earnings_per_share.copy()
        if dataframe.empty:
            return None

        dataframe.iloc[:2, :] = dataframe.iloc[:2, :].applymap(
            lambda x: float(normalize_value(x)) if isinstance(x, str) else x
        )
        dataframe.iloc[2, :] = pd.Series(dataframe.iloc[2, :], dtype="Int64")
        dataframe.iloc[3:, :] = dataframe.iloc[3:, :].applymap(
            lambda x: float(normalize_value(x)) if isinstance(x, str) else x
        )

        return dataframe

    @property
    def revenue(self) -> typing.Optional[pd.DataFrame]:
        """
        """
        dataframe = self._revenue.copy()
        if dataframe.empty:
            return None

        dataframe.iloc[:2, :] = dataframe.iloc[:2, :].applymap(
            lambda x: float(normalize_value(x)) if isinstance(x, str) else x
        )
        dataframe.iloc[2, :] = pd.Series(dataframe.iloc[2, :], dtype="Int64")
        dataframe.iloc[3:, :] = dataframe.iloc[3:, :].applymap(
            lambda x: float(normalize_value(x)) if isinstance(x, str) else x
        )

        return dataframe

    @property
    def dividend(self) -> typing.Optional[pd.DataFrame]:
        """
        """
        dataframe = self._dividend.copy()
        if dataframe.empty:
            return None

        dataframe = dataframe.applymap(
            lambda x: float(normalize_value(x)) if isinstance(x, str) else x
        )

        return dataframe

    def _scrape_chart(self, page, selector: str) -> typing.Optional[pd.DataFrame]:
        """
        :param page:
        :type page: sync_api._generated.Page
        :param selector:
        :return:
        """
        regex = re.compile(r"^(\d{4}) (EPS|Revenue|Dividend) Analysis$")

        chart = page.locator(selector)
        chart.hover()
        chart_bars = chart.locator("map > area[shape='rect']")

        popup_heading = page.locator("div#popContent > h1")
        popup_body = page.locator("div#popBody")

        data = {}
        for bar in chart_bars.all():
            bar.dispatch_event("mouseover")

            popup_heading.wait_for(state="visible", timeout=5000)
            year = int(regex.search(popup_heading.text_content()).group(1))
            items =  dict(x.split(": ") for x in popup_body.inner_text().split("\n"))
            data.setdefault(int(year), dict(items))

            bar.dispatch_event("mouseout")

        return pd.DataFrame(data).replace("--", np.nan)


class _KeyMeasures(PageSection):
    """
    """
    def __init__(self, symbol: str, soup: bs4.BeautifulSoup, page):
        super().__init__(symbol, soup)

        self._dataframe = pd.read_html(page.locator("div#keyMeasResults").inner_html())[0]
        self._dataframe.replace("--", np.nan, inplace=True)

    @property
    def valuation(self) -> pd.DataFrame:
        """
        """
        dataframe = self._dataframe.iloc[1:5, 1:5].copy()
        dataframe.index = list(self._dataframe.iloc[1:5, 0])
        dataframe.columns = list(self._dataframe.iloc[0, 1:5])

        return dataframe
    
    @property
    def financial_strength(self) -> pd.DataFrame:
        """
        """
        dataframe = self._dataframe.iloc[6:13, 1:5].copy()
        dataframe.index = list(self._dataframe.iloc[6:13, 0])
        dataframe.columns = list(self._dataframe.iloc[0, 1:5])

        return dataframe
    
    @property
    def assets(self) -> pd.DataFrame:
        """
        """
        dataframe = self._dataframe.iloc[14:17, 1:5].copy()
        dataframe.index = list(self._dataframe.iloc[14:17, 0])
        dataframe.columns = list(self._dataframe.iloc[0, 1:15])

        dataframe.iloc[1, :] = dataframe.iloc[1, :].map(
            lambda x: expand_value(x.strip("$"))
        )

        return dataframe

    @property
    def profitability(self) -> pd.DataFrame:
        """
        """
        dataframe = pd.DataFrame(self._dataframe.iloc[18:22, 1:5].copy())
        dataframe.index = list(self._dataframe.iloc[18:22, 0])
        dataframe.columns = list(self._dataframe.iloc[0, 1:5])

        dataframe.iloc[0, :] = dataframe.iloc[0, :].map(
            lambda x: expand_value(x.strip("$"))
        )
        dataframe.iloc[1:5, :] = dataframe.iloc[1:5, :].applymap(
            lambda x: float(x.strip("%"))
        )

        return dataframe

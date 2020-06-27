import html2text
import json
from pprint import pprint
import re
from lxml import html
import common
import logging

if __name__ == '__main__':

    LOG = logging.getLogger()

    logging.basicConfig(

        format='%(levelname)s/%(module)s:%(lineno)d: %(message)s',

        level=logging.INFO)

else:

    LOG = logging.getLogger(__name__)

LOG.setLevel(logging.INFO)



# Scrapers fetch and parse webpage

# Json readers fetch data from JSON APIs

# all quote() functions returns common.StockQuote





class AAStockScraper(object):

    _aastock_url = 'http://www.aastocks.com/en/stock/detailquote.aspx?symbol=%s'



    @staticmethod

    def quote(symbol, flags=None):

        quote = common.StockQuote(symbol)

        quote.complete_time = common.get_timestamp()

        quote.valid = False

        return quote





class AAStockMScraper(object):

    _aamobile_url = 'http://www.aastocks.com/en/mobile/Quote.aspx?symbol=%s'



    @staticmethod

    def quote(symbol, flags=None):

        # lxml won't take unicode data

        data = common.download_webpage(

            AAStockMScraper._aamobile_url % symbol, noencode=True)

        tree = html.document_fromstring(data)

        # http://lxml.de/api/lxml.html.HtmlElement-class.html



        # create dict for most of the info

        d = {

            e.getparent().text.lower(): e.text

            for e in tree.find_class('float_right')

            }

        LOG.debug("float_right: %s",

                  [e.text for e in tree.find_class('float_right')])



        # day high/low is in cell_last

        LOG.debug('text_last: %s',

                  tree.find_class('cell_last')[0].text_content())

            # '\nLast\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa04.430+0.290(+7.005%)\n L/H4.240-4.450\n'

        match = re.search(r'L/H *([.\d]+)-([.\d]+)',

                          tree.find_class('cell_last')[0].text_content())

        if match:

            LOG.debug('%s', match.groups())

            d['low'] = match.groups()[0]

            d['high'] = match.groups()[1]



        # deals with bidask seperately, append to dict

        LOG.debug('bidask: %s',

                  [e.text_content() for e in tree.find_class('bidask')])

            # ['Bid(Delayed)4.430', 'Ask(Delayed)4.440']

        for e in tree.find_class('bidask'):

            d[e.text.lower()] = re.findall(r'[.\d]+', e.text_content())[0]



        quote = common.StockQuote(symbol)

        quote.quote = d['ask']

        quote.low = d['low']

        quote.high = d['high']

        quote.volume = d['volume']

        quote.opening = d['open']

        quote.close_yest = d['prev. close']

        quote_time = tree.find_class('font12_white')[0].text

        # format as isotime string

        last_update = quote_time.partition(' ')

        quote.quote_time = last_update[1] + 'T' + last_update[2]

        quote.complete_time = common.get_timestamp()

        quote.valid = True

        return quote





class JsonReader(object):

    # ETNet, delayed

    _etnet_url = 'http://gateway.etnet.com.hk/WCData/snapshot.jsp?code=%s'

    # \n\n\n\n\n\n\n\n\n\n\nvar snapshot=[<JSON>]\n



    # Money18, realtime, but it checks the 't=' parameter

    # http://money18.on.cc/js/real/quote/%s_r.js?t=%s



    @staticmethod

    def quote(symbol, flags=None):

        data = common.download_webpage(JsonReader._etnet_url % symbol)

        # strip JSON from reply

        r = re.search(r'\[(.*)\]', data, re.S | re.U)

        if not r:

            quote.complete_time = common.get_timestamp()

            return quote

        d = json.loads(r.groups()[0])



        quote = common.StockQuote(symbol)

        quote.quote = d['ask']

        quote.low = d['low']

        quote.high = d['high']

        quote.volume = d['sharestraded']

        quote.opening = None

        quote.close_yest = d['prvClose']

        # format as isotime string

        SEHKTime = d['SEHKTime'].partition(' ')

        quote.quote_time = SEHKTime[0] + 'T' + SEHKTime[1]

        quote.complete_time = common.get_timestamp()

        quote.valid = True

        return quote



# look up table for scrapers

LUT = {

    'aa': AAStockScraper,

    'AAStockScraper': AAStockScraper,

    'aam': AAStockMScraper,

    'aamobile': AAStockMScraper,

    'AAStockMScraper': AAStockMScraper,

    'json': JsonReader,

    'JsonReader': JsonReader,

}



DEFAULT_PROVIDER = AAStockMScraper
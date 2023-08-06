from time import sleep

from qtl_xtp_api import MdApi, consts


class SampleMdApi(MdApi):

    def __init__(self, settings):
        super().__init__()
        self.settings = settings

        self.tickers = {}

        client_id = self.settings['client_id']
        save_file_path = self.settings['save_file_path']
        log_level = self.settings['log_level']
        self.CreateQuoteApi(client_id, save_file_path, log_level)

    def get_trading_day(self):
        return self.GetTradingDay()

    def get_api_version(self):
        return self.GetApiVersion()

    def login(self):
        ip = self.settings['ip']
        port = self.settings['port']
        user = self.settings['user']
        password = self.settings['password']
        sock_type = consts.XTP_PROTOCOL_TCP
        res = self.Login(ip, port, user, password, sock_type, '')
        if res == 0:
            print(f'Login Success...')
        else:
            error = self.GetApiLastError()
            print(f'Login Error: {error}')

    def query_all_tickers(self, exchange_id):
        print('query_all_tickers...')
        self.QueryAllTickers(exchange_id)

    def subscribe_all_market_data(self, exchange_id):
        self.SubscribeAllMarketData(exchange_id)

    def OnDepthMarketData(self, market_data, bid1_qty, max_bid1_count, ask1_qty, max_ask1_count):
        print('OnDepthMarketData => ')
        print(f'{market_data=}')
        print(f'{bid1_qty=}')
        print(f'{max_bid1_count=}')
        print(f'{ask1_qty=}')
        print(f'{max_ask1_count=}')

    def OnQueryAllTickers(self, ticker_info, error_info, is_last):
        print('OnQueryAllTickers => ')
        print(f'ticker: {ticker_info}')
        self.tickers[(ticker_info['exchange_id'], ticker_info['ticker'])] = ticker_info

    def OnSubscribeAllMarketData(self, exchange_id, error_info):
        print('OnSubscribeAllMarketData => ')
        print(f'{exchange_id=}')
        print(f'{error_info=}')


def main():
    print('Run Sample Md Api...')

    # 注意修改用户名密码，这里使用 xtp 测试服务器
    settings = {
        'client_id': 1,
        'save_file_path': './',
        'log_level': 1,
        'ip': '119.3.103.38',
        'port': 6002,
        'user': '',
        'password': ''
    }

    sample_api = SampleMdApi(settings)
    print(f'ApiVersion: {sample_api.get_api_version()}')

    sample_api.login()
    print(f'TradingDay: {sample_api.get_trading_day()}')

    exchange_id = consts.XTP_EXCHANGE_SH
    sample_api.query_all_tickers(exchange_id)
    sleep(3)
    sample_api.subscribe_all_market_data(exchange_id)
    input('Waiting...\n')


if __name__ == '__main__':
    main()

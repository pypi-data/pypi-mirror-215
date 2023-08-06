from time import sleep

from qtl_xtp_api import TdApi, consts


class SampleTdApi(TdApi):

    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.request_id = 0
        self.session_id = 0

        client_id = self.settings['client_id']
        save_file_path = self.settings['save_file_path']
        log_level = self.settings['log_level']
        software_key = self.settings['software_key']
        self.CreateTraderApi(client_id, save_file_path, log_level)
        self.SetSoftwareKey(software_key)
        self.SubscribePublicTopic(consts.XTP_TERT_QUICK)

    def next_request_id(self):
        self.request_id += 1
        return self.request_id

    def get_api_version(self):
        return self.GetApiVersion()

    def get_trading_day(self):
        return self.GetTradingDay()

    def login(self):
        ip = self.settings['ip']
        port = self.settings['port']
        user = self.settings['user']
        password = self.settings['password']
        sock_type = consts.XTP_PROTOCOL_TCP
        self.session_id = self.Login(ip, port, user, password, sock_type, '')
        if self.session_id != 0:
            print(f'Login Success, session_id: {self.session_id}')
        else:
            error = self.GetApiLastError()
            print(f'Login Error: {error}')

    def query_position(self):
        return self.QueryPosition('', self.session_id, self.next_request_id(), consts.XTP_MKT_INIT)

    def query_asset(self):
        return self.QueryAsset(self.session_id, self.next_request_id())

    def buy(self):
        # sample order
        order = {
            'order_client_id': 123,
            'ticker': '600519',
            'market': consts.XTP_MKT_SH_A,
            'price': 1750.0,
            'quantity': 100,
            'price_type': consts.XTP_PRICE_LIMIT,
            'side': 1,  # XTP_SIDE_BUY
            'business_type': consts.XTP_BUSINESS_TYPE_CASH
        }
        return self.InsertOrder(order, self.session_id)

    def OnError(self, error_info):
        print(f'OnError => {error_info=}')

    def OnOrderEvent(self, order_info, error_info, session_id):
        print('OnOrderEvent => ')
        print(f'  {session_id=}')
        print(f'  {error_info=}')
        print(f'  {order_info=}')

    def OnTradeEvent(self, trade_info, session_id):
        print('OnTradeEvent => ')
        print(f'  {session_id=}')
        print(f'  {trade_info=}')

    def OnCancelOrderError(self, cancel_info, error_info, session_id):
        print('OnCancelOrderError => ')
        print(f'  {session_id=}')
        print(f'  {error_info=}')
        print(f'  {cancel_info=}')

    def OnQueryOrder(self, order_info, error_info, request_id, is_last, session_id):
        print('OnQueryOrder => ')
        print(f'  {session_id=}')
        print(f'  {request_id=}')
        print(f'  {is_last=}')
        print(f'  {error_info=}')
        print(f'  {order_info=}')

    def OnQueryTrade(self, trade_info, error_info, request_id, is_last, session_id):
        print('OnQueryTrade => ')
        print(f'  {session_id=}')
        print(f'  {request_id=}')
        print(f'  {is_last=}')
        print(f'  {error_info=}')
        print(f'  {trade_info=}')

    def OnQueryPosition(self, position, error_info, request_id, is_last, session_id):
        print('OnQueryPosition => ')
        print(f'  {session_id=}')
        print(f'  {request_id=}')
        print(f'  {is_last=}')
        print(f'  {error_info=}')
        print(f'  {position=}')

    def OnQueryAsset(self, asset, error_info, request_id, is_last, session_id):
        print('OnQueryAsset => ')
        print(f'  {session_id=}')
        print(f'  {request_id=}')
        print(f'  {is_last=}')
        print(f'  {error_info=}')
        print(f'  {asset=}')


def main():
    print('Run Sample Td Api...')

    # 注意修改用户名密码，这里使用 xtp 测试服务器
    settings = {
        'client_id': 1,
        'save_file_path': './',
        'log_level': 1,
        'ip': '122.112.139.0',
        'port': 6101,
        'user': '15007306',
        'password': 'C5WPbvZi',
        'software_key': 'b8aa7173bba3470e390d787219b2112e'
    }

    sample_api = SampleTdApi(settings)
    print(f'ApiVersion: {sample_api.get_api_version()}')

    sample_api.login()
    print(f'TradingDay: {sample_api.get_trading_day()}')

    sample_api.query_position()
    sleep(2)
    sample_api.query_asset()
    sleep(2)
    sample_api.buy()

    input('Waiting...\n')


if __name__ == '__main__':
    main()

import pandas_datareader.data as web
from threading import Thread

results = []

def get_data(symbol):
    global results
    markets  = {
            'R2.F' : 'MSCI WORLD',
            'IGLH.UK' : 'ISHARES GLOBAL GOVT BONDS',
            'AH.F' : 'BLOOMBERG COMMODITY INDEX',
            'REET.US' : 'ISHARES GLOBAL REIT',
            'DX.F' : 'DOLLAR INDEX',
            'BIL.US' : 'SPDR 1-3 MONTH T-BILL'

        }
    data = web.DataReader(symbol, 'stooq')
    nums = range(2, 252)
    total = []
    for x in nums:
        if data['Close'][1] > data['Close'][x]:
            score = 1
        else:
            score = -1
        total.append(score)
    total = (sum(total))
    result = [total, markets[symbol]]
    if result not in results:
        results.append(result)
        results.sort(key=lambda x: x[0], reverse=True)

    
def get_trend():
    global results

    threads = []
    num_threads = 6
    tickers = ['R2.F', 'IGLH.UK', 'AH.F', 'REET.US', 'DX.F', 'BIL.US']

    for i in range(num_threads):
        for x in tickers:
            thread = Thread(target=get_data, args=(x,))
            threads.append(thread)

    for thread in threads:
        thread.start()

    return results
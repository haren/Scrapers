import urllib
from datetime import date, timedelta
from time import strftime

class Importer:
    pass

class GpwImporter(Importer):
    """A simple importer for gpw.pl archite data"""

    def __init__(self):
        pass

    def import_data_from_gpw(self, date_from, date_to, path):
        for single_date in self.date_range(date_from, date_to):
            html_data = self.read_single_page(single_date.strftime('%Y-%m-%d'))
            self.save_html_data_to_file(html_data, path, single_date.strftime('%Y-%m-%d'))

    def read_single_page(self, date):
        url = 'http://www.gpw.pl/notowania_archiwalne_full?type=10&date=' + date
        page_data = urllib.urlopen(url)
        return page_data.read()

    def save_html_data_to_file(self, html_data, path, file_name):    
        file_path = path + '\\' + file_name + '.html'
        file = open(file_path, 'wb')
        file.writelines(html_data)
        file.close()
        print 'Succesfully saved for ', file_path

    def date_range(self, start_date, end_date):
        for n in range(int ((end_date - start_date).days)):
            yield start_date + timedelta(n)

class MoneyPlImporter(Importer):
    requestUrl = "http://www.money.pl/ajax/gielda/finanse/"

    def get_company_data(self, ticker, p, t, q):
        data = urllib.urlencode({"ticker":"KPX", "p":"Q","t": "t","o":"4"})
        result = urllib.urlopen("http://www.money.pl/ajax/gielda/finanse/",data).read()
        print result
        raw_input()


#perform scraping            
#files_path = 'C:\Users\lukas_000\Dropbox\TZ&LH&JR exchange\Gambler\GPW_notowania_archiwalne'
#start_date = date(2013,9,2)
#end_date = date(2013,10,22)

#importer = GpwImporter()
#importer.import_data_from_gpw(start_date, end_date, files_path)
importer = MoneyPlImporter()
importer.get_company_data("","","","")

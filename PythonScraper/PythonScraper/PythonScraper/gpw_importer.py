
class GpwImporter():
    """A simple importer for gpw.pl archite data"""

    def __init__(self):
        pass

    def import_data_from_gpw(self, url, date_from, date_to, path):
        for single_date in date_range(date_from, date_to):
            html_data = self.read_single_page(url, single_date.strftime('%Y-%m-%d'))
            self.save_html_data_to_file(html_data, 
                                        path, single_date.strftime('%Y-%m-%d'))

    def read_single_page(self, url, date):
        url = url + date
        page_data = urllib.urlopen(url)
        return page_data.read()

    def save_html_data_to_file(self, html_data, path, file_name):    
        file_path = path + '\\' + file_name + '.html'
        file = open(file_path, 'wb')
        file.writelines(html_data)
        file.close()
        print ('Succesfully saved for ', file_path)

    def date_range(self, start_date, end_date):
        for n in range(int ((end_date - start_date).days)):
            yield start_date + timedelta(n)
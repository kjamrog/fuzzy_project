from openpyxl import load_workbook
import os
import src.MFs as mfs


class Computer:
    def __init__(self, data):
        self.name = str(data['Manufacturer']) + ' ' + str(data['Series']) + ' ' + str(data['Model'])
        self.screen_diameter = float(data['Screen diameter'].replace(',', '.'))
        self.price = data['Price']
        self.cpu = data['CPU']
        self.cpu_rate = data['CPU rate']
        self.resolution = data['Resolution']
        self.ram = str(data['RAM [GB]']) + 'GB'
        self.ram_rate = data['RAM rate']
        self.drive = data['Drive type'] + ' ' + str(data['Drive [GB]']) + 'GB'
        self.drive_rate = data['Drive rate']
        self.graphics = data['Graphics']
        self.calculated_rate = 0

    def calc_rate(self, max_price):
        self.calculated_rate = mfs.calculate(max_price, self)


class ComputersList:
    def __init__(self):
        self.computers = []
        self.__load_computers_data()

    def __load_computers_data(self):
        path_to_data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/data.xlsx')
        wb = load_workbook(path_to_data_file, data_only=True)
        data = wb['Sheet1']
        col_range = data['C:AE']
        number_of_models = data['B21'].value
        for i in range(number_of_models - 1):
            index = i + 1
            if col_range[0][index].value == 1:
                comp = dict()
                for col in col_range:
                    comp[col[0].value] = col[index].value
                # print(comp)
                self.computers.append(Computer(comp))

    def __calculate_ratings(self, max_price):
        for c in self.computers:
            c.calc_rate(max_price)

    def get_sorted(self):
        return sorted(self.computers, key=lambda x: float(x.calculated_rate), reverse=True)

    def get_filter_lambda(self, screen_size):
        if screen_size==17:
            return lambda x: x.screen_diameter>=17
        elif screen_size==15:
            return lambda x: x.screen_diameter>=15 and x.screen_diameter <16
        else:
            return lambda x: x.screen_diameter<=14
        


    def get_best(self, max_price, amount, screen_size):
        self.__calculate_ratings(max_price)
        sorted_computers = self.get_sorted()
        filtered_computers = list(filter(self.get_filter_lambda(screen_size), sorted_computers))
        amount = min(amount, len(filtered_computers))
        return [filtered_computers[i] for i in range(amount)]

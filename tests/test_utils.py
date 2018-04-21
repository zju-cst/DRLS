from drls.utils import read_excel
from drls.utils import app_dir

if __name__ == "__main__":

    print(app_dir()+"/data/test.xls")
    dict = read_excel(app_dir()+"/data/test.xls")
    print(dict)
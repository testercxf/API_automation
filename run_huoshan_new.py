import  os
from time import sleep
import pytest



if __name__ == '__main__':
    pytest.main()
    sleep(1)
    os.system("allure generate  ./temp  -o  ./reports  --clean")

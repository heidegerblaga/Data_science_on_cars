import re


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    url = "https://www.otomoto.pl/osobowe?page=2&search%5Badvanced_search_expanded%5D=true"
    page = int(re.findall(r'\d+',str(re.findall(r'page=\d',url)))[0]) + 1
    print(page)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

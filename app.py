import tkinter as tk
from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.parse


class App:
    def __init__(self, master):
        self.frame = tk.Frame(master)

        self.title = tk.Label(self.frame, text='찾을 검색어를 입력해 주세요:')

        self.frame_input = tk.Frame(self.frame)

        self.input_keyword = tk.Entry(self.frame_input, width=25)
        self.input_keyword.bind('<Return>', self.search)

        self.button_submit = tk.Button(self.frame_input, width=10, text='검색')
        self.button_submit.bind('<Button-1>', self.search)

        self.frame_text_result = tk.Frame(self.frame)

        self.text_result_scrollbar_x = tk.Scrollbar(self.frame_text_result, orient='horizontal')
        self.text_result_scrollbar_y = tk.Scrollbar(self.frame_text_result, orient='vertical')
        self.text_result = tk.Listbox(
            self.frame_text_result,
            xscrollcommand=self.text_result_scrollbar_x.set,
            yscrollcommand=self.text_result_scrollbar_y.set
        )

        self.frame.pack(fill='both', expand=True)
        self.title.pack(ipady=10)

        self.frame_input.pack()
        self.input_keyword.pack(side='left', padx=3, pady=10, ipady=5)
        self.button_submit.pack(side='right', pady=10, ipady=2)

        self.frame_text_result.pack(fill='both', expand=True)
        self.text_result_scrollbar_x.pack(side='bottom', fill='x')
        self.text_result_scrollbar_y.pack(side='right', fill='y')
        self.text_result.pack(side='left', fill='both', expand=True)
        self.text_result_scrollbar_x.config(command=self.text_result.xview)
        self.text_result_scrollbar_y.config(command=self.text_result.yview)

        self.input_keyword.focus_set()

    def search(self, event):
        keyword = self.input_keyword.get()
        if keyword == '':
            self.text_result.delete(0, 29)
            self.text_result.insert('end', '입력한 내용이 없습니다. 다시 입력해 주세요.')
        else:
            self.text_result.delete(0, 29)

            url = "https://www.google.com/search?q=" \
                  + urllib.parse.quote_plus(keyword)

            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            html = urlopen(req)
            soup = BeautifulSoup(html, 'html.parser')

            with open('./example.html', 'w', encoding='utf-8') as f:
                f.write(str(soup))

            # ZINbbc xpd O9g5cc uUPGi
            # BNeawe vvjwJb AP7Wnd
            # BNeawe s3v9rd AP7Wnd

            txt = soup.find_all('div', {'class': 'ZINbbc xpd O9g5cc uUPGi'})[:-1]

            txt_title, txt_text = [], []
            for item in txt:
                title = item.find('div', {'class': 'BNeawe vvjwJb AP7Wnd'})
                text = item.find('div', {'class': 'BNeawe s3v9rd AP7Wnd'})
                if title is not None and text is not None:
                    txt_title.append(title.text)
                    txt_text.append(text.text)

            for i in range(len(txt_title)):
                self.text_result.insert('end', '[%d]' % (i+1))
                self.text_result.insert('end', '제목: %s' % txt_title[i])
                self.text_result.insert('end', '내용: %s' % txt_text[i])

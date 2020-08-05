import tkinter as tk
import tkinter.font
import threading

from crawl import get_images


class App:
    def __init__(self, master):
        # define components
        self.frame = tk.Frame(master)

        self.title = tk.Label(self.frame, text='찾을 검색어를 입력해 주세요.')
        font = tk.font.Font(family="Arial", size=20, weight="bold")
        self.title.configure(font=font)

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

        # pack components(order is important)
        self.frame.pack(fill='both', expand=True)
        self.title.pack(pady=20)

        self.frame_input.pack()
        self.input_keyword.pack(side='left', padx=3, pady=5, ipady=5)
        self.button_submit.pack(side='right', pady=5, ipady=3)

        self.frame_text_result.pack(fill='both', expand=True)
        self.text_result_scrollbar_x.pack(side='bottom', fill='x')
        self.text_result_scrollbar_y.pack(side='right', fill='y')
        self.text_result.pack(side='left', fill='both', expand=True)
        self.text_result_scrollbar_x.config(command=self.text_result.xview)
        self.text_result_scrollbar_y.config(command=self.text_result.yview)

        self.input_keyword.focus_set()

        self.keyword_count = 0

    def search(self, event):
        print(event)
        keyword = self.input_keyword.get()
        if keyword is "":
            return
        else:
            self.text_result.insert(self.keyword_count, keyword)
            self.keyword_count += 1

        # make thread and start
        self.refresh()
        thread = threading.Thread(target=get_images, args=(keyword,))
        thread.start()
        self.title['text'] = '입력된 검색어가 크롤링됩니다.'
        self.input_keyword.delete(0, 'end')

    def refresh(self):
        self.frame.update()
        self.frame.after(1000, self.refresh)

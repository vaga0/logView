import sys, os, requests
# from tkinterdnd2 import DND_FILES, TkinterDnD
import tkinter as tk
from tkinter import messagebox
from menu import create_menubar
from menu import open_file

class App:
	def __init__(self, root):
		self.version = {
			"ver": "1.0.0",
			"author": " Vaga Tsai",
			"createDate": "2023/10/17",
			"lastUpdate": "2023/10/17"
		}
		self.root = root
		self.root.title('Log View (｡◕‿◕｡)つ[v' + self.version['ver'] + ']')
		self.original_content = None
		self.entities = {
			'_frame': {},
			'_label': {},
			'_entry': {},
			'_btn': {}
		}

		# self.create_login_form()
		self.show_dashboard({'message':''})

	def show_version (self):
		# 創建一個新的 Toplevel 視窗
		version_win = tk.Toplevel()
		version_win.title("版本資訊")

		# 使視窗出現在主視窗的中心位置
		version_win.geometry("300x200+%d+%d" % (self.root.winfo_x() + 200, self.root.winfo_y() + 10))

		# 版本和作者資訊
		info_strings = [
			("版本:", self.version["ver"]),
			("作者:", self.version["author"]),
			("建立日期:", self.version["createDate"]),
			("最後更新:", self.version["lastUpdate"])
		]

		for info, value in info_strings:
			tk.Label(version_win, text=f"{info} {value}", font=("Microsoft YaHei", 10), padx=10).pack(pady=5)

		# version_win.geometry("300x200+%d+%d" % (self.root.winfo_x() + 50, self.root.winfo_y() + 50))


		# 關閉按鈕
		close_btn = tk.Button(version_win, text="關閉", command=version_win.destroy)
		close_btn.pack(pady=10)

	def search_keyword(self, mode):
		keyword = self.entities['_entry']['keyword_entry'].get()
		if not keyword:
			messagebox.showwarning("提示", "請輸入關鍵字")
			return
		
		if self.original_content is None:
			# 如果還未讀取原始內容，則讀取並保存
			print('revocer original_content')
			self.original_content = self.text_area.get("1.0", "end-1c")  # -1c用於刪除末尾換行符

		content_lines = self.filter_content(keyword, mode)
		if content_lines <= 1:
			messagebox.showinfo("Information", "沒有符合過濾條件的資料")
			self.entities['_btn']['button_qry2'].config(state=tk.DISABLED)
		else:
			self.entities['_btn']['button_qry2'].config(state=tk.NORMAL)

		self.entities['_btn']['button_clean'].config(state=tk.NORMAL)

	def reset_content(self):
		self.entities['_entry']['keyword_entry'].delete(0, tk.END)
		self.entities['_label']['filter_history_string_label'].config(text='')
		self.entities['_btn']['button_qry2'].config(state=tk.DISABLED)
		self.entities['_btn']['button_clean'].config(state=tk.DISABLED)
		if self.original_content:
			# 將文本區的內容重置為原始內容
			self.text_area.delete("1.0", "end")
			self.text_area.insert("1.0", self.original_content)

	def filter_content(self, keyword, mode):
		# 從原始內容中進行過濾
		if mode == 'more':
			current_content = self.text_area.get("1.0", tk.END)
			lines = current_content.split("\n")
			current_text = self.entities['_label']['filter_history_string_label'].cget("text")
			self.entities['_label']['filter_history_string_label'].config(text=current_text + ' > ' + keyword)
		else:
			lines = self.original_content.split("\n")
			self.entities['_label']['filter_history_string_label'].config(text=keyword)

		# filtered_lines = []
		# for line in lines:
		# 	if keyword.lower() in line.lower():
		# 		filtered_lines.append(line)
		# shortening: 這簡寫對新手很不直覺 第二個 line 是 lines 的每一筆資料，第一個 line 是一種預處理
		filtered_lines = [line for line in lines if keyword.lower() in line.lower()]

		# 清空當前 text_area 的內容
		self.text_area.delete("1.0", tk.END)

    # 將過濾後的內容插入 text_area
		current_line = 1
		for idx, line in enumerate(filtered_lines, start=1):
			self.text_area.insert(tk.END, f"{line}\n")

			# 標行色下 Tag 待會加顏色
			idx_length = len(str(idx))
			self.text_area.tag_add("lineCount", f"{current_line}.0", f"{current_line}.{idx_length}")
			
			# 如果行號是偶數
			if idx % 2 == 0:
				line_start = f"{current_line}.0"
				line_end = f"{current_line}.end"
				self.text_area.tag_add("even", line_start, line_end)

			# 如果這行包含 keyword，就將它的部分高亮
			start_position = line.lower().find(keyword.lower())
			while start_position != -1:
				start_idx = f"{current_line}.{start_position}"
				end_idx = f"{current_line}.{start_position + len(keyword)}"
				self.text_area.tag_add("highlight", start_idx, end_idx)
				
				# 查找下一個匹配的關鍵字（如果有的話）
				start_position = line.lower().find(keyword.lower(), start_position + len(keyword))

			self.text_area.insert(tk.END, "\n")
			current_line +=2

		# 配置 tags
		self.text_area.tag_config("even", background="#e3e3e3")
		self.text_area.tag_config("highlight", foreground="red")

		# 設定影響層級
		self.text_area.tag_raise("sel","even")
		self.text_area.tag_raise("sel", "lineCount")
		self.text_area.tag_raise("lineCount", "even")

		return current_line

	def create_login_form(self):
		self.clear_screen()
		self.resize(300, 200)

		login_frame = tk.Frame(self.root, padx=10, pady=10)
		login_frame.pack(pady=10)  # 使用 pack 並增加 pady 使其在主窗口中央

		self.host_label = tk.Label(login_frame, text="Host:")
		self.host_label.grid(row=0, column=0, padx=10, pady=10)

		self.host_entry = tk.Entry(login_frame)
		self.host_entry.grid(row=0, column=1, padx=10, pady=10)
		self.host_entry.insert(0, "127.0.0.1")

		self.username_label = tk.Label(login_frame, text="帳號:")
		self.username_label.grid(row=1, column=0, padx=10, pady=10)

		# StringVar for monitoring changes
		self.username_var = tk.StringVar()
		self.username_var.trace_add("write", self.on_username_change)

		self.username_entry = tk.Entry(login_frame, textvariable=self.username_var)
		self.username_entry.grid(row=1, column=1, padx=10, pady=10)
		self.username_entry.insert(0, "Guest")

		self.password_label = tk.Label(login_frame, text="密碼:")
		self.password_label.grid(row=2, column=0, padx=10, pady=10)

		self.password_entry = tk.Entry(login_frame, show='*')
		self.password_entry.grid(row=2, column=1, padx=10, pady=10)
		self.password_entry.insert(0, "guest")

		self.login_button = tk.Button(login_frame, text="登入", command=self.login)
		self.login_button.grid(row=3, column=0, columnspan=2, pady=10)

	def on_username_change(self, *args):
		print(f"Username changed to: {self.username_var.get()}")

	def login(self):
		if self.username_entry.get() and self.password_entry.get():
			response = self.verify_credentials_with_api(self.username_entry.get(), self.password_entry.get())
			if response is None:
				return
			
			if response and response.get('status') == 'success':
				self.show_dashboard(response)
			else:
				error_message = response.get('message', 'Invalid credentials. Please try again.')
				messagebox.showerror("Error", error_message)
		else:
			messagebox.showerror("Error", "Invalid credentials. Please try again.")

	def show_dashboard(self, response):
		self.clear_screen()

		self.resize(700, 400)

		create_menubar(self.root, self)

		# Upper Frame for buttons
		upper_frame = self.entities['_frame']['_upper_frame'] = tk.Frame(self.root, bd=2, relief='ridge', padx=10, pady=10)
		upper_frame.pack(fill=tk.X, padx=10, pady=5)
		upper_frame_L1 = self.entities['_frame']['upper_frame_L1'] = tk.Frame(upper_frame)
		upper_frame_L1.pack(fill=tk.X, padx=5, )
		upper_frame_L2 = self.entities['_frame']['upper_frame_L2'] = tk.Frame(upper_frame)
		upper_frame_L2.pack(fill=tk.X, padx=5, )
		upper_frame_L3 = self.entities['_frame']['upper_frame_L3'] = tk.Frame(upper_frame)
		upper_frame_L3.pack(fill=tk.X, padx=5, )

		self.source_label = self.entities['_label']['source_label'] = tk.Label(upper_frame_L1, text="來源:")
		self.source_label.pack(side=tk.LEFT)

		source_path_label = self.entities['_label']['source_path_label'] = tk.Label(upper_frame_L1, text="...")
		source_path_label.pack(side=tk.LEFT)

		keyword_label = self.entities['_label']['keyword_label'] = tk.Label(upper_frame_L2, text="關鍵字:")
		keyword_label.pack(side=tk.LEFT)

		keyword_entry = self.entities['_entry']['keyword_entry'] = tk.Entry(upper_frame_L2)
		keyword_entry.pack(side=tk.LEFT)

		button_qry1 = self.entities['_btn']['button_qry1'] = tk.Button(upper_frame_L2, text="重新查詢", command=lambda: self.search_keyword('reset'))
		button_qry1.pack(side=tk.LEFT, padx=5)

		button_qry2 = self.entities['_btn']['button_qry2'] = tk.Button(upper_frame_L2, text="繼續查詢", command=lambda: self.search_keyword('more'))
		button_qry2.pack(side=tk.LEFT, padx=5)
		button_qry2.config(state=tk.DISABLED)

		button_clean = self.entities['_btn']['button_clean'] = tk.Button(upper_frame_L2, text="重置", command=self.reset_content)
		button_clean.pack(side=tk.LEFT, padx=5)
		button_clean.config(state=tk.DISABLED)

		self.filter_history_label = self.entities['_label']['filter_history_label'] = tk.Label(upper_frame_L3, text="Filter History:")
		self.filter_history_label.pack(side=tk.LEFT)

		self.filter_history_string_label = self.entities['_label']['filter_history_string_label'] = tk.Label(upper_frame_L3, text="")
		self.filter_history_string_label.pack(side=tk.LEFT)

		# Lower Frame for Text Widget
		main_frame = self.entities['_label']['main_frame'] = tk.Frame(self.root, bd=2, relief='ridge', padx=10, pady=10)
		main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

		# 創建滾動條
		scrollbar = tk.Scrollbar(main_frame)
		scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

		self.text_area = self.entities['_entry']['text_area'] = tk.Text(main_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
		self.text_area.pack(fill=tk.BOTH, expand=True)
		
		# 拖放功能：
		# self.text_area.drop_target_register(DND_FILES)
		# self.text_area.dnd_bind('<<Drop>>', self.on_drop)

		# self.text_area.drop_target_register('<<Drop>>', 'DND_Files')
		# self.text_area.dnd_bind('<<Drop>>', self.on_drop)


		# 將滾動條與文本框連接
		scrollbar.config(command=self.text_area.yview)

		# Sample text
		self.text_area.insert(tk.END, "請選擇資料來源: \n\n")
		self.text_area.insert(tk.END, "1. 開啟檔案\n\n")
		self.text_area.insert(tk.END, "2. 複製內容貼上\n\n")
		self.text_area.insert(tk.END, "3. 拖曳檔案至此(.exe檔不支援)\n\n")
		self.text_area.insert(tk.END, "\n" + response.get('message'))

	def clear_screen(self):
		for widget in self.root.winfo_children():
			widget.destroy()

	def verify_credentials_with_api(self, username, password):
		api_url = "http://127.0.0.1/hrm/api/v1/login/pylogin.php"
		payload = {
			"username": username,
			"password": password
		}

		try:
			response = requests.post(api_url, data=payload)
			return response.json()
		except requests.RequestException as e:
			messagebox.showerror("Error", "Unable to connect to the server. Please try again later.")
			return None

	def on_entry_change(self, *args):
		print("Entry changed to:", self.entry_var.get())

	def resize(self, width, height):
		screen_width = root.winfo_screenwidth()
		screen_height = root.winfo_screenheight()
		window_width = width
		window_height = height
		x_position = (screen_width / 2) - (window_width / 2)
		y_position = (screen_height / 2) - (window_height / 2)
		root.geometry(f"{window_width}x{window_height}+{int(x_position)}+{int(y_position)}")

	def on_drop(self, event):
		file_path = event.data.strip()  # 擷取拖放文件的路徑
		open_file(self, tk, file_path)  # 使用您已有的 open_file 方法打開它

if __name__ == "__main__":
	def is_running_as_bundled_executable():
			return getattr(sys, '_MEIPASS', None) is not None

	root = tk.Tk()
	# root = TkinterDnD.Tk()

	script_dir = os.path.dirname(os.path.abspath(__file__))
	# root.iconbitmap(script_dir + os.sep + 'logo-32.ico')
	root.iconbitmap('D:\py_project\sample_1\logo-32.ico')

	app = App(root)
	root.mainloop()

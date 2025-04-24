# menu.py

from tkinter import filedialog

def create_menubar(root, app_instance):
	import tkinter as tk

	# menu_font = ('Arial', 10)
	menu_font = ('Microsoft YaHei', 10)

	menubar = tk.Menu(root)
	root.config(menu=menubar)

	file_menu = tk.Menu(menubar, tearoff = 0, font=menu_font)
	menubar.add_cascade(label="檔案", menu=file_menu)
	file_menu.add_command(label="讀取", command=lambda: open_file(app_instance, tk, None))
	file_menu.add_separator()
	# file_menu.add_command(label="登出", command=app_instance.create_login_form)
	file_menu.add_command(label="離開", command=root.quit)

	file_menu2 = tk.Menu(menubar, tearoff = 0, font=menu_font)
	menubar.add_cascade(label="關於", menu=file_menu2)
	file_menu2.add_command(label="版本", command=app_instance.show_version)

def open_file(app_instance, tk, file_path=None):
	if not file_path:  # 如果沒有提供 file_path，那麼使用 filedialog 問用戶
		file_path = filedialog.askopenfilename()
	if not file_path:
		return
	
	app_instance.entities['_label']['source_path_label'].config(text=file_path)
	app_instance.entities['_entry']['keyword_entry'].delete(0, tk.END)
	app_instance.entities['_label']['filter_history_string_label'].config(text='')
	app_instance.entities['_btn']['button_qry2'].config(state=tk.DISABLED)

	app_instance.text_area.delete(1.0, tk.END)
	with open(file_path, 'r', encoding='utf-8') as file:
		file_content = file.readlines()
	# app_instance.text_area.insert(tk.END, file_content)

	current_line = 1
	for idx, line in enumerate(file_content, start=1):

		# 先插入一行資料
		app_instance.text_area.insert(tk.END, f"{idx} {line}")

		# 標行色下 Tag 待會加顏色
		idx_length = len(str(idx))
		app_instance.text_area.tag_add("lineCount", f"{current_line}.0", f"{current_line}.{idx_length}")
		
		# 如果本筆是偶數資料，將剛剛插入的整行資料進行 tag 標註 "even"
		if idx % 2 == 0:
			line_start = f"{current_line}.0"
			line_end = f"{current_line}.end"
			app_instance.text_area.tag_add("even", line_start, line_end)

		# 加一行換行
		app_instance.text_area.insert(tk.END, "\n")
		current_line += 2

	app_instance.text_area.tag_config("lineCount", foreground="#00a67d")
	app_instance.text_area.tag_config("even", background="#e3e3e3")

	# 避免滑鼠圈選的顏色不見
	app_instance.text_area.tag_config("sel", background="#005eda")

	# 設定影響層級
	app_instance.text_area.tag_raise("sel","even")
	app_instance.text_area.tag_raise("sel", "lineCount")
	app_instance.text_area.tag_raise("lineCount", "even")

	app_instance.original_content = app_instance.text_area.get("1.0", "end-1c")  # -1c用於刪除末尾換行符
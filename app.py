import os
import sys
import json
import tkinter as tk
from tkinter import ttk, messagebox
from ticket import render_ticket
from PIL import Image, ImageTk

def resource_path(relative_path):
    """获取打包后的资源路径"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# ----------------------------
# 加载用户数据
# ----------------------------
def load_user_data(style):
    user_json_path = resource_path(f"user_{style}.json")
    if os.path.exists(user_json_path):
        with open(user_json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {}


# ----------------------------
# 保存用户数据
# ----------------------------
def save_user_data(data, style):
    user_json_path = resource_path(f"user_{style}.json")
    with open(user_json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# ----------------------------
# 更新字段
# ----------------------------
def update_fields(style):
    global field_widgets, user_data, field_frame
    # 清除之前的字段
    for widget in field_frame.winfo_children():
        widget.destroy()

    # 加载用户数据
    user_data = load_user_data(style)
    field_widgets = {}

    # 两列布局
    keys = list(user_data.keys())
    row = 0
    for i, key in enumerate(keys):
        col = i % 2
        r = row if col == 0 else row
        lbl = ttk.Label(field_frame, text=key+":", anchor="e", width=20)
        lbl.grid(row=r, column=col*2, padx=5, pady=5, sticky="e")
        entry = ttk.Entry(field_frame, width=30)
        entry.insert(0, str(user_data[key]))
        entry.grid(row=r, column=col*2+1, padx=5, pady=5, sticky="w")
        field_widgets[key] = entry
        if col == 1:
            row += 1


# ----------------------------
# 生成车票
# ----------------------------
def generate_ticket():
    user_data = {key: entry.get() for key, entry in field_widgets.items()}
    selected_style = style_var.get()
    save_user_data(user_data, selected_style)

    try:
        template_json_path = os.path.join(template_dir, f"ticket_template_{selected_style}.json")
        result_img = render_ticket(user_data, template_json_path, template_dir)
        output_path = os.path.join(os.getcwd(), "ticket_result.png")
        result_img.save(output_path)
        messagebox.showinfo("成功", f"✅ 车票已生成：{output_path}")
    except Exception as e:
        messagebox.showerror("错误", f"生成车票失败：{e}")


# ----------------------------
# 主窗口
# ----------------------------
def start_main_window():
    global field_widgets, style_var, template_dir, field_frame

    template_dir = resource_path("templates")

    root = tk.Tk()
    root.title("CRTicketMaker")
    root.geometry("700x700")
    root.configure(bg="#f0f0f0")

    # 顶部选择栏
    top_frame = tk.Frame(root, bg="#f0f0f0")
    top_frame.pack(fill="x", padx=10, pady=10)

    tk.Label(top_frame, text="选择车票样式:", bg="#f0f0f0", font=("Segoe UI", 10, "bold")).pack(side="left")
    style_var = tk.StringVar()
    style_combobox = ttk.Combobox(top_frame, textvariable=style_var, values=["red15", "red05_shortride"], width=20)
    style_combobox.pack(side="left", padx=10)
    style_combobox.current(0)

    # 滚动区域
    canvas_frame = tk.Frame(root)
    canvas_frame.pack(fill="both", expand=True, padx=10, pady=(0,10))

    canvas = tk.Canvas(canvas_frame, bg="#f0f0f0")
    scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#ffffff", bd=1, relief="solid")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # 字段区域
    field_frame = tk.Frame(scrollable_frame, bg="#ffffff")
    field_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # 初始化字段
    update_fields(style_var.get())

    # 当选择样式变化时更新字段
    style_combobox.bind("<<ComboboxSelected>>", lambda e: update_fields(style_var.get()))

    # 底部生成按钮
    btn_frame = tk.Frame(root, bg="#f0f0f0")
    btn_frame.pack(fill="x", pady=10)
    generate_btn = tk.Button(btn_frame, text="生成车票", bg="#4CAF50", fg="white", font=("Segoe UI", 12, "bold"),
                             activebackground="#45a049", padx=20, pady=8, command=generate_ticket)
    generate_btn.pack(side="top", pady=5)

    root.mainloop()


if __name__ == "__main__":
    start_main_window()

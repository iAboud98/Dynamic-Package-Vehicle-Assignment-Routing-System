import customtkinter as ctk
from tkinter import filedialog
import json

# Theme Setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("SmartDrop - Intelligent Package Routing")
app.geometry("1200x750")

default_color = "Blue"
default_theme = "Dark"
current_color = default_color
current_theme = default_theme

# Color Themes
theme_colors = {
    "Blue": {
        "Dark":  {"button": "#3282B8", "hover": "#236192", "title": "#87CEFA", "text": "white", "sub": "white", "desc": "#AAAAAA", "dropdown": "#2B2B2B"},
        "Light": {"button": "#4682B4", "hover": "#3A5F8A", "title": "#005A9E", "text": "white", "sub": "black", "desc": "#555555", "dropdown": "#EAEAEA"},
    },
    "Green": {
        "Dark":  {"button": "#4CAF50", "hover": "#3C8D40", "title": "#A5D6A7", "text": "white", "sub": "white", "desc": "#AAAAAA", "dropdown": "#2B2B2B"},
        "Light": {"button": "#81C784", "hover": "#66BB6A", "title": "#2E7D32", "text": "white", "sub": "black", "desc": "#555555", "dropdown": "#EAEAEA"},
    },
    "Purple": {
        "Dark":  {"button": "#7D3C98", "hover": "#663399", "title": "#D7BDE2", "text": "white", "sub": "white", "desc": "#AAAAAA", "dropdown": "#2B2B2B"},
        "Light": {"button": "#BA68C8", "hover": "#9C27B0", "title": "#6A1B9A", "text": "white", "sub": "black", "desc": "#555555", "dropdown": "#EAEAEA"},
    }
}

# Apply theme colors
def apply_colors():
    colors = theme_colors[current_color][current_theme]

    # main app buttons
    for btn in [add_package_btn, add_vehicle_btn, solve_btn, settings_btn]:
        btn.configure(fg_color=colors["button"], hover_color=colors["hover"])

    # titles and texts
    algo_label.configure(text_color=colors["title"])
    main_title.configure(text_color=colors["title"])
    package_label.configure(text_color=colors["title"])
    vehicle_label.configure(text_color=colors["title"])
    subtitle.configure(text_color=colors["sub"])
    description.configure(text_color=colors["desc"])

    # dropdown background color
    settings_dropdown.configure(fg_color=colors["dropdown"])

    # menus inside dropdown
    theme_menu.configure(
        fg_color=colors["button"],
        text_color=colors["text"],
        button_color=colors["button"],
        button_hover_color=colors["hover"]
    )
    color_menu.configure(
        fg_color=colors["button"],
        text_color=colors["text"],
        button_color=colors["button"],
        button_hover_color=colors["hover"]
    )

    # buttons inside dropdown (except Reset and Exit)
    for child in settings_dropdown.winfo_children():
        if isinstance(child, ctk.CTkButton):
            if "Reset" in child.cget("text") or "Exit" in child.cget("text"):
                child.configure(fg_color="red", hover_color="darkred", text_color="white")
            else:
                child.configure(fg_color=colors["button"], hover_color=colors["hover"], text_color=colors["text"])


# Title
title_frame = ctk.CTkFrame(app, fg_color="transparent")
title_frame.pack(pady=(25, 10), fill="x")
main_title = ctk.CTkLabel(title_frame, text="SmartDrop", font=("Courier", 38, "bold"))
main_title.pack()
subtitle = ctk.CTkLabel(title_frame, text="AI-Powered Package Routing System", font=("Courier", 20))
subtitle.pack()
description = ctk.CTkLabel(title_frame, text="Optimize assignments with Genetic & Simulated Annealing Algorithms", font=("Courier", 14))
description.pack(pady=5)

# Algorithm
algo_frame = ctk.CTkFrame(app, width=1400, height=70)
algo_frame.pack(pady=10, padx=20, anchor="w")
algo_frame.pack_propagate(False)
algo_label = ctk.CTkLabel(algo_frame, text="Choose your Algorithm:", font=("Courier", 20, "bold"))
algo_label.pack(side="left", padx=(10, 20))
algo_var = ctk.IntVar()
ctk.CTkRadioButton(algo_frame, text="Genetic Algorithm", variable=algo_var, value=1).pack(side="left", padx=10)
ctk.CTkRadioButton(algo_frame, text="Simulated Annealing", variable=algo_var, value=2).pack(side="left", padx=10)

# Dropdown Frame
settings_dropdown = ctk.CTkToplevel(app)
settings_dropdown.withdraw()
settings_dropdown.overrideredirect(True)
settings_dropdown.lift(app)

def change_theme(choice):
    global current_theme
    current_theme = choice
    ctk.set_appearance_mode(choice)
    apply_colors()

def change_color(color_name):
    global current_color
    current_color = color_name
    apply_colors()

def reset_all():
    global current_color, current_theme
    current_color = default_color
    current_theme = default_theme
    color_menu.set(default_color)
    theme_menu.set(default_theme)
    change_theme(default_theme)
    apply_colors()
    for widget in package_scroll.winfo_children(): widget.destroy()
    for widget in vehicle_scroll.winfo_children(): widget.destroy()
    add_package_bar()
    add_vehicle_bar()

def save_data():
    data = {"packages": [], "vehicles": []}
    for row in package_scroll.winfo_children():
        entries = row.winfo_children()[1:-1]
        data["packages"].append([e.get() for e in entries])
    for row in vehicle_scroll.winfo_children():
        data["vehicles"].append([row.winfo_children()[1].get()])
    file_path = filedialog.asksaveasfilename(defaultextension=".json")
    if file_path:
        with open(file_path, "w") as f:
            json.dump(data, f)


def load_data():
    for widget in package_scroll.winfo_children(): widget.destroy()
    for widget in vehicle_scroll.winfo_children(): widget.destroy()
    file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
    if file_path:
        with open(file_path, "r") as f:
            data = json.load(f)
        for row in data["packages"]: add_package_bar(*row)
        for row in data["vehicles"]: add_vehicle_bar(*row)


def toggle_settings_dropdown():
    if settings_dropdown.winfo_viewable():
        settings_dropdown.withdraw()
    else:
        app.update_idletasks()
        x = settings_btn.winfo_rootx() - 30
        y = settings_btn.winfo_rooty() + settings_btn.winfo_height() + 5
        settings_dropdown.geometry(f"+{x}+{y}")
        settings_dropdown.deiconify()
        settings_dropdown.focus_force()

theme_menu = ctk.CTkOptionMenu(settings_dropdown, values=["Light", "Dark"], command=change_theme)
theme_menu.set(default_theme)
theme_menu.pack(pady=(15, 5))

color_menu = ctk.CTkOptionMenu(settings_dropdown, values=["Blue", "Green", "Purple"], command=change_color)
color_menu.set(default_color)
color_menu.pack(pady=5)

ctk.CTkButton(settings_dropdown, text="📤 Save", command=save_data).pack(pady=5)
ctk.CTkButton(settings_dropdown, text="📥 Load", command=load_data).pack(pady=5)
ctk.CTkButton(settings_dropdown, text="🧹 Reset All Settings", command=reset_all, fg_color="red", hover_color="darkred").pack(pady=5)
ctk.CTkButton(settings_dropdown, text="❌ Exit", command=app.destroy,
              fg_color="red", hover_color="darkred").pack(pady=5)
settings_dropdown.bind("<FocusOut>", lambda e: settings_dropdown.withdraw())

settings_btn = ctk.CTkButton(algo_frame, text="⚙️ Settings", width=100, command=toggle_settings_dropdown)
settings_btn.place(relx=1.0, rely=0.24, x=-10, y=5, anchor="ne")

# Layout
main_frame = ctk.CTkFrame(app)
main_frame.pack(padx=20, pady=20, fill="both", expand=True)

package_frame = ctk.CTkFrame(main_frame, width=600)
package_frame.pack(side="left", fill="both", expand=True, padx=10)
package_label = ctk.CTkLabel(package_frame, text="📦 Package Table", font=("Courier", 20, "bold"))
package_label.pack(pady=10)
package_scroll = ctk.CTkScrollableFrame(package_frame, height=350)
package_scroll.pack(pady=10, padx=10, fill="both", expand=True)

vehicle_frame = ctk.CTkFrame(main_frame, width=400)
vehicle_frame.pack(side="right", fill="both", expand=True, padx=10)
vehicle_label = ctk.CTkLabel(vehicle_frame, text="🚚 Vehicle Table", font=("Courier", 20, "bold"))
vehicle_label.pack(pady=10)
vehicle_scroll = ctk.CTkScrollableFrame(vehicle_frame, height=350)
vehicle_scroll.pack(pady=10, padx=10, fill="both", expand=True)

solve_btn = ctk.CTkButton(app, text="🚀 Solve", font=("Courier", 18))
solve_btn.pack(pady=10)

def update_package_ids():
    for i, row in enumerate(package_scroll.winfo_children(), start=1):
        row.winfo_children()[0].configure(text=str(i))
        
def update_vehicle_ids():
    for i, row in enumerate(vehicle_scroll.winfo_children(), start=1):
        row.winfo_children()[0].configure(text=str(i))
        
def update_add_buttons_state():
    # Only enable if every package row is confirmed
    all_pk = all(getattr(r, "confirmed", False) for r in package_scroll.winfo_children())
    add_package_btn.configure(state="normal" if all_pk else "disabled")
    # Only enable if every vehicle row is confirmed
    all_vh = all(getattr(r, "confirmed", False) for r in vehicle_scroll.winfo_children())
    add_vehicle_btn.configure(state="normal" if all_vh else "disabled")

def add_package_bar(x="", y="", w="", p=""):
    row = ctk.CTkFrame(package_scroll)
    row.pack(pady=5, padx=5)
    row.confirmed = False

    # 1) ID cell
    id_lbl = ctk.CTkLabel(row, text="", width=30)
    id_lbl.pack(side="left", padx=5)

    # 2) Entries for X, Y, Weight, Priority
    entries = {}
    for key, val, width in zip(
        ("X", "Y", "Weight", "Priority"),
        (x, y, w, p),
        (50, 50, 80, 60)
    ):
        e = ctk.CTkEntry(row, placeholder_text=key, width=width)
        if val:
            e.insert(0, val)
        e.pack(side="left", padx=5)
        entries[key] = e

    # 3) Inline error label
    err_lbl = ctk.CTkLabel(row, text="", text_color="red", font=("Courier", 12))
    err_lbl.pack(side="left", padx=(5, 10))

    # 4) Callbacks
    def on_delete():
        row.destroy()
        update_package_ids()
        update_add_buttons_state()

    def on_confirm():
        vals = {k: e.get().strip() for k, e in entries.items()}

        # require all fields filled
        if any(v == "" for v in vals.values()):
            err_lbl.configure(text="⚠ fill all fields")
            return

        # parse X, Y, Weight
        try:
            xv = float(vals["X"])
            yv = float(vals["Y"])
            wv = float(vals["Weight"])
        except ValueError:
            err_lbl.configure(text="⚠ X,Y,Weight must be numeric")
            return

        # parse Priority
        try:
            pv = int(vals["Priority"])
        except ValueError:
            err_lbl.configure(text="Priority must be integer")
            return

        # range checks
        if not (0 <= xv <= 100 and 0 <= yv <= 100):
            err_lbl.configure(text="⚠ X,Y ∈ [0,100]")
            return
        if wv <= 0:
            err_lbl.configure(text="Weight must be > 0")
            return
        if not (0 <= pv <= 5):
            err_lbl.configure(text="⚠ Priority ∈ [0,5]")
            return

        # valid → lock entries & swap buttons
        row.confirmed = True
        for e in entries.values():
            e.configure(state="readonly")
        err_lbl.configure(text="")
        confirm_btn.pack_forget()
        edit_btn.pack(side="left", padx=2)
        update_add_buttons_state()

    def on_edit():
        for e in entries.values():
            e.configure(state="normal")
        edit_btn.pack_forget()
        confirm_btn.pack(side="left", padx=2)
        update_add_buttons_state()

    # 5) Buttons: delete, confirm, edit
    delete_btn = ctk.CTkButton(
        row, text="❌", width=30,
        fg_color="red", hover_color="#cc0000",
        command=on_delete
    )
    confirm_btn = ctk.CTkButton(
        row, text="✅", width=30,
        fg_color="#28a745", hover_color="#218838", text_color="white",
        command=on_confirm
    )
    edit_btn = ctk.CTkButton(
        row, text="✏️", width=30,
        fg_color="#ffc107", hover_color="#e0a800", text_color="black",
        command=on_edit
    )

    delete_btn.pack(side="left", padx=2)
    confirm_btn.pack(side="left", padx=2)
    # edit_btn will be shown after successful confirm

    update_package_ids()
    update_add_buttons_state()

def add_vehicle_bar(cap=""):
    row = ctk.CTkFrame(vehicle_scroll)
    row.pack(pady=5, padx=5)
    row.confirmed = False

    # 1) ID cell
    id_lbl = ctk.CTkLabel(row, text="", width=30)
    id_lbl.pack(side="left", padx=5)

    # 2) Capacity entry
    cap_entry = ctk.CTkEntry(row, placeholder_text="Capacity", width=100)
    if cap:
        cap_entry.insert(0, cap)
    cap_entry.pack(side="left", padx=5)

    # 3) Inline error label
    err_lbl = ctk.CTkLabel(row, text="", text_color="red", font=("Courier", 12))
    err_lbl.pack(side="left", padx=(5, 10))

    # 4) Callbacks
    def on_delete():
        row.destroy()
        update_vehicle_ids()
        update_add_buttons_state()

    def on_confirm():
        val = cap_entry.get().strip()
        if not val:
            err_lbl.configure(text="⚠ fill capacity")
            return
        # parse as float
        try:
            cv = float(val)
        except ValueError:
            err_lbl.configure(text="Capacity must be numeric")
            return
        if cv <= 0:
            err_lbl.configure(text="Capacity must be > 0")
            return

        # valid → lock entry & swap buttons
        row.confirmed = True
        cap_entry.configure(state="readonly")
        err_lbl.configure(text="")
        confirm_btn.pack_forget()
        edit_btn.pack(side="left", padx=2)
        update_add_buttons_state()


    def on_edit():
        cap_entry.configure(state="normal")
        edit_btn.pack_forget()
        confirm_btn.pack(side="left", padx=2)
        update_add_buttons_state()

    # 5) Buttons: delete, confirm, edit
    delete_btn = ctk.CTkButton(
        row, text="❌", width=30,
        fg_color="red", hover_color="#cc0000",
        command=on_delete
    )
    confirm_btn = ctk.CTkButton(
        row, text="✅", width=30,
        fg_color="#28a745", hover_color="#218838", text_color="white",
        command=on_confirm
    )
    edit_btn = ctk.CTkButton(
        row, text="✏️", width=30,
        fg_color="#ffc107", hover_color="#e0a800", text_color="black",
        command=on_edit
    )

    delete_btn.pack(side="left", padx=2)
    confirm_btn.pack(side="left", padx=2)
    # edit_btn will be shown after successful confirm

    update_vehicle_ids()
    update_add_buttons_state()

# Buttons
add_package_btn = ctk.CTkButton(package_frame, text="➕ Add Package", command=add_package_bar)
add_package_btn.pack(pady=10)

add_vehicle_btn = ctk.CTkButton(vehicle_frame, text="➕ Add Vehicle", command=add_vehicle_bar)
add_vehicle_btn.pack(pady=10)

add_package_bar()
add_vehicle_bar()
update_add_buttons_state()
apply_colors()

def defocus_entries(event):
    widget = event.widget

    # 1) if I clicked *anywhere* inside a CTkEntry, do nothing
    temp = widget
    while temp:
        if isinstance(temp, ctk.CTkEntry):
            return
        temp = temp.master

    # 2) if I clicked on (or inside) the Settings button, do nothing
    temp = widget
    while temp:
        if temp is settings_btn:
            return
        temp = temp.master

    # otherwise, it really is “outside” – pull focus away
    app.focus_set()

# make sure we add this *after* settings_btn & all entries exist, but *before* mainloop
app.bind_all("<Button-1>", defocus_entries, add="+")


app.mainloop()
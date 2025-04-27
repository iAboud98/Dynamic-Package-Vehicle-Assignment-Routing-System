#Aboud Fialah           ID: 1220216         Section: 2
#Aws Hammad             ID: 1221697         Section: 3   

import customtkinter as ctk
from tkinter import filedialog

def launch_gui():       #main function

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

    def apply_colors():
        colors = theme_colors[current_color][current_theme]
        for btn in [add_package_btn, add_vehicle_btn, solve_btn, settings_btn]:
            btn.configure(fg_color=colors["button"], hover_color=colors["hover"])
        algo_label.configure(text_color=colors["title"])
        main_title.configure(text_color=colors["title"])
        package_label.configure(text_color=colors["title"])
        vehicle_label.configure(text_color=colors["title"])
        subtitle.configure(text_color=colors["sub"])
        description.configure(text_color=colors["desc"])
        settings_dropdown.configure(fg_color=colors["dropdown"])
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

    # Settings dropdown
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
        
    def get_locked_color():
        # a subtle grey for dark vs. light theme
        if ctk.get_appearance_mode() == "Dark":
            return "#2B2B2B"
        else:
            return "#EAEAEA"

    def reset_all():
        global current_color, current_theme
        current_color = default_color
        current_theme = default_theme
        color_menu.set(default_color)
        theme_menu.set(default_theme)
        change_theme(default_theme)
        apply_colors()
        for w in package_scroll.winfo_children(): w.destroy()
        for w in vehicle_scroll.winfo_children(): w.destroy()
        add_package_bar()
        add_vehicle_bar()

    def save_data_txt():
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files","*.txt")])
        if not path:
            return
        with open(path, "w") as f:
            # write packages
            f.write("# packages: X Y Weight Priority\n")
            for row in package_scroll.winfo_children():
                # children: [ID_label, X_entry, Y_entry, W_entry, P_entry, err_lbl, …]
                entries = row.winfo_children()[1:5]
                vals = [e.get().strip() for e in entries]
                f.write(" ".join(vals) + "\n")

            f.write("\n# vehicles: Capacity\n")
            for row in vehicle_scroll.winfo_children():
                cap = row.winfo_children()[1].get().strip()
                f.write(cap + "\n")

    def load_data_txt():
        # clear
        for w in package_scroll.winfo_children(): w.destroy()
        for w in vehicle_scroll.winfo_children(): w.destroy()

        path = filedialog.askopenfilename(filetypes=[("Text Files","*.txt")])
        if not path:
            return

        with open(path, "r") as f:
            lines = [L.strip() for L in f if L.strip() and not L.startswith("#")]

        # find blank‐line separator
        try:
            sep = lines.index("")  # blank line
            pkg_lines = lines[:sep]
            vh_lines  = lines[sep+1:]
        except ValueError:
            # if no blank, assume half packages or guess by count?
            # here: everything until a non‐4‐column line is packages
            pkg_lines, vh_lines = [], []
            for L in lines:
                if len(L.split()) == 4:
                    pkg_lines.append(L)
                else:
                    vh_lines.append(L)

        # rebuild
        for L in pkg_lines:
            x,y,w,p = L.split()
            add_package_bar(x, y, w, p)
        for L in vh_lines:
            add_vehicle_bar(L)

        update_package_ids()
        update_vehicle_ids()
        update_add_buttons_state()
        apply_colors()



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

    theme_menu = ctk.CTkOptionMenu(settings_dropdown, values=["Light","Dark"], command=change_theme)
    theme_menu.set(default_theme)
    theme_menu.pack(pady=(15,5))
    color_menu = ctk.CTkOptionMenu(settings_dropdown, values=["Blue","Green","Purple"], command=change_color)
    color_menu.set(default_color)
    color_menu.pack(pady=5)
    ctk.CTkButton(settings_dropdown, text="📤 Save File", command=save_data_txt).pack(pady=5)
    ctk.CTkButton(settings_dropdown, text="📥 Load File", command=load_data_txt).pack(pady=5)
    ctk.CTkButton(settings_dropdown, text="🧹 Reset All Settings", command=reset_all, fg_color="red", hover_color="darkred").pack(pady=5)
    ctk.CTkButton(settings_dropdown, text="❌ Exit", command=app.destroy, fg_color="red", hover_color="darkred").pack(pady=5)
    settings_dropdown.bind("<FocusOut>", lambda e: settings_dropdown.withdraw())

    settings_btn = ctk.CTkButton(algo_frame, text="⚙️ Settings", width=100, command=toggle_settings_dropdown)
    settings_btn.place(relx=1.0, rely=0.24, x=-10, y=5, anchor="ne")

    # Main layout
    main_frame = ctk.CTkFrame(app)
    main_frame.pack(padx=20, pady=20, fill="both", expand=True)

    package_frame = ctk.CTkFrame(main_frame, width=600)
    package_frame.pack(side="left", fill="both", expand=True, padx=10)
    package_label = ctk.CTkLabel(package_frame, text="📦 Package Table", font=("Courier",20,"bold"))
    package_label.pack(pady=10)
    package_scroll = ctk.CTkScrollableFrame(package_frame, height=350)
    package_scroll.pack(pady=10, padx=10, fill="both", expand=True)

    vehicle_frame = ctk.CTkFrame(main_frame, width=400)
    vehicle_frame.pack(side="right", fill="both", expand=True, padx=10)
    vehicle_label = ctk.CTkLabel(vehicle_frame, text="🚚 Vehicle Table", font=("Courier",20,"bold"))
    vehicle_label.pack(pady=10)
    vehicle_scroll = ctk.CTkScrollableFrame(vehicle_frame, height=350)
    vehicle_scroll.pack(pady=10, padx=10, fill="both", expand=True)

    solve_btn = ctk.CTkButton(app, text="🚀 Solve", font=("Courier",18))
    solve_btn.pack(pady=10)

    def update_package_ids():
        for i, row in enumerate(package_scroll.winfo_children(), start=1):
            row.winfo_children()[0].configure(text=str(i))
            
    def update_vehicle_ids():
        for i, row in enumerate(vehicle_scroll.winfo_children(), start=1):
            row.winfo_children()[0].configure(text=str(i))
            
    def update_add_buttons_state():
        pk_rows = package_scroll.winfo_children()
        vh_rows = vehicle_scroll.winfo_children()

        # **Is the package table “ready” to add another?**
        pkg_all_confirmed = bool(pk_rows) and all(r.confirmed for r in pk_rows)
        pkg_editing       = any(getattr(r, "editing", False) for r in pk_rows)
        pkg_ready         = pkg_all_confirmed and not pkg_editing

        # **Is the vehicle table “ready” to add another?**
        vh_all_confirmed = bool(vh_rows) and all(r.confirmed for r in vh_rows)
        vh_editing       = any(getattr(r, "editing", False) for r in vh_rows)
        vh_ready         = vh_all_confirmed and not vh_editing

        # now set each Add-button on its own “ready” flag
        add_package_btn.configure(state="normal" if pkg_ready else "disabled")
        add_vehicle_btn.configure(state="normal" if vh_ready else "disabled")

        # Solve only when both are ready
        solve_btn.configure(state="normal" if pkg_ready and vh_ready else "disabled")

    def add_package_bar(x="", y="", w="", p=""):
        row = ctk.CTkFrame(package_scroll)
        row.pack(pady=5, padx=5)
        row.confirmed = False
        row.editing   = False

        id_lbl = ctk.CTkLabel(row, text="", width=30)
        id_lbl.pack(side="left", padx=5)

        entries = {}
        for key, val, width in zip(
            ("X","Y","Weight","Priority"),
            (x,y,w,p),
            (50,50,80,60)
        ):
            e = ctk.CTkEntry(row, placeholder_text=key, width=width)
            # **insert any pre-existing value**  
            if val:
                e.insert(0, val)
            # then stash its “normal” colors  
            e._orig_fg_color   = e.cget("fg_color")
            e._orig_text_color = e.cget("text_color")
            e.pack(side="left", padx=5)
            entries[key] = e

        err_lbl = ctk.CTkLabel(row, text="", text_color="red", font=("Courier",12))
        err_lbl.pack(side="left", padx=(5,10))

        def on_delete():
            rows = package_scroll.winfo_children()
            if len(rows)==1:
                for e in entries.values():
                    e.configure(state="normal")
                    e.delete(0,"end")
                row.confirmed = False
                row.editing   = False
                err_lbl.configure(text="")
                confirm_btn.pack(side="left", padx=2)
                edit_btn.pack_forget()
            else:
                row.destroy()
                update_package_ids()
            update_add_buttons_state()

        def on_confirm():
            vals = {k:e.get().strip() for k,e in entries.items()}
            if any(v=="" for v in vals.values()):
                err_lbl.configure(text="⚠ fill all fields"); return
            try:
                xv,yv,wv = float(vals["X"]), float(vals["Y"]), float(vals["Weight"])
            except ValueError:
                err_lbl.configure(text="⚠ X,Y,Weight must be numeric"); return
            try:
                pv = int(vals["Priority"])
            except ValueError:
                err_lbl.configure(text="Priority must be integer"); return
            if not (0<=xv<=100 and 0<=yv<=100):
                err_lbl.configure(text="⚠ X,Y ∈ [0,100]"); return
            if wv<=0:
                err_lbl.configure(text="Weight must be > 0"); return
            if not (0<=pv<=5):
                err_lbl.configure(text="⚠ Priority ∈ [0,5]"); return

            row.confirmed = True
            row.editing   = False
            for e in entries.values():
                e.configure(state="readonly")
            err_lbl.configure(text="")
            confirm_btn.pack_forget()
            edit_btn.pack(side="left", padx=2)
            for widget in row.winfo_children():
                if isinstance(widget, ctk.CTkEntry):
                    widget.configure(fg_color=get_locked_color())
                    widget.configure(text_color="gray")
            update_add_buttons_state()

        def on_edit():
            row.confirmed = False
            row.editing   = True
            for e in entries.values():
                e.configure(state="normal")
            edit_btn.pack_forget()
            confirm_btn.pack(side="left", padx=2)
            for widget in row.winfo_children():
                if isinstance(widget, ctk.CTkEntry):
                    widget.configure (
                        fg_color=widget._orig_fg_color,
                        text_color=widget._orig_text_color
                        )
            update_add_buttons_state()

        delete_btn = ctk.CTkButton(row, text="❌", width=30, fg_color="red", hover_color="#cc0000", command=on_delete)
        confirm_btn= ctk.CTkButton(row, text="✅", width=30, fg_color="#28a745", hover_color="#218838", text_color="white", command=on_confirm)
        edit_btn   = ctk.CTkButton(row, text="✏️", width=30, fg_color="#ffc107", hover_color="#e0a800", text_color="black", command=on_edit)

        delete_btn.pack(side="left", padx=2)
        confirm_btn.pack(side="left", padx=2)
        edit_btn.pack_forget()

        for e in entries.values():
            e.bind("<Return>", lambda ev, fn=on_confirm: fn())

        update_package_ids()
        update_add_buttons_state()

    def add_vehicle_bar(cap=""):
        row = ctk.CTkFrame(vehicle_scroll)
        row.pack(pady=5, padx=5)
        row.confirmed = False
        row.editing   = False

        id_lbl = ctk.CTkLabel(row, text="", width=30)
        id_lbl.pack(side="left", padx=5)

        cap_entry = ctk.CTkEntry(row, placeholder_text="Capacity", width=100)
        if cap:
            cap_entry.insert(0, cap)
        cap_entry._orig_fg_color   = cap_entry.cget("fg_color")
        cap_entry._orig_text_color = cap_entry.cget("text_color")
        cap_entry.pack(side="left", padx=5)

        err_lbl = ctk.CTkLabel(row, text="", text_color="red", font=("Courier",12))
        err_lbl.pack(side="left", padx=(5,10))

        def on_delete():
            rows = vehicle_scroll.winfo_children()
            if len(rows)==1:
                cap_entry.configure(state="normal")
                cap_entry.delete(0,"end")
                row.confirmed = False
                row.editing   = False
                err_lbl.configure(text="")
                confirm_btn.pack(side="left", padx=2)
                edit_btn.pack_forget()
            else:
                row.destroy()
                update_vehicle_ids()
            update_add_buttons_state()

        def on_confirm():
            val = cap_entry.get().strip()
            if not val:
                err_lbl.configure(text="⚠ fill capacity"); return
            try:
                cv = float(val)
            except ValueError:
                err_lbl.configure(text="Capacity must be numeric"); return
            if cv<=0:
                err_lbl.configure(text="Capacity must be > 0"); return

            row.confirmed = True
            row.editing   = False
            cap_entry.configure(state="readonly")
            err_lbl.configure(text="")
            confirm_btn.pack_forget()
            edit_btn.pack(side="left", padx=2)
            for widget in row.winfo_children():
                if isinstance(widget, ctk.CTkEntry):
                    widget.configure(fg_color=get_locked_color())
                    widget.configure(text_color="gray")
            update_add_buttons_state()

        def on_edit():
            row.confirmed = False
            row.editing   = True
            cap_entry.configure(state="normal")
            edit_btn.pack_forget()
            confirm_btn.pack(side="left", padx=2)
            for widget in row.winfo_children():
                if isinstance(widget, ctk.CTkEntry):
                    widget.configure (
                        fg_color=widget._orig_fg_color,
                        text_color=widget._orig_text_color
                        )
            update_add_buttons_state()

        delete_btn = ctk.CTkButton(row, text="❌", width=30, fg_color="red", hover_color="#cc0000", command=on_delete)
        confirm_btn= ctk.CTkButton(row, text="✅", width=30, fg_color="#28a745", hover_color="#218838", text_color="white", command=on_confirm)
        edit_btn   = ctk.CTkButton(row, text="✏️", width=30, fg_color="#ffc107", hover_color="#e0a800", text_color="black", command=on_edit)

        delete_btn.pack(side="left", padx=2)
        confirm_btn.pack(side="left", padx=2)
        edit_btn.pack_forget()

        cap_entry.bind("<Return>", lambda ev, fn=on_confirm: fn())

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
        temp = widget
        while temp:
            if isinstance(temp, ctk.CTkEntry): return
            temp = temp.master
        temp = widget
        while temp:
            if temp is settings_btn: return
            temp = temp.master
        app.focus_set()

    app.bind_all("<Button-1>", defocus_entries, add="+")

    collected_data = {          
        'packages': [], 
        'vehicles': [],
        'algorithm': None,
    }

    def collect_data():
        # Variables to store package and vehicle data
        package_data = []  # List of tuples: (id, x, y, weight, priority)
        vehicle_data = []  # List of tuples: (id, capacity)

        # Collect package data
        for i, row in enumerate(package_scroll.winfo_children(), start=1):
            entries = row.winfo_children()[1:-1]  # Skip ID and buttons
            x = float(entries[0].get())
            y = float(entries[1].get())
            weight = float(entries[2].get())
            priority = int(entries[3].get())
            package_data.append((i, x, y, weight, priority))  # Save with id as the first index

        # Collect vehicle data
        for i, row in enumerate(vehicle_scroll.winfo_children(), start=1):
            entries = row.winfo_children()[1:-1]  # Skip ID and buttons
            capacity = float(entries[0].get())
            vehicle_data.append((i, capacity))  # Save with id as the first index

        # Get the selected algorithm
        if algo_var.get() == 1:
            algorithm = "GA"
        else:
            algorithm = "SA"

        return package_data, vehicle_data, algorithm
    
    def solve_callback():
        """Called when Solve button is pressed"""
        collected_data['packages'], collected_data['vehicles'], collected_data['algorithm'] = collect_data()
        app.quit()  # Close the GUI window
        app.destroy()
        

    # Link the solve function to the Solve button
    solve_btn.configure(command=solve_callback)
    app.mainloop()

    return collected_data
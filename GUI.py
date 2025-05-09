#Aboud Fialah           ID: 1220216         Section: 2
#Aws Hammad             ID: 1221697         Section: 3   

import customtkinter as ctk
from tkinter import filedialog
import tkinter.messagebox as mb

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
        #print(f"--- Applying colors for theme: {current_theme}, color: {current_color}")
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
        # Update confirmed package rows
        for row in package_scroll.winfo_children():
            if getattr(row, "confirmed", False):
                for widget in row.winfo_children():
                    if isinstance(widget, ctk.CTkEntry):
                        widget.configure(fg_color=get_locked_color(), text_color="gray")

        # Update confirmed vehicle rows
        for row in vehicle_scroll.winfo_children():
            if getattr(row, "confirmed", False):
                for widget in row.winfo_children():
                    if isinstance(widget, ctk.CTkEntry):
                        widget.configure(fg_color=get_locked_color(), text_color="gray")

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
    algo_var.trace_add("write", lambda *args: update_solve_button_state())
    ctk.CTkRadioButton(algo_frame, text="Genetic Algorithm", variable=algo_var, value=1).pack(side="left", padx=10)
    ctk.CTkRadioButton(algo_frame, text="Simulated Annealing", variable=algo_var, value=2).pack(side="left", padx=10)

    # Settings dropdown
    settings_dropdown = ctk.CTkToplevel(app)
    settings_dropdown.withdraw()
    settings_dropdown.overrideredirect(True)
    settings_dropdown.lift(app)

    def change_theme(choice):
        nonlocal current_theme
        current_theme = choice
        ctk.set_appearance_mode(choice)
        apply_colors()

    def change_color(color_name):
        nonlocal current_color
        #print(f"--- Changing color to: {color_name}") 
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
                # children
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
            # if no blank, assume half packages or guess by count
            # here: everything until a non‐4‐column line is packages
            pkg_lines, vh_lines = [], []
            for L in lines:
                if len(L.split()) == 4:
                    pkg_lines.append(L)
                else:
                    vh_lines.append(L)

        # rebuild
        for L in pkg_lines:
            x, y, w, p = L.split()
            add_package_bar(x, y, w, p, auto_confirm=True)

        for L in vh_lines:
            add_vehicle_bar(L, auto_confirm=True)

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

        # **Is the package table “ready” to add another?
        pkg_all_confirmed = bool(pk_rows) and all(r.confirmed for r in pk_rows)
        pkg_editing       = any(getattr(r, "editing", False) for r in pk_rows)
        pkg_ready         = pkg_all_confirmed and not pkg_editing

        # **Is the vehicle table “ready” to add another?
        vh_all_confirmed = bool(vh_rows) and all(r.confirmed for r in vh_rows)
        vh_editing       = any(getattr(r, "editing", False) for r in vh_rows)
        vh_ready         = vh_all_confirmed and not vh_editing

        # now set each Add-button on its own “ready” flag
        add_package_btn.configure(state="normal" if pkg_ready else "disabled")
        add_vehicle_btn.configure(state="normal" if vh_ready else "disabled")

        # Solve only when both are ready
        update_solve_button_state()
    def update_solve_button_state():
        pk_rows = package_scroll.winfo_children()
        vh_rows = vehicle_scroll.winfo_children()
        
        # Package table ready
        pkg_ready = bool(pk_rows) and all(getattr(r, "confirmed", False) for r in pk_rows) and not any(getattr(r, "editing", False) for r in pk_rows)
        
        # Vehicle table ready
        vh_ready = bool(vh_rows) and all(getattr(r, "confirmed", False) for r in vh_rows) and not any(getattr(r, "editing", False) for r in vh_rows)

        # Algorithm selected
        algo_chosen = algo_var.get() in (1, 2)

        # Total weight and capacity check
        try:
            total_weight = sum(float(r.winfo_children()[3].get()) for r in pk_rows)
            total_capacity = sum(float(r.winfo_children()[1].get()) for r in vh_rows)
            weight_ok = total_weight <= total_capacity
        except:
            weight_ok = False

        solve_btn.configure(
            state="normal" if pkg_ready and vh_ready and algo_chosen and weight_ok else "disabled"
        )

    def add_package_bar(x="", y="", w="", p="", auto_confirm=False):
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
            # insert any pre-existing value
            if val:
                e.insert(0, val)
            # then stash its normal colors  
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
        
        if auto_confirm:
            on_confirm()

        update_package_ids()
        update_add_buttons_state()

    def add_vehicle_bar(cap="", auto_confirm=False):
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
        
        if auto_confirm:
            on_confirm()

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
        if event.widget.winfo_toplevel() is not app:
            return
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
        # 1) collect & optimize
        collected_data['packages'], collected_data['vehicles'], collected_data['algorithm'] = collect_data()
        from loadManager import LoadManager
        manager = LoadManager()
        manager.load_packages(collected_data['packages'])
        manager.load_vehicles(collected_data['vehicles'])
        params = {
            "GA": {'population_size': 150, 'mutation_rate': 0.02, 'num_of_generations': 1000},
            "SA": {'initial_temp':1000, 'cooling_rate':0.96, 'stopping_temp':1, 'num_of_iterations':100}
        }
        
        try:
            result = manager.optimize(collected_data['algorithm'], params)
        except ValueError as e:
            mb.showerror("Assignment Error", str(e))
            return
        
        if isinstance(result, tuple):
            vehicles, total_cost = result
        else:
            vehicles, total_cost = result, sum(v.distance for v in result)

        active_vs = [v for v in vehicles if v.packages]
        if not active_vs:
            print("⚠ No routes to animate.")
            return

        # 2) make the toplevel & canvas
        from tkinter import Canvas
        anim_win = ctk.CTkToplevel(app)
        anim_win.title("SmartDrop SA Animation")
        try:
            anim_win.state('zoomed')
        except:
            anim_win.attributes('-zoomed', True)
        anim_win.transient(app)
        anim_win.grab_set()
        anim_win.lift()
        anim_win.focus_force()

        # 3) create a fixed-size canvas and center it
        CANVAS_W, CANVAS_H = 2450, 1400
        canvas = Canvas(
            anim_win,
            width=CANVAS_W, height=CANVAS_H,
            bg="#1F2937",
            highlightthickness=1,
            highlightbackground="#374151"
        )
        canvas.place(relx=0.5, rely=0.43, anchor="center")
        
        # Vehicle list frame (initially hidden)
        list_frame = ctk.CTkFrame(anim_win, fg_color="transparent")
        is_list_visible = [False]  # mutable flag to track visibility

        def toggle_vehicle_panel():
            if is_list_visible[0]:
                list_frame.place_forget()
                is_list_visible[0] = False
                toggle_btn.configure(text="📋 Show Vehicles")
            else:
                list_frame.place(relx=0.01, rely=0.01, anchor="nw")
                is_list_visible[0] = True
                toggle_btn.configure(text="📋 Hide Vehicles")
                
        # Vehicle list header & total 
        colors = [
            "#e6194B", "#3cb44b", "#ffe119", "#4363d8",
            "#f58231", "#911eb4", "#42d4f4", "#f032e6",
            "#bfef45", "#fabebe", "#469990", "#e6beff",
            "#9A6324", "#fffac8", "#800000", "#aaffc3",
            "#000075", "#a9a9a9"
        ]
        ctk.CTkLabel(
            list_frame,
            text="Vehicles",
            font=("Courier",16,"bold"),
            text_color="white"
        ).pack(pady=(5,2), padx=10)

        total_distance = sum(v.distance for v in vehicles)
        ctk.CTkLabel(
            list_frame,
            text=f"Total Distance: {total_distance:.2f}",
            font=("Courier",14),
            text_color="#AAAAAA"
        ).pack(pady=(0,10), padx=10)

        # Map each active vehicle to its color 
        color_map = {
            v.id: colors[i % len(colors)]
            for i, v in enumerate(active_vs)
        }

        # 4) List every vehicle sorted by ID 
        for v in sorted(vehicles, key=lambda v: v.id):
            row = ctk.CTkFrame(list_frame, fg_color="transparent")
            row.pack(anchor="w", pady=3, padx=10)

            # pick its assigned color if it ran, or grey if unused
            col = color_map.get(v.id, "gray")
            circle = ctk.CTkLabel(
                row,
                text="🚚",
                font=("Arial",16),
                text_color=col
            )
            circle.pack(side="left", padx=(0,6))

            pkg_count = len(v.packages)
            label_text = f"Vehicle {v.id}   |   📦 {pkg_count}   |   📏 {v.distance:.2f}"
            ctk.CTkLabel(
                row,
                text=label_text,
                font=("Courier",14),
                text_color="white"
            ).pack(side="left")
        

        # 5) compute scale & origin based on the canvas size
        world_size = 100
        step_units  = 10

        # use just a 5px margin on top/bottom/left
        margin = 5
        grid_w = 2100 - 2 * margin
        grid_h = 1200 - 2 * margin
        grid_origin_x = (CANVAS_W - grid_w) // 2
        grid_origin_y = (CANVAS_H - grid_h) // 2
        scale_x = grid_w / world_size
        scale_y = grid_h / world_size
        origin_px = (grid_origin_x, grid_origin_y + grid_h)
        # grid spacing in pixels
        step_px_x = step_units * scale_x
        step_px_y = step_units * scale_y
        n_lines = int(world_size // step_units) + 1

        # Draw vertical grid lines + X labels
        for i in range(n_lines):
            x = grid_origin_x + i * step_px_x
            canvas.create_line(x, grid_origin_y, x, grid_origin_y + grid_h, fill="white", width=2)
            
            # X-axis label (bottom)
            canvas.create_text(
                x, grid_origin_y + grid_h + 15,  # a bit below the bottom line
                text=str(i * step_units), fill="white", font=("Courier", 12)
            )

        # 6) Draw horizontal grid lines + Y labels
        for i in range(n_lines):
            y = grid_origin_y + i * step_px_y
            canvas.create_line(grid_origin_x, y, grid_origin_x + grid_w, y, fill="white", width=2)
        
            # Y-axis label (left)
            canvas.create_text(
                grid_origin_x - 15, y,  # a bit to the left of the line
                text=str((n_lines - 1 - i) * step_units), fill="white", font=("Courier", 12)
            )
        canvas.create_text(CANVAS_W/2, CANVAS_H-30, text="X coordinate", fill="white", font=("Courier",14))
        canvas.create_text(50, CANVAS_H/2, text="Y coordinate", fill="white", font=("Courier",14), angle=90)
        canvas.create_text(CANVAS_W/2, 55, text="SmartDrop Animation", fill="white", font=("Courier",20,"bold"))

        for idx, v in enumerate(active_vs):
            color = colors[idx % len(colors)]
            for p in v.packages:
                px = origin_px[0] + p.x * scale_x
                py = origin_px[1] - p.y * scale_y  # invert Y for canvas

                # Draw the package as a colored dot
                canvas.create_oval(px - 4, py - 4, px + 4, py + 4, fill=color, outline="")

                # Add a label for the package ID
                canvas.create_text(px, py - 15, text=str(p.id), font=("Helvetica", 14), fill=color)
        # 7) draw empty vehicles at depot
        for v in vehicles:
            if not v.packages:
                x0, y0 = origin_px
                canvas.create_oval(x0-8, y0-8, x0+8, y0+8, fill="gray", outline="")
                canvas.create_text(x0, y0-16, text=f"V{v.id}", font=("Helvetica",10), fill="white")

        # 8) prepare each active vehicle’s path & shape
        colors = [
            "#e6194B", "#3cb44b", "#ffe119", "#4363d8", "#f58231", "#911eb4",
            "#42d4f4", "#f032e6", "#bfef45", "#fabebe", "#469990", "#e6beff",
            "#9A6324", "#fffac8", "#800000", "#aaffc3", "#000075", "#a9a9a9"
        ]
        veh_anim = []
        for idx, v in enumerate(active_vs):
            world_path = [(0,0)] + [(p.x, p.y) for p in v.packages] + [(0,0)]
            px = origin_px[0] + x * scale_x
            py = origin_px[1] - y * scale_y
            pixel_path = []
            color = colors[idx % len(colors)]

            for x, y in world_path:
                px = origin_px[0] + x * scale_x
                py = origin_px[1] - y * scale_y
                pixel_path.append((px, py))

            x0, y0 = pixel_path[0]
            shape = canvas.create_oval(x0-12, y0-12, x0+12, y0+12, fill=color, outline="")
            label = canvas.create_text(x0, y0-16, text=f"V{v.id}", font=("Helvetica",12,"bold"), fill="white")

            veh_anim.append({"shape": shape, "label": label, "path": pixel_path, "step": 0, "color": color, "trail": []})

        # 9) animation loop
        def move():
            running = False
            for data in veh_anim:
                path, s = data["path"], data["step"]
                if s < len(path) - 1:
                    running = True
                    x1, y1, x2, y2 = canvas.coords(data["shape"])
                    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
                    tx, ty = path[s + 1]
                    dx, dy = (tx - cx) / 10, (ty - cy) / 10
                    canvas.move(data["shape"], dx, dy)
                    canvas.move(data["label"], dx, dy)
                    canvas.update_idletasks()
                    if abs(tx - cx) < 2 and abs(ty - cy) < 2:
                        data["step"] += 1
            if running:
                anim_win.after(50, move)
        def reset_and_replay():
            for data in veh_anim:
                start_x, start_y = data["path"][0]
                x1, y1, x2, y2 = canvas.coords(data["shape"])
                cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
                dx = start_x - cx
                dy = start_y - cy
                canvas.move(data["shape"], dx, dy)
                canvas.move(data["label"], dx, dy)
                data["step"] = 0
            move_controlled()
            
        is_paused = [False]  # mutable wrapper

        def toggle_pause():
            is_paused[0] = not is_paused[0]
            pause_btn.configure(text="▶️ Resume" if is_paused[0] else "⏸️ Pause")

        def move_controlled():
            if is_paused[0]:
                anim_win.after(100, move_controlled)
                return

            running = False
            for data in veh_anim:
                path, s = data["path"], data["step"]
                if s < len(path) - 1:
                    running = True
                    x1, y1, x2, y2 = canvas.coords(data["shape"])
                    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
                    tx, ty = path[s + 1]
                    dx, dy = (tx - cx) / 10, (ty - cy) / 10
                    canvas.move(data["shape"], dx, dy)
                    trail_start = (cx, cy)
                    trail_end = (cx + dx, cy + dy)
                    line = canvas.create_line(*trail_start, *trail_end, fill=data["color"], width=2)
                    data["trail"].append(line)
                    canvas.move(data["label"], dx, dy)
                    canvas.update_idletasks()
                    if abs(tx - cx) < 2 and abs(ty - cy) < 2:
                        data["step"] += 1
            if running:
                anim_win.after(50, move_controlled)

        def reset_and_replay():
            for data in veh_anim:
                start_x, start_y = data["path"][0]
                x1, y1, x2, y2 = canvas.coords(data["shape"])
                cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
                dx = start_x - cx
                dy = start_y - cy
                canvas.move(data["shape"], dx, dy)
                canvas.move(data["label"], dx, dy)
                data["step"] = 0
            is_paused[0] = False
            pause_btn.configure(text="⏸️ Pause")
            move_controlled()

        # Control Button Layout
        controls_frame = ctk.CTkFrame(anim_win, fg_color="transparent")
        controls_frame.place(relx=0.5, rely=0.9, anchor="center")
        toggle_btn = ctk.CTkButton(controls_frame, text="📋 Show Vehicles", command=toggle_vehicle_panel)
        toggle_btn.pack(side="left", padx=10)

        replay_btn = ctk.CTkButton(controls_frame, text="🔁 Replay", command=reset_and_replay)
        replay_btn.pack(side="left", padx=10)

        pause_btn = ctk.CTkButton(controls_frame, text="⏸️ Pause", command=toggle_pause)
        pause_btn.pack(side="left", padx=10)

        exit_btn = ctk.CTkButton(controls_frame, text="❌ Exit", command=anim_win.destroy, fg_color="red", hover_color="#aa0000")
        exit_btn.pack(side="left", padx=10)

        # Initial run
        move_controlled()
    # Link the solve function to the Solve button
    solve_btn.configure(command=solve_callback)
    app.mainloop()

    return collected_data
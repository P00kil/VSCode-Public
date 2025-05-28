import tkinter as tk
import tkinter.ttk as ttk
import random
import platform
import tkinter.messagebox as messagebox
import os

# Zeichenarten für Passwortgenerierung
g = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
k = 'abcdefghijklmnopqrstuvwxyz'
z = '0123456789'
s = '!§%&/()=?*-_.,'

# Speicherpfad für Passwort je nach Betriebssystem
if platform.system() == 'Windows':
    pfad = "C:\\Users\\Public\\Documents\\pwgenlock.txt"
elif platform.system() == 'Darwin':  # macOS
    pfad = "/Users/kilianhandy/Documents/PWGEN1/pwgenlock.txt"
else:
    pfad = "pwgenlock.txt"  # Fallback für andere Systeme

def otp_encrypt(text, key):
    # Text und Key auf gleiche Länge bringen
    key = (key * ((len(text) // len(key)) + 1))[:len(text)]
    return ''.join([chr(ord(a) ^ ord(b)) for a, b in zip(text, key)])


def otp_decrypt(cipher, key):
    # Entschlüsseln ist identisch zu Verschlüsseln
    return otp_encrypt(cipher, key)


class app(tk.Frame):

    def __init__(self):
        self.otp_key = ""  # OTP-Schlüssel
        self.password_data = []  # Speichert (site, email, pw)
        self.root = tk.Tk()
        super().__init__(self.root)
        self.root.geometry('800x450')
        self.root.title('Passwort-Generator')

        # Dunkles Farbschema
        self.font_family = 'Segoe UI' if platform.system() == 'Windows' else 'Helvetica'
        self.bg_color = "#1b1f26"      # Dunkler Hintergrund
        self.fg_color = '#f5f6fa'      # Heller Text
        self.entry_bg = "#2d2e3b"      # Dunkelgrau für Eingabefelder/Textfelder
        self.entry_fg = '#f5f6fa'      # Heller Text in Eingabefeldern
        self.highlight_color = "#483161"  # Noch dunkler für Hervorhebung
        self.button_bg = "#2F313C"     # Mittelgrau für Buttons
        self.button_fg = '#f5f6fa'     # Heller Text auf Buttons


        self.start_window()
        self.mainloop()

    def start_window(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', background=self.button_bg, foreground=self.button_fg, font=(self.font_family, 11))
        style.map('TButton',
             background=[('active', self.highlight_color), ('!active', self.button_bg)],
             foreground=[('active', self.button_fg), ('!active', self.button_fg)]
        )   
        self.frame_start = tk.Frame(self.root, bg=self.bg_color)
        self.frame_start.place(x=0, y=0, width=800, height=450)
        # Label mittig
        self.label_start = tk.Label(self.frame_start, text="Passwortmanager V1.1", font=(self.font_family, 16), bg=self.bg_color, fg=self.fg_color)
        self.label_start.place(relx=0.5, rely=0.4, anchor="center")
        # Entry mittig darunter
        self.key_entry = tk.Entry(
            self.frame_start,
            width=30,
            font=(self.font_family, 12),
            bg=self.entry_bg,
            fg=self.entry_fg,
            insertbackground=self.entry_fg,
            highlightbackground=self.bg_color
        )
        self.key_entry.place(relx=0.5, rely=0.5, anchor="center")
        self.key_entry.insert(0, "Schlüssel")
        self.key_entry.bind('<FocusIn>', lambda event: self.key_entry.delete(0, tk.END))
        # Button mittig darunter
        self.button_start = ttk.Button(
            self.frame_start,
            text="Starten",
            command=lambda: (self.set_otp_key(start=True), self.frame_start.destroy(), self.create_widgets()),
            style='TButton'
        )
        self.button_start.place(relx=0.5, rely=0.6, anchor="center")
        self.root.bind('<Return>', lambda event: self.button_start.invoke())  # Enter-Taste zum Starten

    def create_widgets(self):
        self.root.configure(bg=self.bg_color)
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('.', background=self.bg_color, foreground=self.fg_color, fieldbackground=self.entry_bg)
        style.configure('TNotebook', background=self.bg_color)
        style.configure('TNotebook.Tab',
            background=self.bg_color,
            foreground=self.fg_color,
            lightcolor=self.bg_color,
            borderwidth=0,
            padding=[10, 5]
        )
        style.configure('TLabel', background=self.bg_color, foreground=self.fg_color)
        style.configure('TFrame', background=self.bg_color)
        style.configure('TLabelframe', background=self.bg_color, foreground=self.fg_color)
        style.configure('TLabelframe.Label', background=self.bg_color, foreground=self.fg_color)
        style.configure('TButton', background=self.button_bg, foreground=self.button_fg, font=(self.font_family, 11))
        style.map('TButton',
            background=[('active', self.highlight_color), ('!active', self.button_bg)],
            foreground=[('active', self.button_fg), ('!active', self.button_fg)]
        )
        style.map('TNotebook.Tab',
            background=[('selected', self.button_bg), ('active', self.highlight_color)],
            foreground=[('selected', self.button_fg), ('active', self.button_fg)]
        )

        style.configure("Vertical.TScrollbar", background=self.bg_color, troughcolor=self.entry_bg)

        self.notebook1 = ttk.Notebook(self.root)
        self.notebook1.place(x=8, y=8, width=780, height=430)

        # Tab "Erstellen"
        self.notebook1Tab0 = ttk.Frame(self.notebook1)
        self.notebook1.add(self.notebook1Tab0, text=' Erstellen ')

        # Name/Stichwort + Passwortanzeige
        frame_top = tk.Frame(self.notebook1Tab0, bg=self.bg_color)
        frame_top.place(x=20, y=20, width=740, height=60)
        self.name_label = tk.Label(frame_top, text="Website:", font=(self.font_family, 12), bg=self.bg_color, fg=self.fg_color)
        self.name_label.pack(side='left', padx=(0, 10))
        self.site_entry = tk.Entry(frame_top, width=25, font=(self.font_family, 12), bg=self.entry_bg, fg=self.entry_fg, insertbackground=self.entry_fg)
        self.site_entry.pack(side='left')
        self.lPasswort = tk.Label(frame_top, text='Passwort', font=(self.font_family, 20), anchor='center', width=20, bg=self.bg_color, fg=self.fg_color)
        self.lPasswort.pack(side='left', padx=(40, 0))

        # Zeichenarten + Länge
        frame_opts = tk.LabelFrame(self.notebook1Tab0, text=' Optionen ', font=(self.font_family, 10), bg=self.bg_color, fg=self.fg_color)
        frame_opts.place(x=20, y=150, width=350, height=120)
        self.radiobuttonGroup1RB0CV = tk.IntVar(value=1)
        self.radiobuttonGroup1RB1CV = tk.IntVar(value=0)
        self.radiobuttonGroup1RB2CV = tk.IntVar(value=0)
        self.radiobuttonGroup1RB3CV = tk.IntVar(value=0)
        tk.Checkbutton(frame_opts, anchor='w', text='GROSSBUCHSTABEN', variable=self.radiobuttonGroup1RB0CV, font=(self.font_family, 10), bg=self.bg_color, fg=self.fg_color, selectcolor=self.highlight_color, activebackground=self.bg_color, activeforeground=self.fg_color).grid(row=0, column=0, sticky='w')
        tk.Checkbutton(frame_opts, anchor='w', text='kleinbuchstaben', variable=self.radiobuttonGroup1RB1CV, font=(self.font_family, 10), bg=self.bg_color, fg=self.fg_color, selectcolor=self.highlight_color, activebackground=self.bg_color, activeforeground=self.fg_color).grid(row=1, column=0, sticky='w')
        tk.Checkbutton(frame_opts, anchor='w', text='Ziffern', variable=self.radiobuttonGroup1RB2CV, font=(self.font_family, 10), bg=self.bg_color, fg=self.fg_color, selectcolor=self.highlight_color, activebackground=self.bg_color, activeforeground=self.fg_color).grid(row=2, column=0, sticky='w')
        tk.Checkbutton(frame_opts, anchor='w', text='Sonderzeichen', variable=self.radiobuttonGroup1RB3CV, font=(self.font_family, 10), bg=self.bg_color, fg=self.fg_color, selectcolor=self.highlight_color, activebackground=self.bg_color, activeforeground=self.fg_color).grid(row=3, column=0, sticky='w')
        self.lAnzahlZeichen = tk.Label(frame_opts, text='Anzahl Zeichen:', font=(self.font_family, 12), bg=self.bg_color, fg=self.fg_color)
        self.lAnzahlZeichen.grid(row=0, column=1, padx=(20, 0), sticky='w')
        self.scale1CV = tk.IntVar(value=8)
        self.scale1 = tk.Scale(frame_opts, variable=self.scale1CV, orient='horizontal', from_=5, to=20, length=120, font=(self.font_family, 10), bg=self.bg_color, fg=self.fg_color, troughcolor=self.highlight_color, highlightbackground=self.bg_color)
        self.scale1.grid(row=1, column=1, rowspan=3, padx=(20, 0), sticky='w')

        # Buttons
        frame_btns = tk.Frame(self.notebook1Tab0, bg=self.bg_color)
        frame_btns.place(x=400, y=160, width=350, height=120) 

        self.bPasswortgenerieren = ttk.Button(
            frame_btns,
            text='Passwort generieren',
            command=self.bPasswortgenerieren_Command
        )
        self.bPasswortgenerieren.pack(pady=(5, 8), fill='x')

        self.button1 = ttk.Button(
            frame_btns,
            text="Sichern",
            command=self.button1_Command
        )
        self.button1.pack(pady=5, fill='x')
        

        # E-Mail-Eingabe
        frame_middle = tk.Frame(self.notebook1Tab0, bg=self.bg_color)
        frame_middle.place(x=20, y=80, width=320, height=60)
        self.name_label = tk.Label(frame_middle, text="E-Mail:", font=(self.font_family, 12), bg=self.bg_color, fg=self.fg_color)
        self.name_label.pack(side='left', padx=(0, 21))
        self.name_entry = tk.Entry(frame_middle, width=25, font=(self.font_family, 12), bg=self.entry_bg, fg=self.entry_fg, insertbackground=self.entry_fg)
        self.name_entry.pack(side='left')

        # Tab "Verwalten"
        self.notebook1Tab1 = ttk.Frame(self.notebook1)
        self.notebook1.add(self.notebook1Tab1, text=' Verwalten ')

        frame_search = tk.LabelFrame(self.notebook1Tab1, text=" Passwort suchen ", font=(self.font_family, 10), bg=self.bg_color, fg=self.fg_color)
        frame_search.place(x=20, y=20, width=500, height=80)
        self.search_label = tk.Label(frame_search, text="Website", font=(self.font_family, 11), bg=self.bg_color, fg=self.fg_color)
        self.search_label.pack(side='left', padx=(10, 5))
        self.search_entry = tk.Entry(frame_search, width=20, font=(self.font_family, 11), bg=self.entry_bg, fg=self.entry_fg, insertbackground=self.entry_fg)
        self.search_entry.pack(side='left', padx=(0, 10))
        self.search_button = ttk.Button(
            frame_search, text="Suchen", command=self.search_password, style='TButton'
        )
        self.search_button.pack(side='left', padx=(0, 10))

        self.password_list_label = tk.Label(
            self.notebook1Tab1,
            text="Alle gespeicherten Passwörter:",
            anchor='w',
            font=(self.font_family, 11),
            fg=self.fg_color,
            bg=self.bg_color
        )
        self.password_list_label.place(x=30, y=150, width=730, height=25)

        # Scrollbar
        self.scrollbar = tk.Scrollbar(self.notebook1Tab1, orient='vertical')
        self.scrollbar.place(x=730, y=180, height=190)

        self.password_list = tk.Listbox(
            self.notebook1Tab1,
            height=12,
            width=60,
            font=(self.font_family, 11),
            fg=self.entry_fg,
            bg=self.entry_bg,
            selectbackground=self.highlight_color,
            selectforeground=self.fg_color,
            yscrollcommand=self.scrollbar.set
        )
        self.password_list.place(x=30, y=180, width=700, height=190)
        self.password_list.bind('<<ListboxSelect>>', self.on_password_select)
        self.scrollbar.config(command=self.password_list.yview)

        # Tab "Schlüssel"
        self.notebook1Tab2 = ttk.Frame(self.notebook1)
        self.notebook1.add(self.notebook1Tab2, text=' Schlüssel ')

        frame_otp = tk.LabelFrame(self.notebook1Tab2, text="Schlüssel ", font=(self.font_family, 10), bg=self.bg_color, fg=self.fg_color)
        frame_otp.place(x=20, y=40, width=500, height=80)
        self.key_label = tk.Label(frame_otp, text="Schlüssel:", font=(self.font_family, 11), bg=self.bg_color, fg=self.fg_color)
        self.key_label.pack(side='left', padx=(10, 5))
        self.key_entry = tk.Entry(frame_otp, show="*", width=20, font=(self.font_family, 11), bg=self.entry_bg, fg=self.entry_fg, insertbackground=self.entry_fg)
        self.key_entry.pack(side='left', padx=(0, 10))
        self.key_button = ttk.Button(
            frame_otp, text="Setzen", command=self.set_otp_key, style='TButton'
        )
        self.key_button.pack(side='left', padx=(0, 10))
        self.key_status = tk.Label(self.notebook1Tab2, text="", anchor='w', font=(self.font_family, 11), fg=self.fg_color, bg=self.bg_color)
        self.key_status.place(x=30, y=130, width=480, height=25)

        # Event-Handler für Tab-Wechsel
        def on_tab_changed(event):
            if self.notebook1.index(self.notebook1.select()) == 1:  # 1 = "Verwalten"-Tab
                self.show_all_passwords()

        self.notebook1.bind("<<NotebookTabChanged>>", on_tab_changed)

    def bPasswortgenerieren_Command(self):
        global g, k, z, s
        v = ''
        xg, xk, xz, xs = '', '', '', ''
        laenge = int(self.scale1CV.get())
        gg = self.radiobuttonGroup1RB0CV.get()
        kk = self.radiobuttonGroup1RB1CV.get()
        zz = self.radiobuttonGroup1RB2CV.get()
        ss = self.radiobuttonGroup1RB3CV.get()
        summe = gg + kk + zz + ss
        pw = ""
        if summe == 0:
            self.lPasswort["text"] = "Wähle Zeichenart aus!"
            return
        if gg == 1:
            xg = random.choice(g)
            v += g
        if kk == 1:
            xk = random.choice(k)
            v += k
        if zz == 1:
            xz = random.choice(z)
            v += z
        if ss == 1:
            xs = random.choice(s)
            v += s

        p1 = xg + xk + xz + xs
        l1 = laenge - len(p1)
        for _ in range(l1):
            p1 += random.choice(v)
        liste = list(p1)
        random.shuffle(liste)
        self.pw = ''.join(liste)
        self.lPasswort['text'] = self.pw

    def show_all_passwords(self):
        import base64
        self.password_list.delete(0, tk.END)
        self.password_data = []
        if not self.otp_key:
            self.password_list.insert(tk.END, "Bitte Schlüssel setzen, um Passwörter anzuzeigen.")
            return
        try:
            with open(pfad, "r", encoding="utf-8") as datei:
                lines = datei.readlines()
            for line in lines:
                if ":" not in line:
                    continue
                entry, encrypted_pw_b64 = line.strip().split(":", 1)
                if ',' in entry:
                    idx = entry.index(',')
                    site = entry[:idx]
                    email = entry[idx+1:]  # Das Komma wird entfernt!
                else:
                    site = entry
                    email = ""
                try:
                    encrypted_pw = base64.b64decode(encrypted_pw_b64).decode("latin1")
                    pw = otp_decrypt(encrypted_pw, self.otp_key)
                except Exception:
                    pw = "[Entschlüsselung fehlgeschlagen]"
                emailneu = email.replace(',', ' ')
                self.password_data.append((site, emailneu, pw))
                self.password_list.insert(tk.END, site)
            if not self.password_data:
                self.password_list.insert(tk.END, " Keine Passwörter gespeichert.")
        except Exception as e:
            self.password_list.insert(tk.END, f" Fehler: {e}")

    def set_otp_key(self, start=False):
        key = self.key_entry.get().strip()
        if key:
            self.otp_key = key
            if not start and hasattr(self, 'key_status'):
                self.key_status['text'] = "Schlüssel gesetzt."
            if not start:
                self.show_all_passwords()
        else:
            if not start and hasattr(self, 'key_status'):
                self.key_status['text'] = "Bitte Schlüssel eingeben!"

    def button1_Command(self):
        name = self.name_entry.get().strip()
        site = self.site_entry.get().strip()
        missing = []
        if not site:
            missing.append("Website fehlt")
        if not name:
            missing.append("E-Mail fehlt")
        if not hasattr(self, 'pw') or not getattr(self, 'pw', ''):
            missing.append("Passwort fehlt")
        if missing:
            # Label genau dort platzieren, wo "Passwort" steht (z.B. x=400, y=20)
            self.lPasswort.place_forget()
            self.lPasswort = tk.Label(
                self.notebook1Tab0,
                text="\n".join(missing),
                font=(self.font_family, 20),
                anchor='center',
                justify='center',
                width=20,
                height=len(missing),
                bg=self.bg_color,
                fg=self.fg_color
            )
            self.lPasswort.place(x=400, y=20)  # Hier ist die Position wie beim ursprünglichen "Passwort"
            return
        # Nach erfolgreichem Speichern wieder Standardgröße und Position
        self.lPasswort.place_forget()
        self.lPasswort = tk.Label(
            self.notebook1Tab0,
            text="Gespeichert!",
            font=(self.font_family, 20),
            anchor='center',
            justify='center',
            width=20,
            height=1,
            bg=self.bg_color,
            fg=self.fg_color
        )
        self.lPasswort.place(x=400, y=20)
        if not self.otp_key:
            messagebox.showwarning("Schlüssel fehlt", "Bitte zuerst den Schlüssel setzen!")
            return
        encrypted_pw = otp_encrypt(self.pw, self.otp_key)
        import base64
        encrypted_pw_b64 = base64.b64encode(encrypted_pw.encode("latin1")).decode("ascii")
        with open(pfad, "a", encoding="utf-8") as datei:
            datei.write(f"{site},{name}:{encrypted_pw_b64}\n")
        self.lPasswort['text'] = "Gespeichert!"
        self.show_all_passwords()  # Nach dem Speichern aktualisieren

    def search_password(self):
        keyword = self.search_entry.get().strip().lower()
        if not self.otp_key:
            messagebox.showwarning("Schlüssel fehlt", "Bitte zuerst den Schlüssel setzen!")
            return
        import base64
        self.password_list.delete(0, tk.END)
        self.password_data = []
        try:
            with open(pfad, "r", encoding="utf-8") as datei:
                lines = datei.readlines()
            for line in lines:
                if ":" not in line:
                    continue
                entry, encrypted_pw_b64 = line.strip().split(":", 1)
                # Trenne site und email
                if ',' in entry:
                    idx = entry.index(',')
                    site = entry[:idx]
                    email = entry[idx+1:]  # Das Komma wird entfernt!
                else:
                    site = entry
                    email = ""
                # Suche in site und email
                if keyword in site.lower() or keyword in email.lower():
                    try:
                        encrypted_pw = base64.b64decode(encrypted_pw_b64).decode("latin1")
                        pw = otp_decrypt(encrypted_pw, self.otp_key)
                    except Exception:
                        pw = "[Entschlüsselung fehlgeschlagen]"
                    self.password_data.append((site, email, pw))
                    self.password_list.insert(tk.END, site)
            if not self.password_data:
                self.password_list.insert(tk.END, "Kein Passwort gefunden.")
        except Exception as e:
            self.password_list.insert(tk.END, f"Fehler: {e}")

    def on_password_select(self, event):
        selection = self.password_list.curselection()
        if not selection or not self.password_data:
            return
        idx = selection[0]
        if idx >= len(self.password_data):
            return
        site, email, pw = self.password_data[idx]
        win = tk.Toplevel(self.root)
        win.title("Passwort-Details")
        win.geometry("400x250")
        win.configure(bg=self.bg_color)
        tk.Label(win, text=f"Website: {site}", font=(self.font_family, 12)).pack(pady=10)
        tk.Label(win, text=f"E-Mail: {email}", font=(self.font_family, 12)).pack(pady=10)
        tk.Label(win, text=f"Passwort: {pw}", font=(self.font_family, 12)).pack(pady=10)

        def delete_password():
            if not messagebox.askyesno("Löschen bestätigen", "Soll dieses Passwort wirklich gelöscht werden?"):
                return
            try:
                with open(pfad, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                search_key = f"{site},{email}"  # site und email wie in der Datei!
                new_lines = []
                for line in lines:
                    if ":" not in line:
                        new_lines.append(line)
                        continue
                    entry, _ = line.strip().split(":", 1)
                    if entry != search_key:
                        new_lines.append(line)
                with open(pfad, "w", encoding="utf-8") as f:
                    f.writelines(new_lines)
                win.destroy()
                self.show_all_passwords()
            except Exception as e:
                messagebox.showerror("Fehler", f"Löschen fehlgeschlagen: {e}")
       
        button_frame = tk.Frame(win, bg=self.bg_color)
        button_frame.pack(pady=15)
        ttk.Button(button_frame, text="Löschen", command=delete_password).pack(side='left', padx=10)
        ttk.Button(button_frame, text="Schließen", command=win.destroy).pack(side='left', padx=10)

app()

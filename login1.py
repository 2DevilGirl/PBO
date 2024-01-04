import mysql.connector
import pymysql
import os
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle

def connect_to_database():
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'login'
    }
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            return connection
    except mysql.connector.Error as err:
        print(f'Error: {err}')
        return None

def on_login_success(root):
    root.destroy()
    os.system("python main.py")

def login(username, password, label_result, root, frame_login, frame_registration):
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()
            query = "SELECT * FROM log WHERE email = %s AND password = %s"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()

            if result:
                label_result.config(text='Login berhasil.')
                cursor.close()
                connection.close()
                on_login_success(root)
                return
            else:
                label_result.config(text='Akun email belum terdaftar.')

        except pymysql.Error as err:
            label_result.config(text=f'Error: {err}')
        finally:
            cursor.close()
            connection.close()

def switch_to_registration(frame_login, frame_registration):
    frame_login.pack_forget()
    frame_registration.pack()

def simpan_data_login(username, password, label_result, frame_login, frame_registration):
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()
            query = "INSERT INTO log (email, password) VALUES (%s, %s)"
            cursor.execute(query, (username, password))
            connection.commit()
            label_result.config(text='Registrasi berhasil. Data login disimpan.')
            frame_registration.pack_forget()
            frame_login.pack()

        except mysql.connector.Error as err:
            connection.rollback()
            label_result.config(text=f'Error: {err}')
        finally:
            cursor.close()
            connection.close()

def registrasi(entry_username, entry_password, label_result, frame_login, frame_registration):
    new_username = entry_username.get()
    new_password = entry_password.get()
    simpan_data_login(new_username, new_password, label_result, frame_login, frame_registration)

def main():
    root = tk.Tk()
    root.title("Login GUI")

    style = ThemedStyle(root)
    style.set_theme("radiance")
    root.geometry("500x300")
    frame_login = ttk.Frame(root)
    frame_login.pack()

    label_username = ttk.Label(frame_login, text="Email:")
    label_username.pack()
    entry_username = ttk.Entry(frame_login)
    entry_username.pack()

    label_password = ttk.Label(frame_login, text="Password:")
    label_password.pack()
    entry_password = ttk.Entry(frame_login, show="*")
    entry_password.pack()

    label_result = ttk.Label(frame_login, text="")
    label_result.pack()

    # Change the color of the login button to blue
    button_login = ttk.Button(frame_login, text="Login", command=lambda: login(entry_username.get(), entry_password.get(), label_result, root, frame_login, frame_registration), style="TButton", cursor="hand2")
    style.configure("TButton", foreground="blue", background="#FFFFFF", font=('Arial', 12))
    button_login.pack()

    label_not_registered = ttk.Label(frame_login, text="Belum Punya Akun?")
    label_not_registered.pack()

    button_switch_to_registration = ttk.Button(frame_login, text="Daftar", command=lambda: switch_to_registration(frame_login, frame_registration))
    button_switch_to_registration.pack()
    frame_registration = ttk.Frame(root)

    label_new_username = ttk.Label(frame_registration, text="Masukkan email baru:")
    label_new_username.pack()
    entry_new_username = ttk.Entry(frame_registration)
    entry_new_username.pack()

    label_new_password = ttk.Label(frame_registration, text="Masukkan password baru:")
    label_new_password.pack()
    entry_new_password = ttk.Entry(frame_registration, show="*")
    entry_new_password.pack()

    label_registration_result = ttk.Label(frame_registration, text="")
    label_registration_result.pack()

    button_register = ttk.Button(frame_registration, text="Registrasi", command=lambda: registrasi(entry_new_username, entry_new_password, label_registration_result, frame_login, frame_registration), style="TButton", cursor="hand2")
    style.configure("TButton", foreground="blue", background="#FFFFFF", font=('Arial', 12))
    button_register.pack()

    frame_registration.pack_forget()

    root.mainloop()

if __name__ == "__main__":
    main()

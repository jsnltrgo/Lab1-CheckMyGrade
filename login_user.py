import sqlite3
import hashlib
import csv
from database import get_connection


class hashFunction:
    def getHashValue(self, message, type):
        if type.upper() == 'SHA256':
            return hashlib.sha256(message.encode('utf-8')).hexdigest()
        elif type.upper() == 'MD5':
            return hashlib.md5(message.encode('utf-8')).hexdigest()
        else:
            print("Did not find the algo. Possible types are MD5/SHA256")
            return None

class LoginUser:
    def __init__(self, email_id, password, role):
        self.email_id = email_id
        self.password = password
        self.role = role

    def encrypt_password(self, password):
        """Hash the password using SHA256 for one-way storage."""
        return str(hashFunction().getHashValue(password, 'SHA256'))

    def login(self, email_id, password):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT PASSWORD FROM LOGIN WHERE USER_ID = ?", (email_id,))
            row = cursor.fetchone()
            # Hash the login attempt and compare to stored hash
            if row and row[0] == self.encrypt_password(password):
                print(f"Welcome {email_id}")
                return True
            else:
                print("Invalid email or password.")
                return False

    def logout(self):
        print(f"{self.email_id} has been logged out.")

    def change_password(self, old_password, new_password):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT PASSWORD FROM LOGIN WHERE USER_ID = ?", (self.email_id,))
            row = cursor.fetchone()
            # Verify old password by comparing hashes
            if row and row[0] == self.encrypt_password(old_password):
                hashed_new = self.encrypt_password(new_password)
                cursor.execute(
                    "UPDATE LOGIN SET PASSWORD = ? WHERE USER_ID = ?",
                    (hashed_new, self.email_id)
                )
                conn.commit()
                self.sync_to_csv()
                print("Password changed successfully.")
            else:
                print("Old password is incorrect.")

    def add_user(self, email_id, password, role):
        with get_connection() as conn:
            cursor = conn.cursor()
            hashed = self.encrypt_password(password)
            try:
                cursor.execute(
                    "INSERT INTO LOGIN (USER_ID, PASSWORD, ROLE) VALUES (?, ?, ?)",
                    (email_id, hashed, role)
                )
                conn.commit()
                self.sync_to_csv()
                print(f"{email_id} added successfully.")
            except sqlite3.IntegrityError:
                print(f"{email_id} already exists.")

    def sync_to_csv(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM LOGIN")
            rows = cursor.fetchall()
        with open('data/login.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['user_id', 'password', 'role'])
            writer.writerows(rows)
        print("CSV synced")


# test

if __name__ == "__main__":
    user = LoginUser("jason.letargo@sjsu.edu", "pas$w0rd", "student")
    user.add_user("jason.letargo@sjsu.edu", "pas$w0rd", "student")
    user.login("jason.letargo@sjsu.edu", "pas$w0rd")
    user.logout()

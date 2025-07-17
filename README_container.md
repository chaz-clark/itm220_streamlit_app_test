# 🔧 Streamlit CRUD App — Running in a Container (MySQL over TCP)

This guide explains how to run the Streamlit CRUD app **inside a container (like Codespaces, DevContainer, Docker)** when your MySQL server is running on your host machine.

When inside a container:
- You **cannot use the Unix socket** (`/tmp/mysql.sock`) because the container has its own isolated `/tmp`.
- Instead, you must connect to MySQL **over TCP** using the host machine’s IP address.
- Or optionally set up an SSH tunnel if TCP is not allowed.

---

## 🧱 Why doesn’t the default config work?

On macOS (or Linux), the default MySQL server listens on a **Unix socket** at `/tmp/mysql.sock` and sometimes does *not* listen for TCP connections.  
Your container can’t access that socket because it lives only on the host.

---

## 🚀 Step-by-Step Guide

### ✅ Step 1: Make Sure MySQL Listens on TCP

On your host machine:
1️⃣ Edit MySQL’s config file:
- macOS:  
  `/etc/my.cnf`  
  or  
  `/usr/local/mysql/my.cnf`

Add or update this section:
```ini
[mysqld]
bind-address = 0.0.0.0
```

This allows MySQL to listen on all interfaces.

2️⃣ Restart MySQL:
```bash
sudo /usr/local/mysql/support-files/mysql.server restart
```

---

### ✅ Step 2: Find Your Host’s IP Address

On your host (Mac or PC), run:
```bash
ifconfig
```
or
```bash
ipconfig
```

Look for your local network IP, e.g.:
```
192.168.1.123
```

---

### ✅ Step 3: Update `get_connection()` in the App

Inside `streamlit_app_local_mysql.py`, change the connection to use TCP:
```python
import mysql.connector
import streamlit as st

def get_connection():
    try:
        conn = mysql.connector.connect(
            host="192.168.1.123",         # replace with your host's IP
            port=3306,
            user="root",                 # or your MySQL user
            password="your_password",   # your MySQL password
            database="your_database"    # your existing database
        )
        return conn
    except mysql.connector.Error as e:
        st.error(f"Error connecting to MySQL: {e}")
        return None
```

Replace `192.168.1.123` and the credentials with your own.

---

### 🔷 Optional: SSH Tunnel (if TCP is not enabled)

If you cannot change the MySQL config to allow TCP, you can use an SSH tunnel.

Your host must have SSH enabled.

Example using `sshtunnel`:
```python
from sshtunnel import SSHTunnelForwarder
import mysql.connector
import streamlit as st

def get_connection():
    try:
        server = SSHTunnelForwarder(
            ('192.168.1.123', 22),            # host's IP and SSH port
            ssh_username='your_ssh_user',
            ssh_pkey='/path/to/private/key', # or ssh_password='your_password'
            remote_bind_address=('127.0.0.1', 3306)
        )
        server.start()

        conn = mysql.connector.connect(
            host='127.0.0.1',
            port=server.local_bind_port,
            user='root',
            password='your_password',
            database='your_database'
        )
        return conn
    except Exception as e:
        st.error(f"Error: {e}")
        return None
```

You’ll also need to:
```bash
pip install sshtunnel
```

---

### 🚀 Step 4: Run the App in the Container

After updating the connection:
```bash
pip install -r requirements.txt
streamlit run streamlit_app_local_mysql.py
```

Your container will now connect to your host MySQL over TCP (or SSH if used).

---

## 🔍 Troubleshooting

| Problem                                  | Solution |
|------------------------------------------|----------|
| `Can't connect to MySQL server`         | Make sure MySQL is listening on `0.0.0.0` and port `3306` |
| `Access denied`                         | Check your MySQL user & password |
| `Timeout`                               | Check your firewall & host IP |
| Using socket path fails                 | You can’t use `/tmp/mysql.sock` inside a container |

---

## 📝 Summary

✅ On host → MySQL over socket works.  
✅ In container → use host’s IP + TCP connection.  
✅ Or SSH tunnel if TCP isn’t allowed.

---

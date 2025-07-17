# 🔧 Streamlit CRUD App (SQLite + Local MySQL Version)

[![View in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://itm220appapptest-cpcjhoquckesa9crpj5ref.streamlit.app)

This is a simple, fully functional Streamlit web app for performing:
- CRUD operations (Create, Read, Update, Delete)
- A real-world SQL transaction: transferring values between rows using safe, rollback-enabled logic

It uses a **SQLite** database by default for demonstration, and also includes a template for connecting to a **local MySQL database** — ideal for learning database logic and deploying on Streamlit Community Cloud.

---

## 📦 Project Structure

```
.
├── streamlit_app.py              # Main Streamlit app (SQLite)
├── streamlit_app_local_mysql.py  # Streamlit app template for local MySQL
├── config.py                     # Table/column settings
├── requirements.txt              # Dependencies
├── database.sqlite               # Sample SQLite database
```

---

## 🚀 Step-by-Step Guide (For Students)

### ✅ Step 1: Run the Sample App Locally

Before deploying anything, get it working on your own machine.

#### 🧰 Requirements:
- Python 3.8+
- pip (Python package installer)

#### 🔧 Setup Instructions:
1. Clone or download this repo
2. Open a terminal in the repo folder
3. Run:

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`.  
If it doesn't open, try a different browser and copy the URL manually.

Explore the sample app with preloaded users (`Alice`, `Bob`, `Charlie`). Try adding, editing, deleting users, and transferring age.

---

### ☁️ Step 2 (optional): Deploy the Working Example to the Cloud

After running locally and confirming it works:

1. Push your copy of this repo to GitHub
2. Visit: [https://streamlit.io/cloud](https://streamlit.io/cloud)
3. Log in and click **"New app"**
4. Connect your GitHub repo
5. Click **Deploy**

🎉 You now have a live CRUD app running with:
- A sample SQLite DB (`database.sqlite`)
- Features:
  - Add, edit, delete users
  - Transfer age between users

---

### 🔍 Step 3: Explore the Sample App

Open your deployed app in the browser and try the following:

- Add a new user
- Edit an existing user's name or age
- Delete someone from the list
- Use **"Transfer Age Between Users"** to shift age values around

This gives you a feel for how the app works before using your own data.

---

## 🔄 Step 4: Switch to Your Own MySQL Database (Local)

When you're ready to use your own **local MySQL database**, use the `streamlit_app_local_mysql.py` template.

---

### ⚙️ Step 5: Update the MySQL Connection

In `streamlit_app_local_mysql.py`, locate the `get_connection()` function and replace the placeholder values with your own MySQL credentials:

```python
def get_connection():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",    # or "localhost"
            port=3306,
            user="your_user",         # your MySQL username
            password="your_password", # your MySQL password
            database="your_database"  # your existing database name
        )
        return conn
    except mysql.connector.Error as e:
        st.error(f"Error connecting to MySQL: {e}")
        return None
```

---

### 📤 Step 6: Point to Your Existing Table

You’ve already been working on your MySQL database all semester — great!  
You **do not need to create a new table or insert sample data**, just ensure the app refers to the correct database and table you already have.

In `config.py`, set the name of the table and columns that match your project:

```python
TABLE_NAME = "your_table_name"

COLUMNS = {
    "name": "VARCHAR(255)",
    "email": "VARCHAR(255)",
    "age": "INT"
}
```

Once configured, run the app:

```bash
streamlit run streamlit_app_local_mysql.py
```

Test the CRUD operations and transfer-age feature with your own MySQL database.

---

## 📬 For Educators

This template is meant for:
- Class projects
- Assignments with database components
- Lightweight app demos with local or remote DBs

---

⚠️ **Heads-up:** When deployed to Streamlit Cloud using SQLite, your data won’t persist between app restarts or redeploys (because it reloads the original file from GitHub).

✅ If you want to keep your data:
- Run the app locally
- Or connect it to a cloud-hosted database (like PlanetScale or MySQL)

---

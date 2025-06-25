🔧 Streamlit CRUD App (SQLite Version)

This is a simple, fully functional Streamlit web app for performing:
	•	CRUD operations (Create, Read, Update, Delete)
	•	A real-world SQL transaction: transferring values between rows using safe, rollback-enabled logic

It uses a SQLite database and is designed for educational use, ideal for learning database logic and deploying on Streamlit Community Cloud.

---

## 📦 Project Structure

```
.
├── app.py               # Main Streamlit app
├── config.py            # Database/table/column settings
├── requirements.txt     # For deployment
├── database.sqlite      # Sample SQLite database
```

---

## 🚀 Step-by-Step Guide (For Students)

### ✅ Step 1: Run the App Locally First

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
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

Explore the sample app with preloaded users (`Alice`, `Bob`, `Charlie`). Try adding, editing, deleting users, and transferring age.

---

### ☁️ Step 2: Deploy the Working Example to the Cloud

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
  - Transfer age between users (see Step 4)

---

### 🔍 Step 3: Explore the Sample App

Open your deployed app in the browser and try the following:

- Add a new user
- Edit an existing user's name or age
- Delete someone from the list
- Use **"Transfer Age Between Users"** to shift age values around

This gives you a feel for how the app works before using your own data.

---

### ⚙️ Step 4: Update Config for Your Own Table

When you're ready to use your own database:

1. Open `config.py` and update:
   - `DB_PATH` to your new `.sqlite` file name
   - `TABLE_NAME` to match your own table
   - `COLUMNS` with the field names (excluding `id`)

2. Replace `database.sqlite` with your exported version.

---

### 🔄 Step 5: Export Your MySQL DB to SQLite

Use a tool like DB Browser for SQLite, or try this approach:

```bash
# Export MySQL to SQL
mysqldump -u your_user -p your_db > dump.sql

# Convert SQL to SQLite (optional method)
pip install sqlite-utils
sqlite-utils convert dump.sql database.sqlite
```

Once your new `.sqlite` file is in place, commit the change to GitHub — your deployed app will automatically update.

---

### 🔁 Step 6: Test the "Transfer Age" Transaction

Once your app is running, scroll to the section titled:

> **"Transfer Age Between Users (Transactional)"**

#### What It Does:
- Transfers a specified number of "age years" from one user to another.
- Both updates occur in a **single transaction** — if anything fails, nothing is changed.

#### ✅ To Try It:
1. Select a user in the **"From (User ID)"** dropdown.
2. Select a different user in the **"To (User ID)"** dropdown.
3. Enter an age value to transfer (e.g. `2`).
4. Click **"Transfer Age"**.

#### ⚠️ Edge Cases:
- If the **"from" user** doesn’t have enough age, the transaction fails.
- Selecting the same user for both fields is prevented.
- Errors are displayed clearly, and the DB rolls back automatically.

---

## 📬 For Educators

This template is meant for:
- Class projects
- Assignments with database components
- Lightweight app demos with local DBs

Want more private app slots or memory on Streamlit Cloud? Contact: `support@streamlit.io`

---

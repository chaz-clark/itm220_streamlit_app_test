
import streamlit as st
import mysql.connector
from config import TABLE_NAME, COLUMNS

def get_connection():
    try:
        # Preferred: TCP connection (works in container & host if MySQL is listening on 0.0.0.0)
        conn = mysql.connector.connect(
            host="127.0.0.1",           # change to host's IP if running in a container
            port=3306,
            user="root",
            password="password",  # replace with your MySQL root password
            database="my_database"  # replace with your database name
        )
        return conn
    except mysql.connector.Error as e:
        st.error(f"Error connecting to MySQL: {e}")
        return None

def fetch_all():
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute(f"SELECT * FROM {TABLE_NAME}")
        return cur.fetchall()
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return []

def insert_row(data):
    try:
        conn = get_connection()
        cur = conn.cursor()
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {TABLE_NAME} ({', '.join(data.keys())}) VALUES ({placeholders})"
        cur.execute(query, list(data.values()))
        conn.commit()
    except Exception as e:
        st.error(f"Error inserting data: {e}")

def update_row(id_val, data):
    try:
        conn = get_connection()
        cur = conn.cursor()
        set_clause = ', '.join([f"{col}=%s" for col in data])
        query = f"UPDATE {TABLE_NAME} SET {set_clause} WHERE id = %s"
        cur.execute(query, list(data.values()) + [id_val])
        conn.commit()
    except Exception as e:
        st.error(f"Error updating data: {e}")

def delete_row(id_val):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(f"DELETE FROM {TABLE_NAME} WHERE id = %s", (id_val,))
        conn.commit()
    except Exception as e:
        st.error(f"Error deleting data: {e}")

st.title(f"CRUD App for '{TABLE_NAME}' Table")

rows = fetch_all()
st.subheader("Existing Records")
if not rows:
    st.warning("No records found. Please add some records first.")
else:
    st.dataframe(rows)

st.subheader("Add New Record")
with st.form("add_form"):
    new_data = {col: st.text_input(f"{col}") for col in COLUMNS}
    submitted = st.form_submit_button("Add")
    if submitted:
        insert_row(new_data)
        st.success("Record added!")

if rows:
    st.subheader("Update Existing Record")
    row_ids = [row['id'] for row in rows]
    selected_id = st.selectbox("Select ID to update", row_ids)
    selected_row = next((row for row in rows if row['id'] == selected_id), None)

    if selected_row:
        with st.form("update_form"):
            updated_data = {
                col: st.text_input(f"{col}", value=str(selected_row[col]))
                for col in COLUMNS
            }
            updated = st.form_submit_button("Update")
            if updated:
                update_row(selected_id, updated_data)
                st.success("Record updated!")

    st.subheader("Delete Record")
    delete_id = st.selectbox("Select ID to delete", row_ids, key="delete")
    if st.button("Delete"):
        delete_row(delete_id)
        st.warning("Record deleted.")

if not rows or len(rows) < 2:
    st.warning("Not enough records to perform a transfer. Please add more users.")
    st.stop()

st.subheader("Transfer Age Between Users (Transactional)")

name_id_map = {f"{row['name']} (ID {row['id']})": row['id'] for row in rows}
id_name_map = {row['id']: row['name'] for row in rows}
id_age_map = {row['id']: row['age'] for row in rows}

from_name = st.selectbox("From (User)", list(name_id_map.keys()), key="from_user")
to_name_options = [n for n in name_id_map.keys() if n != from_name]

if not to_name_options:
    st.warning("Not enough users to transfer age. Need at least 2 users.")
    st.stop()

to_name = st.selectbox("To (User)", to_name_options, key="to_user")

from_id = name_id_map.get(from_name)
to_id = name_id_map.get(to_name)

st.markdown(f"**{id_name_map[from_id]}'s current age:** {id_age_map[from_id]}")
st.markdown(f"**{id_name_map[to_id]}'s current age:** {id_age_map[to_id]}")

amount = st.number_input(
    "How many years to transfer (subtract from sender and add to recipient)",
    min_value=1,
    step=1,
)

if st.button("Transfer Age"):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(f"SELECT age FROM {TABLE_NAME} WHERE id = %s", (from_id,))
        from_age = cur.fetchone()[0]
        cur.execute(f"SELECT age FROM {TABLE_NAME} WHERE id = %s", (to_id,))
        to_age = cur.fetchone()[0]

        if from_age < amount:
            st.error("Not enough age to transfer!")
        else:
            cur.execute(
                f"UPDATE {TABLE_NAME} SET age = age - %s WHERE id = %s",
                (amount, from_id)
            )
            cur.execute(
                f"UPDATE {TABLE_NAME} SET age = age + %s WHERE id = %s",
                (amount, to_id)
            )
            conn.commit()
            st.success("Age transferred successfully!")
    except Exception as e:
        st.error(f"Transfer failed: {e}")

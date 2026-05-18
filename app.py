import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

st.title("🛒 Product Management System")

menu = [
    "Signup",
    "Login",
    "View Products",
    "Add Product",
    "Delete Product"
]

choice = st.sidebar.selectbox(
    "Menu",
    menu
)

# =========================
# SIGNUP
# =========================

# =========================
# SIGNUP
# =========================

if choice == "Signup":

    st.subheader("Create Account")

    username = st.text_input("Username")
    email = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Signup"):

        payload = {
            "username": username,
            "email": email,
            "password": password
        }

        response = requests.post(
            f"{BASE_URL}/signup",
            json=payload
        )

        try:
            st.json(response.json())

        except Exception:
            st.error("Backend Error")
            st.text(response.text)

# =========================
# LOGIN
# =========================

elif choice == "Login":
    
    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        payload = {
            "username": username,
            "password": password
        }

        response = requests.post(
            f"{BASE_URL}/login",
            json=payload
        )

        data = response.json()

        if response.status_code == 200:

            st.success("Login successful")

            st.session_state["token"] = data["access_token"]

        else:
            st.error(data["detail"])

# =========================
# VIEW PRODUCTS
# =========================

elif choice == "View Products":

    response = requests.get(
        f"{BASE_URL}/products/"
    )

    st.json(response.json())

# =========================
# ADD PRODUCT
# =========================

elif choice == "Add Product":

    token = st.session_state.get("token")

    if not token:
        st.warning("Please login first")

    else:

        name = st.text_input("Product Name")
        description = st.text_input("Description")
        price = st.number_input("Price")
        quantity = st.number_input("Quantity")

        if st.button("Add Product"):

            payload = {
                "name": name,
                "description": description,
                "price": price,
                "quantity": quantity
            }

            headers = {
                "Authorization": f"Bearer {token}"
            }

            response = requests.post(
                f"{BASE_URL}/products/",
                json=payload,
                headers=headers
            )

            st.json(response.json())

# =========================
# DELETE PRODUCT
# =========================

elif choice == "Delete Product":

    token = st.session_state.get("token")

    if not token:
        st.warning("Please login first")

    else:

        product_id = st.number_input(
            "Product ID",
            min_value=1
        )

        if st.button("Delete Product"):

            headers = {
                "Authorization": f"Bearer {token}"
            }

            response = requests.delete(
                f"{BASE_URL}/products/{product_id}",
                headers=headers
            )

            st.json(response.json())          

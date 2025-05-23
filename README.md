# 🚗 AutoFleetX – Online Car Rental System

AutoFleetX is a Django-based full-stack web application designed to manage car rentals online. It provides separate interfaces for **admin** and **authenticated users**, allows secure transactions, and supports dynamic rental pricing and rental history tracking. This project demonstrates robust use of **Python OOP principles**, Django's powerful **ORM**, and clean, user-friendly frontend design.

---

## 🧠 Project Highlights

- 🔐 **Custom Authentication System** with login/signup.
- 🧑‍💼 **Role-based views**: separate UI/UX for Admin and Normal Users.
- 💸 **Wallet System** for users to add money and pay for rentals.
- 🧾 **Rental History** with "Return Now" and "Returned Early" tracking.
- 📊 **Transaction History Page** for all payments and balance top-ups.
- 🧠 **Dynamic Rental Pricing**: live calculation shown on the UI using JavaScript.
- 🛠️ **Admin Restrictions**:
  - Cannot rent cars.
  - Cannot view Contact Us.
- 💬 **Contact Form** for users to submit queries (not visible to admin).
- 📅 **Rental Expiry Checker**: Cars are automatically marked available again if the rental period expires.
- 🧰 **Exception Handling**, **Abstract Classes**, **Composition**, **Inheritance**, and **OOP principles** implemented extensively.
- 🎨 Clean and responsive UI using custom CSS and modern Google Fonts.

---

## ⚙️ Technologies Used

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite
- **Auth**: Django's `AbstractUser` extended with custom fields
- **PDF Generation** (optional): `xhtml2pdf` (if needed)

---

## 🧾 Object-Oriented Features Implemented

- ✅ Inheritance (e.g., `CustomUser` from `AbstractUser`)
- ✅ Composition (e.g., `Rental` has `User` and `Car`)
- ✅ Abstract Class (e.g., `TimeStampedModel`)
- ✅ Method Overriding (`save()` in `Rental`)
- ✅ Exception Handling (`try-except` blocks in views)
- ✅ Operator Overloading (can be optionally shown in report)

---

## 🗂️ Project Structure

```
Car_Rental_System/
│
├── Car_Rental_System/       # Django project root
├── main_app/                # Main Django app with models, views, forms, urls
├── media/                   # Uploaded images (car images)
├── static/                  # Static assets like CSS, images to be uploaded to the website by the admin
├── templates/               # All HTML templates
│
├── db.sqlite3               # SQLite database
├── manage.py                # Django's project runner
├── requirements.txt         # All Python dependencies
├── README.md                # You're reading it
└── .gitignore               # Git ignore rules
```

---

## 🚀 Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/car-rental-system.git
   cd car-rental-system
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

7. **Visit the site**:
   ```
   http://127.0.0.1:8000/
   ```

---

## 🧪 Test Cases & Notes

- ✅ Form validation (e.g., rental duration > 0, numeric inputs)
- ✅ Access control based on user roles
- ✅ Transaction log after each rental/payment
- ✅ "Return Now" works only for active rentals
- ✅ Rental history shows "Returned Early" status if returned before `end_date`
- ✅ Cars become available after expiration via `check_returns()` logic

---

## 📃 License

This project is open source and free to use for learning and showcasing purposes. Contributions are welcome.

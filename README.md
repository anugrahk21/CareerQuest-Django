# 🚀 CareerQuest - Job Application Tracker

**CareerQuest** is a Django-based web application designed to help students track their job applications during placement season. It simplifies the process of managing application statuses, interview dates, and notes.

## ✨ Features

- **🔐 Secure Authentication**:
  - **Google OAuth Integration**: Login seamlessly with your Google account.
  - **Admin Login**: Manual login for superusers to access the admin panel.
  - **Session Management**: Protected routes ensuring only logged-in users access private data.

- **📝 Application Management**:
  - **Add Entries**: Record details like Company Name, Role, Package (CTC), Status (Applied, OA, Interview, etc.), and Notes.
  - **Dropdown Choices**: Standardized inputs for Job Type, Package Range, and Status.
  - **Date Tracking**: Keep track of when you applied or have an upcoming round.

- **🛡️ Admin Dashboard**:
  - Built-in Django Admin to manage users and view all application data efficiently.

## 🛠️ Tech Stack

- **Backend**: Django (Python)
- **Database**: SQLite (Default)
- **Authentication**: `social-auth-app-django` (Google OAuth2)
- **Frontend**: HTML5, CSS (In progress)

## 🚀 Getting Started

### Prerequisites
- Python 3.x
- Google Cloud Console Project (for OAuth credentials)

### Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/anugrahk21/CareerQuest-Django.git
    cd CareerQuest-Django
    ```

2.  **Create Virtual Environment**
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install django social-auth-app-django python-dotenv
    ```

4.  **Navigate to Project Folder**
    ```bash
    cd djangoproject
    ```

5.  **Configuration**
    *   Create a `.env.local` file inside the `djangoproject` folder.
    *   Add your credentials:
        ```env
        SOCIAL_AUTH_GOOGLE_OAUTH2_KEY='your-client-id'
        SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET='your-client-secret'
        SECRET_KEY='your-django-secret-key'
        ```

6.  **Run Migrations**
    ```bash
    python manage.py migrate
    ```

7.  **Create Superuser (Optional)**
    ```bash
    python manage.py createsuperuser
    ```

8.  **Run Server**
    ```bash
    python manage.py runserver
    ```

## 🔮 Future Roadmap

- [ ] **Dashboard View**: Visualize application stats (e.g., Pie chart of Accepted vs. Rejected).
- [ ] **Edit/Delete Functionality**: Update application status directly from the UI.
- [ ] **Email Notifications**: Get reminders for upcoming interviews.
- [ ] **Bootstrap UI**: Revamp the interface for a modern look.

## 🤝 Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.

## 📄 License
[MIT](https://choosealicense.com/licenses/mit/)

## 📞 Contact

Ready to discuss **Web Dev** or share **interview experiences**? Let's connect!

**Anugrah K.**  
*AI & Cybersecurity Enthusiast*  

📧 [Email](mailto:anugrah.k910@gmail.com)  
🔗 [GitHub Profile](https://github.com/anugrahk21)  
💼 [LinkedIn](https://linkedin.com/in/anugrah-k)
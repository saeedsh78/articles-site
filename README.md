
# Django Article Website

Welcome to the Django Article Website! This project is a simple web application built with Django, a high-level Python web framework, to manage and display articles. The website was developed based on the instructional content from the YouTube tutorial series available at this [link](https://www.youtube.com/playlist?list=PLAt10Vana3YeAwS_LyLCeu7chml8eP8bh).

![Static Badge](https://img.shields.io/badge/build-3.6%3E%3D-blue?logo=python&logoColor=yellow&label=python)
![Static Badge](https://img.shields.io/badge/build-4.2.7-brightgreen?logo=Django&logoColor=green&label=Django)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)



## Getting Started

1. Clone the Repository:

```bash
  git clone https://github.com/saeedsh78/articles-site
  cd articles-site
```

2. Create a Virtual Environment:

```bash
python -m venv venv
```

3. Activate the Virtual Environment:

- On Windows:

```bash
venv\Scripts\activate
```

- On macOS/Linux:

```bash
source venv/bin/activate
```
4. Install Dependencies:

```bash
pip install -r requirements.txt
```

5. Apply Migrations:

```bash
python manage.py migrate
```

6. Create a Superuser (Admin):

```bash
python manage.py createsuperuser
```

7. Run the Development Server:

```bash
python manage.py runserver
```
Visit http://127.0.0.1:8000/ in your browser to explore the website.

8. Admin Panel:
Access the Django admin panel at http://127.0.0.1:8000/admin/ using the superuser credentials.


## Features

- Article Management:
  - Create, edit, and delete articles through the custom admin panel.
- User Authentication:
  - Users can register, log in, and log out.
  - Reset Password: Allow users to reset their passwords through email verification
- User Interaction::
  - Comment System: Registered users can leave comments on articles.
  - Article Views: Track the number of views for each article, providing insights into article popularity.
- User Roles:
  - Identify Special Users: Designate certain users as "Special Users" with elevated privileges.



# Team-2570-ReWear-Community-Clothing-Exchange

Team Members:

1.M.Shashank Reddy  E-Mail:shashankreddy417@gmail.com

2.Kargaom Srishanth  E-Mail:kargaomsrishanth@gmail.com

3.Jagarla Srinivas   E-mail:srinivasjagarla73@gmail.com 

4.Laxmi Prasad     E-Mail:laxmiprasad20062003@gmail.com

A web-based clothing exchange platform that promotes sustainable fashion and reduces textile waste through a community-driven clothing exchange system.

## Features

- User Authentication (Register/Login)
- User Profiles with Points System
- Item Management (Upload, Browse, Swap)
- Point-based Redemption System
- Admin Dashboard for Content Moderation
- Responsive Design

## Tech Stack

- Frontend: HTML, CSS, JavaScript
- Backend: Python + Flask
- Database: MongoDB
- Authentication: Flask-Login
- Templating: Jinja2

## Setup Instructions

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
Create a `.env` file with:
```
MONGO_URI=your_mongodb_uri
SECRET_KEY=your_secret_key
```

3. Run the application:
```bash
python app.py
```

## Project Structure

```
reWear/
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── templates/
├── app.py
├── config.py
├── models/
├── routes/
└── utils/
```

# Team-2570-ReWear-Community-Clothing-Exchange

Team Members:

1.M.Shashank Reddy  E-Mail:shashankreddy417@gmail.com

2.Kargaom Srishanth  E-Mail:kargaomsrishanth@gmail.com

3.Jagarla Srinivas   E-mail:srinivasjagarla73@gmail.com 

4.Laxmi Prasad     E-Mail:laxmiprasad20062003@gmail.com

🚀 Overview: <br>
ReWear is a web-based clothing exchange platform that promotes sustainable fashion and reduces textile waste. Users can swap clothes directly or redeem them using earned points — all in a circular, community-driven environment.
🎯 Objective
Build a full-stack clothing exchange system with:

🧑‍🎨 Dynamic UI

🔐 Secure authentication

📊 User/Admin dashboards

🌱 Sustainable economy via swaps or point redemption<br>
Landing page:
![WhatsApp Image 2025-07-12 at 17 04 28_e4d64e11](https://github.com/user-attachments/assets/cf4c45db-57ab-440a-b336-81527ba87a91)
Register page:
![WhatsApp Image 2025-07-12 at 17 06 56_07a492dd](https://github.com/user-attachments/assets/0f2bc0e1-1000-48c4-a430-1b59721be097)
## Features
- User Authentication (Register/Login)
- User Profiles with Points System
- Item Management (Upload, Browse, Swap)
- Point-based Redemption System
- Admin Dashboard for Content Moderation
- Responsive Design
  
🧑 User Dashboard
User Profile:

Name, email, profile picture, location (optional)

Total points available

Swap Info:

Items listed by the user

Ongoing swaps

Completed swap history

Notifications (swap request, approval, redemption success)

<img width="1916" height="1132" alt="image" src="https://github.com/user-attachments/assets/dd668d43-e81e-4265-bb1f-7134c204a48d" />

👑 Admin Dashboard:
Login via secure credentials

Sections:

Item Approval:

View all pending listings

Accept/reject (e.g., inappropriate items, spam)

User Reports:

Swap activity logs

Points summary

Platform Control:

Delete users or items

Ban users violating policies

Send announcements

Moderation Tools:

Search and filter flagged content

Logs of actions taken
<img width="1918" height="1126" alt="image" src="https://github.com/user-attachments/assets/935192cb-dff4-49b8-8746-f8010df7c1aa" />

👕 Item Management
➕ Add New Item Page
Form Fields:

Title, Description, Category (e.g., Men/Women/Kids), Type (e.g., Jeans, Shirt), Size, Condition (New, Gently Used), Tags

Image Upload (multiple images allowed)

Form validation (JS + Flask)

On submission, stored in MongoDB under items collection

🔍 Browse Items Page
Card layout showing:
<img width="1914" height="1135" alt="image" src="https://github.com/user-attachments/assets/f067bf03-e325-4c8a-ab26-df51c5735fdf" />

Item photo, title, category, size

Option to view more or request a swap/redeem

Filters: Category, Size, Tags, Condition

📄 Item Detail Page
Full details about the clothing item

Image gallery (JavaScript-based)

User actions:

Swap Request

Redeem with points

Displays:
<img width="1917" height="1138" alt="image" src="https://github.com/user-attachments/assets/6d2359ee-613e-4027-8613-5cbf833dd64c" />

Uploader info

Item status (Available / Swapped)

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






# ☕ koffie-shop

## 📌 Setup Instructions

### 🔧 Fill Environment Files
Ensure all required environment files are present in `backend/env/` before proceeding.

### 📦 Install Dependencies
To install all necessary dependencies in a virtual environment, run:

```sh
py install.py
```

### 🔄 Migrate Database
Run database migrations using:

```sh
py migrate.py
```

### 🚀 Start the Project
To start the backend server, execute:

```sh
py run.py
```

## 📁 Git Ignore Environment Files
Prevent changes to sensitive environment files from being tracked:

```sh
git update-index --assume-unchanged backend/env/db.env
git update-index --assume-unchanged backend/env/settings.env
```

### 🔄 Restore Change Tracking
If you need to track changes again:

```sh
git update-index --no-assume-unchanged backend/env/db.env
git update-index --no-assume-unchanged backend/env/settings.env
```

## ✍️ Authors

- [IPOleksenko](https://github.com/IPOleksenko) (Owner)

## 📜 License

This project is licensed under the [MIT License](./LICENSE).

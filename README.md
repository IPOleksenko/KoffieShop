<table>
  <tr>
    <td><img src="frontend/src/logo.svg" width="256" alt="logo"></td>
        <td>
            <h1 style="font-size: 32px;">☕ KoffieShop</h1>
        </td>
  </tr>
</table>

## 📌 Setup Instructions

### 🔧 Fill Environment Files
Ensure that all required environment variables are present in both `env/backend.env` and `env/frontend.env` files before proceeding.

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
git update-index --assume-unchanged env/backend.env
git update-index --assume-unchanged env/frontend.env
```

### 🔄 Restore Change Tracking
If you need to track changes again:

```sh
git update-index --no-assume-unchanged env/backend.env
git update-index --no-assume-unchanged env/frontend.env
```

## ✍️ Authors

- [IPOleksenko](https://github.com/IPOleksenko) (Owner)

## 📜 License

This project is licensed under the [MIT License](./LICENSE).

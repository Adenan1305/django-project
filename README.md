# Noodle Shop

A Django restaurant ordering website with customer authentication, member points and rewards, order management, and natural-language menu assistance through OpenRouter.

## Features

- Register with an email address, sign in, and sign out through the website UI.
- Browse the menu and place orders as a guest or signed-in customer.
- Earn and redeem points as an authenticated member.
- Restrict the administration site and management actions to Django staff and superuser accounts.
- Ask the AI assistant to interpret a food request from the server-side menu catalog.
- Review the cart before the server validates prices and stores an order.

## Requirements

- Python 3.12 or newer
- Packages listed in `requirements.txt`
- An OpenRouter API key for AI ordering (optional for the rest of the site)

## Run locally

From the repository root, create and activate a virtual environment, then install the dependencies:

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

Set environment variables before starting the project. Generate a local Django secret key rather than using the development fallback for a deployed site:

```powershell
$env:DJANGO_SECRET_KEY = "replace-with-a-long-random-secret"
$env:OPENROUTER_API_KEY = "your-openrouter-api-key"
```

Apply database migrations, create an administrator account, and start the development server:

```bash
cd myproject
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/`. Customer registration and sign-in are available at `/register/` and `/signin/`. The staff administration site is at `/admin/`.

## Authentication and authorization

The site uses Django's built-in user model and session authentication. Customer registration creates an account and signs the customer in. A signed-in customer can access the points and rewards features. Guests can browse and submit standard orders, while reward redemption requires an authenticated account. Django Admin is restricted to authorized staff; create the first staff administrator with `createsuperuser`.

## AI ordering API

The browser sends a CSRF-protected JSON `POST` request to `/api/ai-order/`. The Django view checks the request and message, calls the OpenRouter chat completions API with the configured server-side key, and validates product IDs, quantities, noodle choices, and egg options against the server catalog. Missing AI configuration disables this feature without preventing the rest of the website from running.

## Run the test suite

```bash
cd myproject
python manage.py test
```

## Submission materials

- **GitHub repository:** [Adenan1305/django-project](https://github.com/Adenan1305/django-project)
- **Presentation slides:** [Download the PowerPoint deck](submission/Noodle_Shop_Presentation_Slides.pptx)
- **Presentation slides PDF:** [Download the PDF](submission/Noodle_Shop_Presentation_Slides.pdf)
- **Article report:** [Download the English report](submission/Article_Report_English.docx)

The `submission/` folder contains the requested presentation and report. The application source remains in `myproject/`.

## Security notes

- Do not commit `.env` files, API keys, production secret keys, local databases, or virtual environments.
- Set a unique `DJANGO_SECRET_KEY`, `DEBUG=False`, and suitable `ALLOWED_HOSTS` for deployment.
- Configure `OPENROUTER_API_KEY` only in the server environment.

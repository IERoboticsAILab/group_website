# CyPhy Life — Group Website

Django site for the CyPhy Life lab at the [IE School of Science and Technology](https://www.ie.edu/school-science-technology/).
Everything on the public site — people, research lines, projects, publications, job openings, contact
details — is edited through the Django admin, so no code changes are needed to update content.

**The whole site lives in this repository** — code, images, and the SQLite database with all the content
in it. Cloning gives you the real, fully populated site; see [Everything lives in the repo](#everything-lives-in-the-repo).

## Stack

- **Django 5.2** on Python 3.11+ (SQLite database)
- **[django-filer](https://django-filer.readthedocs.io/)** + easy-thumbnails for image management
- **[django-prose](https://github.com/withlogicco/django-prose)** for rich-text fields, **markdown2** for Markdown fields
- **Bootstrap 5.3** (CDN) with custom CSS/JS in `static/`

## Quick start

### Local (virtualenv)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python manage.py migrate          # usually "No migrations to apply" — the committed db is current
python manage.py runserver
```

Site: http://127.0.0.1:8000/ · Admin: http://127.0.0.1:8000/admin/

No database setup or content import is needed — `db.sqlite3` and `media/` come with the clone. To edit
content you need an admin login; several already exist in the committed database, and
[Admin accounts](#admin-accounts) covers creating your own.

### Docker

```bash
docker compose up --build
```

Site: http://localhost:8080/. The compose file bind-mounts the project directory and `db.sqlite3`,
so edits and content changes persist on the host and are ready to commit. Run management commands with
`docker compose exec web python manage.py <command>`.

## Project layout

```
group_website/       Django project settings, root URLconf, WSGI/ASGI entrypoints
core/                The single app: models, views, admin, URLs
  templatetags/      markdown2safe filter used to render Markdown fields
  context_processors Injects social media links into every template
templates/           base.html + core/ page templates and partials
static/              CSS, JS, logos, favicon
media/               Uploaded images (filer_public/, members/, projects/, banner/, ...)
db.sqlite3           The database — committed to the repo, with all site content in it
```

## Pages and routes

| URL | View | Template |
| --- | --- | --- |
| `/` | `home` | `core/home.html` |
| `/people/` | `people` | `core/people.html` |
| `/projects/` | `projects` | `core/projects.html` |
| `/projects/<slug>/` | `project_detail` | `core/project_detail.html` |
| `/research-line/<slug>/` | `research_line_detail` | `core/research_line_detail.html` |
| `/publications/` | `publications` | `core/publications.html` |
| `/contact/` | `contact` | `core/contact.html` |
| `/admin/` | Django admin | — |

## Content model

All models live in `core/models.py` and are registered in the admin.

**Singletons** (the admin allows exactly one instance and jumps straight to its edit page):

- `HomeContent` — headline, subheadline, two Markdown sections, a section image, and a YouTube embed URL.
- `LabInfo` — department, building, room, institution, address, email, phone, Google Maps embed URL. Shown on the contact page.
- `SocialMedia` — GitHub and YouTube links; rendered in the navbar on every page via a context processor.

**Repeatable content:**

- `ResearchLine` — long-running research areas. Rich-text `content`, banner image, video URL, inline gallery images (`ResearchLineGalleryImage`), and many-to-many links to team members, publications, and projects.
- `ResearchProject` — individual projects. Same shape as a research line, with its own gallery inline (`ProjectGalleryImage`).
- `TeamMember` — name, position, email, and GitHub/LinkedIn/personal-site links. Flags: `principal_investigator` (listed first on the people page) and `alum` (moved to the alumni section, with optional `alum_destination` and `alum_destination_link` showing where they went next).
- `Publication` — title, authors, abstract, date, and optional paper/PDF/code/website links.
- `JobPosition` — open positions listed on the contact page, newest first.

### Notes on behaviour

- **Slugs** are auto-generated from the title on first save for research lines and projects; the admin also
  prepopulates the field. Changing a title later does *not* change an existing slug, so permalinks stay stable.
- **`active`** on research lines and projects controls visibility. Unchecking it hides the item from the site
  without deleting it.
- The **home page carousel** merges active projects and research lines (up to 3 of each), sorts them by date
  newest-first, keeps the top 6, and groups them into rows of 3. The **projects page** shows all active items
  from both models in one date-sorted list.
- Markdown fields are rendered with the `markdown2safe` template filter (`core/templatetags/markdown_extras.py`),
  which marks output as safe — treat those fields as trusted, admin-only input.

## Everything lives in the repo

This repository is not just the code — it is the **entire running site**. Of the 954 tracked files,
878 are uploaded images. A clone gives you the complete, working website with all of its content:

| Tracked in git | What it holds |
| --- | --- |
| `db.sqlite3` (~1.1 MB) | The whole database: every person, project, research line, publication and job posting, plus admin user accounts and sessions |
| `media/` (~318 MB) | Every uploaded image — `filer_public/` (django-filer originals and thumbnails), `members/`, `projects/`, `banner/`, `home_sections/`, `prose/` |
| `core/migrations/` (28 files) | The full schema history |
| `static/`, `templates/`, `core/`, `group_website/` | Code, styles, logos, page templates |

Only `venv/`, `__pycache__/`, `.env*`, and editor folders are ignored (see `.gitignore`).

**What this means in practice:**

- There is no separate content database or media server to set up. Clone, install dependencies, `runserver` — you have the real site with the real content.
- **Editing content in the admin is a code change.** Adding a publication or swapping a photo modifies `db.sqlite3` and `media/`, and those changes must be committed and pushed or they exist only on your machine.
- `git pull` overwrites your local content with whatever is on the remote. Commit or stash before pulling.
- `db.sqlite3` is binary, so **git cannot merge it**. If two people edit content at the same time, one side's work has to be redone by hand. Coordinate: pull first, make your edits, commit and push promptly.
- The repo grows with every image. Media files are stored in full each time one changes, so prefer resizing large images before uploading.

### Committing content changes

```bash
git pull                          # start from the latest content
python manage.py runserver        # edit at http://127.0.0.1:8000/admin/
git status                        # db.sqlite3 and any new media/ files show as modified
git add db.sqlite3 media/
git commit -m "Add 2026 publications and update team photos"
git push
```

## Database and migrations

Because `db.sqlite3` is committed with all migrations already applied, a fresh clone normally needs
nothing — `migrate` will report "No migrations to apply." You only run these commands when the
**schema** changes, i.e. when you edit `core/models.py`.

### The two commands

```bash
python manage.py makemigrations   # writes a new file in core/migrations/ describing your model changes
python manage.py migrate          # applies pending migrations to db.sqlite3
```

`makemigrations` only creates the migration file; nothing touches the database until `migrate` runs.
Both the new migration file **and** the updated `db.sqlite3` must be committed together, or other
people's databases will fall out of sync with the code.

```bash
git add core/migrations/ db.sqlite3
git commit -m "Add funding field to ResearchProject"
```

### Useful variants

```bash
python manage.py makemigrations core                # limit to the core app
python manage.py makemigrations core --name add_funding_field   # give the file a readable name
python manage.py makemigrations --dry-run           # show what would be generated, write nothing
python manage.py makemigrations --check --dry-run   # exit non-zero if models and migrations disagree
python manage.py showmigrations                     # list migrations, [X] = applied
python manage.py sqlmigrate core 0027               # print the SQL a migration will run
python manage.py migrate core 0026                  # roll back to migration 0026 (reversible ones only)
python manage.py migrate --fake core 0027           # mark as applied without running it (rare, last resort)
```

### If a model change adds a required field

Django will ask for a default for existing rows. Either give the field `null=True`, `blank=True`, or a
`default=`, or supply a one-off value when prompted. Answering that prompt is normal — it is not an error.

### Inside Docker

```bash
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
```

The project directory is bind-mounted, so migration files and the updated database land on your host
and are ready to commit.

## Admin accounts

The admin at `/admin/` is the only way content is edited, so you need an account. The committed
database already contains **six superuser accounts** (`cgomez`, `edu`, `laura`, `milan`, `zaidalsaheb`,
`zaido`) — if one of those is yours, just log in and skip this section.

### Creating a superuser

```bash
python manage.py createsuperuser
```

It prompts for a username, an optional email, and a password (typed twice, hidden). Short or common
passwords trigger a warning that you can override with `y`. Non-interactively:

```bash
DJANGO_SUPERUSER_PASSWORD='choose-a-strong-one' \
  python manage.py createsuperuser --noinput --username alice --email alice@example.com
```

Inside Docker, add `-it` so the prompts work:

```bash
docker compose exec -it web python manage.py createsuperuser
```

### Changing or resetting a password

```bash
python manage.py changepassword zaidalsaheb
```

There is no email-based password reset configured, so a forgotten password is fixed with this command
by anyone who can run it against the database.

### Two things to know about accounts here

- **Accounts are stored in the committed `db.sqlite3`.** Creating a user is a change to a tracked file:
  commit it and every collaborator gets the account; skip the commit and the account exists only for you.
- Django stores passwords hashed, not in plaintext, but those hashes are in the repository and in its
  history. Treat admin passwords as shared-repository secrets — use one that is not reused elsewhere,
  and do not push this repo to a public remote without rotating them.

### Other user management

```bash
python manage.py shell -c "from django.contrib.auth.models import User; print(User.objects.values_list('username', 'is_superuser'))"
```

Users can otherwise be added, deactivated, or given limited permissions from the **Authentication and
Authorization** section of the admin itself.

## Before deploying

`group_website/settings.py` is still the development configuration generated by `startproject`:

- `DEBUG = True`
- `SECRET_KEY` is the hardcoded `django-insecure-...` value committed to the repo
- `ALLOWED_HOSTS = ['*']`
- Static and media files are served by Django itself (only active while `DEBUG` is on)

A real deployment needs `DEBUG = False`, a secret key read from the environment, a concrete `ALLOWED_HOSTS`,
`collectstatic` behind a proper static file server, and a WSGI server instead of `runserver` — the Dockerfile
currently runs the development server on port 8080.

## Development

```bash
python manage.py check      # Django system checks
python manage.py test       # test runner (core/tests.py is currently empty)
```

`requirements.txt` includes `pylint`, `mypy`, `django-stubs`, and `isort` if you want linting or type checks.

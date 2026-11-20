from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .models import ContactMessage

# ---------- EDIT YOUR CONTENT HERE ----------
PROFILE = {
    "cgpa": "8.65",
    "photo": "",  # e.g. "img/profile.jpg" (file in login/static/img/). Empty = "SM" placeholder
    "resume": "resume/Saravanan_M_Resume.pdf",  # file in login/static/resume/
}

SOCIAL = [
    {"name": "LinkedIn", "icon": "li", "url": "", "desc": "Professional profile and experience"},
    {"name": "GitHub", "icon": "gh", "url": "", "desc": "Source code and open projects"},
    {"name": "Instagram", "icon": "ig", "url": "", "desc": "Updates and behind the scenes"},
    {"name": "Email", "icon": "ml", "url": "mailto:saravanan.m.cse.dev@gmail.com",
     "desc": "saravanan.m.cse.dev@gmail.com"},
]

SKILLS = [
    ("Programming Languages", ["Python", "Java", "JavaScript", "SQL", "Kotlin"]),
    ("Frameworks & Technologies", ["Django", "React", "Next.js", "Node.js", "Jetpack Compose", "Android SDK"]),
    ("Backend & APIs", ["REST API Design", "Firebase Cloud Messaging", "Webhooks", "Razorpay Payment Gateway"]),
    ("Databases", ["Supabase", "PostgreSQL", "Firebase Realtime Database", "Firestore"]),
    ("AI / ML", ["OpenAI API Integration", "NLP-based Incident Classification", "Prompt Engineering"]),
    ("Tools", ["Git", "GitHub", "Firebase", "VS Code", "Android Studio"]),
]

# Add a project by appending a dict. Leave github/demo "" until real URLs exist.
PROJECTS = [
    {
        "title": "CYCLEO – Micro-Mobility & Community Platform",
        "desc": "An Android micro-mobility platform combining bicycle sharing, social connectivity and real-time ride analytics.",
        "tech": ["Kotlin", "Jetpack Compose", "Supabase", "Firebase", "Razorpay", "OpenStreetMap"],
        "features": ["Real-time bicycle availability", "OpenStreetMap integration",
                     "Dynamic pricing and battery-level visualization", "QR-based peer discovery",
                     "Social connectivity", "Secure payment integration", "GPS tracking",
                     "CO₂ savings and calorie analytics"],
        "github": "", "demo": "",
    },
    {
        "title": "CRISISSYNC AI – Real-Time Emergency Coordination Platform",
        "desc": "An AI-powered emergency coordination platform designed to improve incident reporting, classification and response management.",
        "tech": ["Python", "Next.js", "Supabase", "OpenAI API", "Firebase Cloud Messaging"],
        "features": ["Guest, Staff and Administrator roles", "Real-time incident synchronization",
                     "AI-based incident classification", "Severity-based emergency routing",
                     "AI-generated evacuation plans", "Real-time push notifications"],
        "github": "", "demo": "",
    },
]

ACHIEVEMENTS = [
    {"rank": "Top 15", "event": "Atria University Hackathon", "project": "CrisisSync AI"},
    {"rank": "Top 9", "event": "QuantumHacks", "project": "CrisisSync AI"},
    {"rank": "Top 5", "event": "College Mini-Project Exhibition", "project": "CYCLEO"},
]

CERTIFICATIONS = [  # "url": "" until you have the real certificate link
    {"title": "Data Structures and Algorithms: The Complete Masterclass", "issuer": "UC San Diego", "url": ""},
    {"title": "Algorithmic Toolbox & Advanced Algorithms", "issuer": "UC San Diego", "url": ""},
    {"title": "Database Management Systems & Introduction to Databases", "issuer": "Meta / Clemson University", "url": ""},
    {"title": "Hardware and Operating System Foundations", "issuer": "Illinois Institute of Technology", "url": ""},
    {"title": "Java Programming for Beginners", "issuer": "IBM", "url": ""},
    {"title": "Introduction to Computing Systems", "issuer": "BITS Pilani", "url": ""},
]
# --------------------------------------------


def _render(request, form=None, errors=None, status=200):
    ctx = {
        "profile": PROFILE, "social": SOCIAL, "skills": SKILLS, "projects": PROJECTS,
        "achievements": ACHIEVEMENTS, "certifications": CERTIFICATIONS,
        "form": form or {}, "errors": errors or {},
    }
    return render(request, "login.html", ctx, status=status)


def home(request):
    return _render(request)


@require_POST
def contact(request):
    data = {k: request.POST.get(k, "").strip() for k in ("name", "email", "subject", "message")}
    errors = {}

    if request.POST.get("website"):  # honeypot: bots fill this hidden field
        return redirect("home")
    if not 2 <= len(data["name"]) <= 100:
        errors["name"] = "Enter your name (2–100 characters)."
    try:
        validate_email(data["email"])
    except ValidationError:
        errors["email"] = "Enter a valid email address."
    if not 3 <= len(data["subject"]) <= 150:
        errors["subject"] = "Enter a subject (3–150 characters)."
    if not 10 <= len(data["message"]) <= 2000:
        errors["message"] = "Write a message of 10–2000 characters."

    if errors:
        return _render(request, data, errors, status=400)

    ContactMessage.objects.create(**data)
    try:
        send_mail(
            f"[Portfolio] {data['subject']}",
            f"From: {data['name']} <{data['email']}>\n\n{data['message']}",
            getattr(settings, "DEFAULT_FROM_EMAIL", None),
            [getattr(settings, "CONTACT_RECEIVER", "saravanan.m.cse.dev@gmail.com")],
            fail_silently=False,
        )
    except Exception:
        pass  # message is already saved in the database; view it in /admin
    messages.success(request, "Thanks! Your message has been sent. I'll reply soon.")
    return redirect("/#contact")

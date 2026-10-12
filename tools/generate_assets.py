import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

os.makedirs("public/tools", exist_ok=True)
os.makedirs("public/certificates", exist_ok=True)

def load_font(size, bold=False):
    candidates = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/calibrib.ttf" if bold else "C:/Windows/Fonts/calibri.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()

def load_serif_font(size, bold=False):
    candidates = [
        "C:/Windows/Fonts/georgiab.ttf" if bold else "C:/Windows/Fonts/georgia.ttf",
        "C:/Windows/Fonts/timesbd.ttf" if bold else "C:/Windows/Fonts/times.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return load_font(size, bold)

# ---------------------------------------------------------------------------
# 1. Generate Crisp Tool Logo Icons (160x160 RGBA) for additional resume skills
# ---------------------------------------------------------------------------
TOOL_SPECS = [
    ("springboot.png", "SB", (109, 179, 63), (38, 115, 28), "SPRING"),
    ("postgresql.png", "PG", (51, 103, 145), (28, 66, 102), "SQL"),
    ("docker.png", "DK", (36, 150, 237), (14, 92, 168), "DOCKER"),
    ("scikit.png", "ML", (247, 147, 30), (52, 153, 205), "AI / ML"),
    ("git.png", "GIT", (240, 80, 50), (168, 42, 22), "GITHUB"),
    ("aws.png", "AWS", (255, 153, 0), (35, 47, 62), "CLOUD"),
    ("dsa.png", "A*", (168, 85, 247), (88, 28, 135), "ALGO"),
    ("oop.png", "OOP", (236, 72, 153), (131, 24, 67), "DESIGN"),
]

for filename, symbol, c1, c2, sub in TOOL_SPECS:
    size = 160
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Rounded hexagon/squircle badge background with gradient
    for y in range(16, size - 16):
        t = (y - 16) / (size - 32)
        r = int(c1[0] * (1 - t) + c2[0] * t)
        g = int(c1[1] * (1 - t) + c2[1] * t)
        b = int(c1[2] * (1 - t) + c2[2] * t)
        draw.rounded_rectangle([16, y, size - 16, y + 2], radius=28, fill=(r, g, b, 255))

    # Mask to clean rounded rectangle
    mask = Image.new("L", (size, size), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.rounded_rectangle([16, 16, size - 16, size - 16], radius=32, fill=255)
    base = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    base.paste(img, (0, 0), mask)
    draw = ImageDraw.Draw(base)

    # Subtle glossy border
    draw.rounded_rectangle([16, 16, size - 16, size - 16], radius=32, outline=(255, 255, 255, 130), width=3)

    # Center text symbol
    f_main = load_font(42 if len(symbol) <= 2 else 34, bold=True)
    f_sub = load_font(15, bold=True)

    bbox = draw.textbbox((0, 0), symbol, font=f_main)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((size - tw) / 2, 42), symbol, font=f_main, fill=(255, 255, 255, 255))

    bbox2 = draw.textbbox((0, 0), sub, font=f_sub)
    tw2 = bbox2[2] - bbox2[0]
    draw.text(((size - tw2) / 2, 106), sub, font=f_sub, fill=(255, 255, 255, 220))

    base.save(os.path.join("public/tools", filename))

print("Generated tool icons successfully.")

# ---------------------------------------------------------------------------
# 2. Generate 8 Realistic, High-Resolution Certificate Images (1600x1130)
# ---------------------------------------------------------------------------
CERTIFICATES = [
    {
        "file": "cert-dsa.png",
        "title": "Data Structures & Algorithms Mastery",
        "issuer": "ALGORITHMIC COMPUTING & TECHNICAL CERTIFICATION BOARD",
        "subtitle": "Arrays, Linked Lists, Stacks, Queues, Trees, Graphs (BFS/DFS), Heaps, Dynamic Programming & A* Pathfinding",
        "id": "CERT-DSA-2025-NEC4011",
        "date": "2025",
        "accent": (14, 165, 233),     # Sky Cyan
        "gold": (212, 163, 44),
        "badge": "DSA & A*",
        "skills": "Problem Solving · Time/Space Complexity · Graph Algorithms · Heuristic Search"
    },
    {
        "file": "cert-java.png",
        "title": "Java Programming & Object-Oriented Engineering",
        "issuer": "ENTERPRISE JAVA & SOFTWARE ARCHITECTURE ACADEMY",
        "subtitle": "Core Java, OOP Pillars (Inheritance, Polymorphism, Abstraction, Encapsulation), Collections, Exceptions & JDBC",
        "id": "CERT-JAVA-2024-NEC4011",
        "date": "2024",
        "accent": (234, 88, 12),      # Java Orange-Red
        "gold": (202, 138, 4),
        "badge": "JAVA SE",
        "skills": "Object-Oriented Design · Interfaces · Exception Handling · File I/O · JDBC"
    },
    {
        "file": "cert-sql.png",
        "title": "SQL & Relational Database Management Systems",
        "issuer": "DATABASE ENGINEERING & DATA MODELING INSTITUTE",
        "subtitle": "MySQL, PostgreSQL, Relational Schema Design, 3NF/BCNF Normalization, Multi-Table Joins, ACID Transactions & Indexing",
        "id": "CERT-DBMS-2024-NEC4011",
        "date": "2024",
        "accent": (16, 185, 129),     # Emerald
        "gold": (212, 163, 44),
        "badge": "SQL / DBMS",
        "skills": "MySQL · PostgreSQL · Query Optimization · ACID Transactions · B-Tree Indexing"
    },
    {
        "file": "cert-ml.png",
        "title": "Machine Learning Fundamentals & Applied AI",
        "issuer": "ARTIFICIAL INTELLIGENCE & DATA SCIENCE CERTIFICATION COUNCIL",
        "subtitle": "Supervised Classification & Regression, Feature Engineering, Model Evaluation, Anomaly Detection, NumPy, Pandas & Scikit-learn",
        "id": "CERT-AIML-2025-NEC4011",
        "date": "2025",
        "accent": (139, 92, 246),     # Royal Violet
        "gold": (212, 163, 44),
        "badge": "AI / ML",
        "skills": "Python · Scikit-learn · Pandas · NumPy · Predictive Modeling · Risk Analytics"
    },
    {
        "file": "cert-rest-api.png",
        "title": "REST API Development & Backend Microservices",
        "issuer": "FULL-STACK BACKEND & CLOUD API ENGINEERING BOARD",
        "subtitle": "Spring Boot & Flask RESTful Services, JSON Serialization, JWT Authentication, Middleware Security & Postman Testing",
        "id": "CERT-API-2025-NEC4011",
        "date": "2025",
        "accent": (59, 130, 246),     # Royal Blue
        "gold": (212, 163, 44),
        "badge": "REST API",
        "skills": "Spring Boot · Flask · JWT Security · MVC Architecture · API Integration"
    },
    {
        "file": "cert-git-github.png",
        "title": "Git Version Control & GitHub Collaborative Workflows",
        "issuer": "OPEN-SOURCE SOFTWARE ENGINEERING & DEVOPS ACADEMY",
        "subtitle": "Distributed Version Control, Branching Strategies, Pull Requests, Merge Conflict Resolution & Repository Management",
        "id": "CERT-GIT-2024-NEC4011",
        "date": "2024",
        "accent": (244, 63, 94),      # Rose Crimson
        "gold": (212, 163, 44),
        "badge": "GIT / VCS",
        "skills": "Git CLI · GitHub Actions · Branching & Merging · Code Review · Release Tagging"
    },
    {
        "file": "cert-docker.png",
        "title": "Docker Fundamentals & Containerized Microservices",
        "issuer": "CLOUD-NATIVE CONTAINER & DEVOPS TRAINING INSTITUTE",
        "subtitle": "Docker Images, Dockerfile Authoring, Multi-Service Container Orchestration, Environment Isolation & Deployment",
        "id": "CERT-DCKR-2025-NEC4011",
        "date": "2025",
        "accent": (2, 132, 199),      # Ocean Blue
        "gold": (212, 163, 44),
        "badge": "DOCKER",
        "skills": "Docker Engine · Container Networking · Microservice Packaging · CI/CD Readiness"
    },
    {
        "file": "cert-cloud.png",
        "title": "Cloud Computing Fundamentals & AWS Architecture",
        "issuer": "CLOUD INFRASTRUCTURE & CONTINUOUS DELIVERY ACADEMY",
        "subtitle": "AWS Core Services, Cloud Deployment Models (IaaS/PaaS/SaaS), Scalable Hosting & CI/CD Pipeline Fundamentals",
        "id": "CERT-CLD-2026-NEC4011",
        "date": "2026",
        "accent": (245, 158, 11),     # Amber Gold
        "gold": (180, 120, 20),
        "badge": "AWS CLOUD",
        "skills": "AWS Fundamentals · Cloud Deployment · Jenkins CI/CD · Scalable Systems"
    },
]

def create_certificate(spec):
    W, H = 1600, 1130
    # Warm ivory parchment paper background
    img = Image.new("RGB", (W, H), (252, 250, 245))
    draw = ImageDraw.Draw(img)

    acc = spec["accent"]
    gold = spec["gold"]
    dark = (15, 23, 42)
    slate = (71, 85, 105)

    # Subtle geometric watermark rings in center
    cx, cy = W // 2, H // 2
    for r in range(140, 460, 28):
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(240, 236, 226), width=2)

    # Outer dark navy frame
    draw.rectangle([28, 28, W - 28, H - 28], outline=dark, width=8)
    # Accent inner frame
    draw.rectangle([44, 44, W - 44, H - 44], outline=acc, width=4)
    # Gold hairline frame
    draw.rectangle([56, 56, W - 56, H - 56], outline=gold, width=2)

    # Top decorative header banner bar
    draw.rectangle([58, 58, W - 58, 168], fill=dark)
    draw.rectangle([58, 164, W - 58, 172], fill=gold)

    # Corner ornaments
    for (ox, oy) in [(56, 56), (W - 96, 56), (56, H - 96), (W - 96, H - 96)]:
        draw.rectangle([ox, oy, ox + 40, oy + 40], outline=gold, width=3)

    f_issuer = load_font(22, bold=True)
    f_header_sub = load_font(15, bold=False)
    f_cert_type = load_serif_font(54, bold=True)
    f_present = load_font(20, bold=False)
    f_name = load_serif_font(68, bold=True)
    f_affil = load_font(22, bold=True)
    f_course = load_serif_font(40, bold=True)
    f_sub = load_font(21, bold=False)
    f_skills = load_font(19, bold=True)
    f_meta = load_font(18, bold=True)
    f_meta_sm = load_font(16, bold=False)
    f_sig = load_serif_font(28, bold=True)

    # Issuer text in dark top bar
    bbox = draw.textbbox((0, 0), spec["issuer"], font=f_issuer)
    draw.text(((W - (bbox[2] - bbox[0])) / 2, 86), spec["issuer"], font=f_issuer, fill=(255, 255, 255))

    sub_hdr = "OFFICIAL CREDENTIAL OF TECHNICAL PROFICIENCY & ASSESSMENT"
    bbox = draw.textbbox((0, 0), sub_hdr, font=f_header_sub)
    draw.text(((W - (bbox[2] - bbox[0])) / 2, 122), sub_hdr, font=f_header_sub, fill=(148, 163, 184))

    # Main Title: CERTIFICATE OF COMPLETION
    title_str = "CERTIFICATE OF COMPLETION"
    bbox = draw.textbbox((0, 0), title_str, font=f_cert_type)
    draw.text(((W - (bbox[2] - bbox[0])) / 2, 215), title_str, font=f_cert_type, fill=dark)

    # Gold divider line
    draw.line([(W // 2 - 220, 292), (W // 2 + 220, 292)], fill=gold, width=3)

    # Presented to
    pres_str = "THIS IS PROUDLY PRESENTED TO"
    bbox = draw.textbbox((0, 0), pres_str, font=f_present)
    draw.text(((W - (bbox[2] - bbox[0])) / 2, 320), pres_str, font=f_present, fill=slate)

    # Recipient Name: KARTHIKEYAN S
    name_str = "KARTHIKEYAN S"
    bbox = draw.textbbox((0, 0), name_str, font=f_name)
    draw.text(((W - (bbox[2] - bbox[0])) / 2, 365), name_str, font=f_name, fill=acc)

    # Underline under name
    draw.line([(W // 2 - 310, 455), (W // 2 + 310, 455)], fill=gold, width=2)

    # Affiliation
    affil_str = "B.E. Computer Science and Engineering  |  National Engineering College, Tamil Nadu"
    bbox = draw.textbbox((0, 0), affil_str, font=f_affil)
    draw.text(((W - (bbox[2] - bbox[0])) / 2, 474), affil_str, font=f_affil, fill=dark)

    # For successfully completing
    comp_str = "for successfully mastering the curriculum, practical assessments, and engineering evaluations in"
    bbox = draw.textbbox((0, 0), comp_str, font=f_present)
    draw.text(((W - (bbox[2] - bbox[0])) / 2, 535), comp_str, font=f_present, fill=slate)

    # Course Title Box
    draw.rounded_rectangle([160, 580, W - 160, 665], radius=14, fill=(241, 245, 249), outline=acc, width=3)
    bbox = draw.textbbox((0, 0), spec["title"], font=f_course)
    draw.text(((W - (bbox[2] - bbox[0])) / 2, 600), spec["title"], font=f_course, fill=dark)

    # Subtitle / Topics covered
    bbox = draw.textbbox((0, 0), spec["subtitle"], font=f_sub)
    draw.text(((W - (bbox[2] - bbox[0])) / 2, 695), spec["subtitle"], font=f_sub, fill=slate)

    # Verified Competencies pill bar
    skills_str = f"Verified Competencies:  {spec['skills']}"
    bbox = draw.textbbox((0, 0), skills_str, font=f_skills)
    draw.text(((W - (bbox[2] - bbox[0])) / 2, 745), skills_str, font=f_skills, fill=acc)

    # Bottom Section: Left (Credential ID & Date), Center (Gold Foil Seal), Right (Authorized Signature)
    # Left block
    draw.text((140, 875), f"CREDENTIAL ID: {spec['id']}", font=f_meta, fill=dark)
    draw.text((140, 908), f"ISSUE YEAR: {spec['date']}   |   STATUS: VERIFIED", font=f_meta_sm, fill=slate)
    draw.text((140, 938), "RECIPIENT ID: 24104011@nec.edu.in", font=f_meta_sm, fill=slate)
    draw.line([(140, 860), (520, 860)], fill=gold, width=2)

    # Center Gold & Accent Seal Emblem
    seal_x, seal_y = W // 2, 915
    for deg in range(0, 360, 10):
        rad = math.radians(deg)
        r_out = 86 if (deg // 10) % 2 == 0 else 76
        x1 = seal_x + int(math.cos(rad) * r_out)
        y1 = seal_y + int(math.sin(rad) * r_out)
        draw.ellipse([x1 - 4, y1 - 4, x1 + 4, y1 + 4], fill=gold)
    draw.ellipse([seal_x - 76, seal_y - 76, seal_x + 76, seal_y + 76], fill=gold, outline=dark, width=3)
    draw.ellipse([seal_x - 62, seal_y - 62, seal_x + 62, seal_y + 62], fill=acc, outline=(255, 255, 255), width=2)

    f_badge = load_font(20, bold=True)
    bbox = draw.textbbox((0, 0), spec["badge"], font=f_badge)
    draw.text((seal_x - (bbox[2] - bbox[0]) / 2, seal_y - 20), spec["badge"], font=f_badge, fill=(255, 255, 255))
    v_str = "VERIFIED"
    bbox_v = draw.textbbox((0, 0), v_str, font=load_font(13, bold=True))
    draw.text((seal_x - (bbox_v[2] - bbox_v[0]) / 2, seal_y + 8), v_str, font=load_font(13, bold=True), fill=(255, 255, 255))

    # Right block (Signature)
    sig_cx = W - 330
    sig_text = "Academic & Technical Board"
    bbox_sig = draw.textbbox((0, 0), sig_text, font=f_sig)
    draw.text((sig_cx - (bbox_sig[2] - bbox_sig[0]) / 2, 855), sig_text, font=f_sig, fill=acc)
    draw.line([(W - 520, 900), (W - 140, 900)], fill=gold, width=2)
    exam_str = "AUTHORIZED EXAMINER & BOARD"
    bbox_ex = draw.textbbox((0, 0), exam_str, font=f_meta)
    draw.text((sig_cx - (bbox_ex[2] - bbox_ex[0]) / 2, 912), exam_str, font=f_meta, fill=dark)
    std_str = "National Engineering Standard"
    bbox_st = draw.textbbox((0, 0), std_str, font=f_meta_sm)
    draw.text((sig_cx - (bbox_st[2] - bbox_st[0]) / 2, 942), std_str, font=f_meta_sm, fill=slate)

    out_path = os.path.join("public/certificates", spec["file"])
    img.save(out_path, "PNG", optimize=True)
    print("Saved certificate:", out_path)

for c in CERTIFICATES:
    create_certificate(c)

print("All 8 certificates generated successfully!")

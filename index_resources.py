from opensearchpy import OpenSearch
import os
from dotenv import load_dotenv
load_dotenv()

client = OpenSearch(
    os.environ.get("BONSAI_URL", ""),
    verify_certs=False,
)

resources = [
    # ── ORIGINAL 31 RESOURCES ─────────────────────────────────────────────────
    {
        "title": "CS50P - Introduction to Programming with Python",
        "url": "https://cs50.harvard.edu/python",
        "type": "course",
        "topic": "Python",
        "level": "beginner",
        "free": True,
        "description": "Harvard's free Python course. Best starting point for learning Python from scratch with lectures and projects.",
        "learning_style": ["visual", "text", "hands-on"],
        "pace": "structured",
        "goal": ["understand concepts", "build projects"]
    },
    {
        "title": "CS50x - Introduction to Computer Science",
        "url": "https://cs50.harvard.edu/x",
        "type": "course",
        "topic": "Computer Science",
        "level": "beginner",
        "free": True,
        "description": "Harvard's most popular CS course. Covers C, Python, SQL, web development with real problem sets.",
        "learning_style": ["visual", "text", "hands-on"],
        "pace": "structured",
        "goal": ["understand concepts", "build projects", "get interview-ready"]
    },
    {
        "title": "3Blue1Brown - Neural Networks Series",
        "url": "https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi",
        "type": "video",
        "topic": "Deep Learning",
        "level": "beginner",
        "free": True,
        "description": "Beautiful visual explanation of how neural networks work. Best way to actually understand the math intuitively.",
        "learning_style": ["visual", "audio"],
        "pace": "self-paced",
        "goal": ["understand concepts"]
    },
    {
        "title": "fast.ai - Practical Deep Learning for Coders",
        "url": "https://course.fast.ai",
        "type": "course",
        "topic": "Machine Learning",
        "level": "intermediate",
        "free": True,
        "description": "Learn deep learning by building real models first, theory later. Best practical ML course available free.",
        "learning_style": ["hands-on", "visual"],
        "pace": "self-paced",
        "goal": ["build projects", "understand concepts"]
    },
    {
        "title": "Roadmap.sh - Python Developer Roadmap",
        "url": "https://roadmap.sh/python",
        "type": "roadmap",
        "topic": "Python",
        "level": "beginner",
        "free": True,
        "description": "Visual step by step roadmap to learn Python properly. Know exactly what to learn and in what order.",
        "learning_style": ["visual", "reference"],
        "pace": "self-paced",
        "goal": ["understand concepts", "learn tools"]
    },
    {
        "title": "Roadmap.sh - AI and Data Scientist Roadmap",
        "url": "https://roadmap.sh/ai-data-scientist",
        "type": "roadmap",
        "topic": "AI/ML",
        "level": "beginner",
        "free": True,
        "description": "Visual roadmap to become an AI engineer. Perfect for students who don't know where to start.",
        "learning_style": ["visual", "reference"],
        "pace": "self-paced",
        "goal": ["understand concepts", "learn tools"]
    },
    {
        "title": "Roadmap.sh - Full Stack Developer Roadmap",
        "url": "https://roadmap.sh/full-stack",
        "type": "roadmap",
        "topic": "Web Development",
        "level": "beginner",
        "free": True,
        "description": "Complete visual roadmap to become a full stack developer. Clear and structured path.",
        "learning_style": ["visual", "reference"],
        "pace": "self-paced",
        "goal": ["understand concepts", "build projects", "learn tools"]
    },
    {
        "title": "Exercism - Python Track",
        "url": "https://exercism.org/tracks/python",
        "type": "practice",
        "topic": "Python",
        "level": "beginner",
        "free": True,
        "description": "Practice Python by solving exercises with mentor feedback. Great for building coding confidence through doing.",
        "learning_style": ["hands-on"],
        "pace": "self-paced",
        "goal": ["build projects", "get interview-ready"]
    },
    {
        "title": "Kaggle Learn - Free Micro-Courses",
        "url": "https://www.kaggle.com/learn",
        "type": "course",
        "topic": "Data Science",
        "level": "beginner",
        "free": True,
        "description": "Free short courses on Python, ML, SQL. Earn certificates and practice on real datasets immediately.",
        "learning_style": ["hands-on", "text"],
        "pace": "micro-learning",
        "goal": ["build projects", "understand concepts", "get interview-ready"]
    },
    {
        "title": "Google Machine Learning Crash Course",
        "url": "https://developers.google.com/machine-learning/crash-course",
        "type": "course",
        "topic": "Machine Learning",
        "level": "beginner",
        "free": True,
        "description": "Free ML course by Google with videos, exercises and real examples. Structured and beginner friendly.",
        "learning_style": ["visual", "text", "hands-on"],
        "pace": "structured",
        "goal": ["understand concepts", "learn tools"]
    },
    {
        "title": "Andrej Karpathy - Zero to Hero Neural Networks",
        "url": "https://karpathy.ai/zero-to-hero.html",
        "type": "video",
        "topic": "Deep Learning",
        "level": "intermediate",
        "free": True,
        "description": "Build neural networks from scratch in Python. Best resource to deeply understand how LLMs actually work.",
        "learning_style": ["visual", "audio", "hands-on"],
        "pace": "self-paced",
        "goal": ["understand concepts", "build projects"]
    },
    {
        "title": "freeCodeCamp - Full Curriculum",
        "url": "https://www.freecodecamp.org",
        "type": "course",
        "topic": "Web Development",
        "level": "beginner",
        "free": True,
        "description": "Free certifications in web development and data science. Completely project-based — learn by building.",
        "learning_style": ["hands-on", "text"],
        "pace": "self-paced",
        "goal": ["build projects", "get interview-ready"]
    },
    {
        "title": "MIT OpenCourseWare - Introduction to Algorithms",
        "url": "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011",
        "type": "course",
        "topic": "Algorithms",
        "level": "intermediate",
        "free": True,
        "description": "Free MIT lecture videos and problem sets on algorithms and data structures. Essential for tech interviews.",
        "learning_style": ["visual", "audio", "text"],
        "pace": "structured",
        "goal": ["understand concepts", "get interview-ready"]
    },
    {
        "title": "LeetCode - Coding Practice",
        "url": "https://leetcode.com",
        "type": "practice",
        "topic": "Data Structures and Algorithms",
        "level": "intermediate",
        "free": True,
        "description": "Free coding practice platform. Essential for placements and internship interviews at tech companies in India.",
        "learning_style": ["hands-on"],
        "pace": "self-paced",
        "goal": ["get interview-ready"]
    },
    {
        "title": "Hugging Face NLP Course",
        "url": "https://huggingface.co/learn/nlp-course",
        "type": "course",
        "topic": "NLP / AI",
        "level": "intermediate",
        "free": True,
        "description": "Free course on natural language processing using Transformers. Best way to learn modern NLP and work with LLMs.",
        "learning_style": ["text", "hands-on"],
        "pace": "self-paced",
        "goal": ["understand concepts", "build projects", "learn tools"]
    },
    {
        "title": "Missing Semester - MIT",
        "url": "https://missing.csail.mit.edu",
        "type": "course",
        "topic": "Developer Tools",
        "level": "beginner",
        "free": True,
        "description": "Free MIT course on tools CS students are never taught — terminal, Git, shell scripting, debugging. Essential.",
        "learning_style": ["text", "hands-on"],
        "pace": "self-paced",
        "goal": ["learn tools"]
    },
    {
        "title": "Google Cloud Skills Boost",
        "url": "https://cloudskillsboost.google",
        "type": "course",
        "topic": "Cloud / GCP",
        "level": "beginner",
        "free": True,
        "description": "Free Google Cloud labs and courses. Earn badges and certifications. Hands-on in real cloud environment.",
        "learning_style": ["hands-on"],
        "pace": "self-paced",
        "goal": ["learn tools", "build projects"]
    },
    {
        "title": "BlueDot Impact - AI Safety Fundamentals",
        "url": "https://aisafetyfundamentals.com",
        "type": "course",
        "topic": "AI Safety",
        "level": "beginner",
        "free": True,
        "description": "Free 8-week course on AI safety. Covers alignment, risks, and how to contribute to the field. Reading-heavy.",
        "learning_style": ["text"],
        "pace": "structured",
        "goal": ["understand concepts"]
    },
    {
        "title": "NPTEL - Introduction to Machine Learning (IIT Madras)",
        "url": "https://nptel.ac.in/courses/106106139",
        "type": "course",
        "topic": "Machine Learning",
        "level": "intermediate",
        "free": True,
        "description": "Free IIT Madras ML course with certificate. Well recognized by Indian companies and useful for placements.",
        "learning_style": ["audio", "visual", "text"],
        "pace": "structured",
        "goal": ["understand concepts", "get interview-ready"]
    },
    {
        "title": "NPTEL - Data Science for Engineers (IIT Madras)",
        "url": "https://nptel.ac.in/courses/106106177",
        "type": "course",
        "topic": "Data Science",
        "level": "intermediate",
        "free": True,
        "description": "Free IIT course on data science. Recognized by Indian universities and employers. Great for JNTU students.",
        "learning_style": ["audio", "visual", "text"],
        "pace": "structured",
        "goal": ["understand concepts", "get interview-ready"]
    },
    {
        "title": "SWAYAM - Free Indian Government Courses",
        "url": "https://swayam.gov.in",
        "type": "course",
        "topic": "Computer Science",
        "level": "beginner",
        "free": True,
        "description": "Free government platform with IIT and IIM courses. Certificates recognized by Indian universities.",
        "learning_style": ["audio", "visual", "text"],
        "pace": "structured",
        "goal": ["understand concepts", "get interview-ready"]
    },
    {
        "title": "W3Schools - HTML CSS JavaScript Reference",
        "url": "https://www.w3schools.com",
        "type": "reference",
        "topic": "Web Development",
        "level": "beginner",
        "free": True,
        "description": "Free reference and tutorials for web technologies. Best quick-reference site. Try code directly in browser.",
        "learning_style": ["reference", "hands-on"],
        "pace": "micro-learning",
        "goal": ["learn tools", "build projects"]
    },
    {
        "title": "DeepLearning.AI - AI For Everyone",
        "url": "https://www.deeplearning.ai/courses/ai-for-everyone",
        "type": "course",
        "topic": "AI",
        "level": "beginner",
        "free": True,
        "description": "Free non-technical AI course by Andrew Ng. Understand what AI can and cannot do. Great first step into AI.",
        "learning_style": ["visual", "audio"],
        "pace": "micro-learning",
        "goal": ["understand concepts"]
    },
    {
        "title": "Papers With Code",
        "url": "https://paperswithcode.com",
        "type": "reference",
        "topic": "AI Research",
        "level": "advanced",
        "free": True,
        "description": "Free platform linking AI research papers with working code. Great for students who want to explore research.",
        "learning_style": ["text", "hands-on", "reference"],
        "pace": "self-paced",
        "goal": ["understand concepts", "build projects"]
    },
    {
        "title": "Codecademy - Learn Python",
        "url": "https://www.codecademy.com/learn/learn-python-3",
        "type": "course",
        "topic": "Python",
        "level": "beginner",
        "free": True,
        "description": "Interactive Python course. Type code directly in the browser with instant feedback. Perfect for visual learners.",
        "learning_style": ["hands-on", "visual"],
        "pace": "micro-learning",
        "goal": ["understand concepts"]
    },
    {
        "title": "SQL for Data Science - Kaggle",
        "url": "https://www.kaggle.com/learn/intro-to-sql",
        "type": "course",
        "topic": "SQL / Data",
        "level": "beginner",
        "free": True,
        "description": "Free SQL course on Kaggle. Learn to query large datasets. Essential skill for data science and ML roles.",
        "learning_style": ["hands-on", "text"],
        "pace": "micro-learning",
        "goal": ["learn tools", "get interview-ready"]
    },
    {
        "title": "The Odin Project - Full Stack Web Development",
        "url": "https://www.theodinproject.com",
        "type": "course",
        "topic": "Web Development",
        "level": "beginner",
        "free": True,
        "description": "Free full stack curriculum. Project-based from day one. Best for students who learn by building real things.",
        "learning_style": ["hands-on", "text"],
        "pace": "self-paced",
        "goal": ["build projects", "learn tools"]
    },
    {
        "title": "Stanford CS229 - Machine Learning",
        "url": "https://cs229.stanford.edu",
        "type": "course",
        "topic": "Machine Learning",
        "level": "advanced",
        "free": True,
        "description": "Stanford's ML course by Andrew Ng. Free lecture notes and problem sets. Best theoretical ML foundation.",
        "learning_style": ["text", "visual"],
        "pace": "structured",
        "goal": ["understand concepts"]
    },
    {
        "title": "YouTube - Traversy Media",
        "url": "https://www.youtube.com/@TraversyMedia",
        "type": "video",
        "topic": "Web Development",
        "level": "beginner",
        "free": True,
        "description": "Free project-based web development tutorials on YouTube. Build real projects while watching. Great for visual learners.",
        "learning_style": ["visual", "audio", "hands-on"],
        "pace": "micro-learning",
        "goal": ["build projects", "learn tools"]
    },
    {
        "title": "Spotify - Lex Fridman Podcast",
        "url": "https://open.spotify.com/show/2MAi0BvDc6GTFvKFPXnkCL",
        "type": "podcast",
        "topic": "AI / Technology",
        "level": "beginner",
        "free": True,
        "description": "Free podcast with deep conversations with AI researchers, engineers and scientists. Great for audio learners curious about AI.",
        "learning_style": ["audio"],
        "pace": "micro-learning",
        "goal": ["understand concepts"]
    },
    {
        "title": "GitHub - Awesome Python Resources",
        "url": "https://github.com/vinta/awesome-python",
        "type": "reference",
        "topic": "Python",
        "level": "intermediate",
        "free": True,
        "description": "Curated list of Python frameworks, libraries and resources. Best reference when you know basics and want to go deeper.",
        "learning_style": ["reference"],
        "pace": "self-paced",
        "goal": ["learn tools", "build projects"]
    },

    # ── NEW: CYBERSECURITY ────────────────────────────────────────────────────
    {
        "title": "TryHackMe - Learn Cybersecurity",
        "url": "https://tryhackme.com",
        "type": "course",
        "topic": "Cybersecurity",
        "level": "beginner",
        "free": True,
        "description": "Free beginner-friendly cybersecurity platform. Learn hacking and defense through browser-based labs. No setup needed.",
        "learning_style": ["hands-on", "visual"],
        "pace": "self-paced",
        "goal": ["understand concepts", "build projects", "learn tools"]
    },
    {
        "title": "Hack The Box - Cybersecurity Training",
        "url": "https://www.hackthebox.com",
        "type": "practice",
        "topic": "Cybersecurity",
        "level": "intermediate",
        "free": True,
        "description": "Real-world hacking challenges and labs. Free tier available. Build practical penetration testing skills.",
        "learning_style": ["hands-on"],
        "pace": "self-paced",
        "goal": ["build projects", "get interview-ready", "learn tools"]
    },
    {
        "title": "Google Cybersecurity Certificate - Coursera (Audit Free)",
        "url": "https://www.coursera.org/professional-certificates/google-cybersecurity",
        "type": "course",
        "topic": "Cybersecurity",
        "level": "beginner",
        "free": True,
        "description": "Google's cybersecurity career certificate. Audit for free on Coursera. Covers networks, Linux, Python, and threat detection.",
        "learning_style": ["visual", "text", "hands-on"],
        "pace": "structured",
        "goal": ["understand concepts", "get interview-ready", "learn tools"]
    },
    {
        "title": "Cybrary - Free Cybersecurity Courses",
        "url": "https://www.cybrary.it",
        "type": "course",
        "topic": "Cybersecurity",
        "level": "beginner",
        "free": True,
        "description": "Free cybersecurity training platform with courses on ethical hacking, network security, and cloud security.",
        "learning_style": ["visual", "audio", "text"],
        "pace": "self-paced",
        "goal": ["understand concepts", "learn tools", "get interview-ready"]
    },
    {
        "title": "OWASP - Web Security Testing Guide",
        "url": "https://owasp.org/www-project-web-security-testing-guide",
        "type": "reference",
        "topic": "Cybersecurity",
        "level": "intermediate",
        "free": True,
        "description": "Free guide to web application security testing. Industry standard reference for understanding web vulnerabilities.",
        "learning_style": ["text", "reference"],
        "pace": "self-paced",
        "goal": ["understand concepts", "build projects", "learn tools"]
    },
    {
        "title": "Roadmap.sh - Cybersecurity Roadmap",
        "url": "https://roadmap.sh/cyber-security",
        "type": "roadmap",
        "topic": "Cybersecurity",
        "level": "beginner",
        "free": True,
        "description": "Visual step-by-step roadmap to become a cybersecurity professional. Know exactly what to learn and in what order.",
        "learning_style": ["visual", "reference"],
        "pace": "self-paced",
        "goal": ["understand concepts", "learn tools"]
    },

    # ── NEW: DSA & COMPETITIVE PROGRAMMING ───────────────────────────────────
    {
        "title": "NeetCode - DSA Roadmap and Solutions",
        "url": "https://neetcode.io",
        "type": "course",
        "topic": "Data Structures and Algorithms",
        "level": "intermediate",
        "free": True,
        "description": "Free DSA roadmap with video solutions for LeetCode problems. Best resource for placement preparation in India.",
        "learning_style": ["visual", "audio", "hands-on"],
        "pace": "self-paced",
        "goal": ["get interview-ready", "understand concepts"]
    },
    {
        "title": "Codeforces - Competitive Programming",
        "url": "https://codeforces.com",
        "type": "practice",
        "topic": "Competitive Programming",
        "level": "intermediate",
        "free": True,
        "description": "Free competitive programming platform with regular contests. Build problem-solving speed and logic for coding rounds.",
        "learning_style": ["hands-on"],
        "pace": "self-paced",
        "goal": ["get interview-ready", "build projects"]
    },
    {
        "title": "GeeksforGeeks - DSA",
        "url": "https://www.geeksforgeeks.org/data-structures",
        "type": "reference",
        "topic": "Data Structures and Algorithms",
        "level": "beginner",
        "free": True,
        "description": "Free DSA tutorials with code examples in Python, Java, C++. Widely used by Indian CS students for placements.",
        "learning_style": ["text", "reference", "hands-on"],
        "pace": "self-paced",
        "goal": ["understand concepts", "get interview-ready"]
    },
    {
        "title": "CP-Algorithms",
        "url": "https://cp-algorithms.com",
        "type": "reference",
        "topic": "Competitive Programming",
        "level": "advanced",
        "free": True,
        "description": "Free collection of competitive programming algorithms with explanations and code. Essential for ICPC and coding contests.",
        "learning_style": ["text", "reference"],
        "pace": "self-paced",
        "goal": ["understand concepts", "get interview-ready"]
    },

    # ── NEW: CLOUD & DEVOPS ───────────────────────────────────────────────────
    {
        "title": "AWS Training - Free Digital Courses",
        "url": "https://aws.amazon.com/training/digital",
        "type": "course",
        "topic": "Cloud / AWS",
        "level": "beginner",
        "free": True,
        "description": "Free AWS training courses and labs. Learn cloud fundamentals directly from Amazon. Great for cloud certifications.",
        "learning_style": ["visual", "hands-on", "text"],
        "pace": "self-paced",
        "goal": ["learn tools", "get interview-ready", "build projects"]
    },
    {
        "title": "KodeKloud - DevOps Free Courses",
        "url": "https://kodekloud.com/courses/",
        "type": "course",
        "topic": "DevOps",
        "level": "beginner",
        "free": True,
        "description": "Free DevOps courses on Docker, Kubernetes, Linux, and shell scripting with browser-based labs.",
        "learning_style": ["visual", "hands-on"],
        "pace": "self-paced",
        "goal": ["learn tools", "build projects"]
    },
    {
        "title": "Roadmap.sh - DevOps Roadmap",
        "url": "https://roadmap.sh/devops",
        "type": "roadmap",
        "topic": "DevOps",
        "level": "beginner",
        "free": True,
        "description": "Visual roadmap to become a DevOps engineer. Covers Linux, Docker, Kubernetes, CI/CD and cloud platforms.",
        "learning_style": ["visual", "reference"],
        "pace": "self-paced",
        "goal": ["understand concepts", "learn tools"]
    },

    # ── NEW: SYSTEM DESIGN ────────────────────────────────────────────────────
    {
        "title": "System Design Primer - GitHub",
        "url": "https://github.com/donnemartin/system-design-primer",
        "type": "reference",
        "topic": "System Design",
        "level": "intermediate",
        "free": True,
        "description": "Free GitHub repo covering system design concepts. Essential for senior tech interviews at top Indian and global companies.",
        "learning_style": ["text", "visual", "reference"],
        "pace": "self-paced",
        "goal": ["understand concepts", "get interview-ready"]
    },
    {
        "title": "ByteByteGo - System Design YouTube",
        "url": "https://www.youtube.com/@ByteByteGo",
        "type": "video",
        "topic": "System Design",
        "level": "intermediate",
        "free": True,
        "description": "Free YouTube channel explaining system design concepts visually. Short, clear videos on scalability and architecture.",
        "learning_style": ["visual", "audio"],
        "pace": "micro-learning",
        "goal": ["understand concepts", "get interview-ready"]
    },

    # ── NEW: LINUX & NETWORKING ───────────────────────────────────────────────
    {
        "title": "Linux Journey - Free Linux Learning",
        "url": "https://linuxjourney.com",
        "type": "course",
        "topic": "Linux",
        "level": "beginner",
        "free": True,
        "description": "Free interactive Linux course covering command line, filesystems, networking. Learn Linux fundamentals step by step.",
        "learning_style": ["text", "hands-on"],
        "pace": "self-paced",
        "goal": ["learn tools", "understand concepts"]
    },
    {
        "title": "Computer Networking Full Course - freeCodeCamp YouTube",
        "url": "https://www.youtube.com/watch?v=qiQR5rTSshw",
        "type": "video",
        "topic": "Networking",
        "level": "beginner",
        "free": True,
        "description": "Free 9-hour networking course on YouTube. Covers TCP/IP, DNS, HTTP, and how the internet works. Great for interviews.",
        "learning_style": ["visual", "audio"],
        "pace": "self-paced",
        "goal": ["understand concepts", "get interview-ready"]
    },

    # ── NEW: JAVA & BACKEND ───────────────────────────────────────────────────
    {
        "title": "Java Programming - MOOC Helsinki",
        "url": "https://java-programming.mooc.fi",
        "type": "course",
        "topic": "Java",
        "level": "beginner",
        "free": True,
        "description": "Free comprehensive Java course from University of Helsinki. 200+ exercises. Best free Java course available online.",
        "learning_style": ["text", "hands-on"],
        "pace": "self-paced",
        "goal": ["understand concepts", "build projects", "get interview-ready"]
    },
    {
        "title": "Spring Boot - Official Guides",
        "url": "https://spring.io/guides",
        "type": "reference",
        "topic": "Backend Development",
        "level": "intermediate",
        "free": True,
        "description": "Free official Spring Boot guides and tutorials. Learn Java backend development with the most popular enterprise framework.",
        "learning_style": ["text", "hands-on", "reference"],
        "pace": "self-paced",
        "goal": ["build projects", "learn tools"]
    },

    # ── NEW: DATABASE ─────────────────────────────────────────────────────────
    {
        "title": "SQLZoo - Interactive SQL Tutorial",
        "url": "https://sqlzoo.net",
        "type": "practice",
        "topic": "SQL",
        "level": "beginner",
        "free": True,
        "description": "Free interactive SQL practice directly in browser. Learn SQL by writing queries on real datasets immediately.",
        "learning_style": ["hands-on", "text"],
        "pace": "micro-learning",
        "goal": ["learn tools", "get interview-ready"]
    },
    {
        "title": "MongoDB University - Free Courses",
        "url": "https://learn.mongodb.com",
        "type": "course",
        "topic": "Database / MongoDB",
        "level": "beginner",
        "free": True,
        "description": "Free official MongoDB courses and certifications. Learn NoSQL database design and querying from MongoDB directly.",
        "learning_style": ["visual", "hands-on", "text"],
        "pace": "self-paced",
        "goal": ["learn tools", "build projects"]
    },

    # ── NEW: MATHEMATICS FOR CS ───────────────────────────────────────────────
    {
        "title": "3Blue1Brown - Essence of Linear Algebra",
        "url": "https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2ZAgoER_jCDKDv",
        "type": "video",
        "topic": "Mathematics for ML",
        "level": "beginner",
        "free": True,
        "description": "Beautiful visual series on linear algebra. Essential foundation for machine learning. Best math videos on YouTube.",
        "learning_style": ["visual", "audio"],
        "pace": "self-paced",
        "goal": ["understand concepts"]
    },
    {
        "title": "Khan Academy - Statistics and Probability",
        "url": "https://www.khanacademy.org/math/statistics-probability",
        "type": "course",
        "topic": "Mathematics for ML",
        "level": "beginner",
        "free": True,
        "description": "Free statistics course essential for data science and ML. Clear explanations with practice exercises.",
        "learning_style": ["visual", "audio", "hands-on"],
        "pace": "self-paced",
        "goal": ["understand concepts"]
    },

    # ── NEW: REACT & FRONTEND ─────────────────────────────────────────────────
    {
        "title": "React Official Tutorial - React.dev",
        "url": "https://react.dev/learn",
        "type": "course",
        "topic": "React",
        "level": "beginner",
        "free": True,
        "description": "Free official React tutorial. Learn React by building a game. Best starting point for modern frontend development.",
        "learning_style": ["text", "hands-on"],
        "pace": "self-paced",
        "goal": ["understand concepts", "build projects"]
    },
    {
        "title": "Roadmap.sh - React Developer Roadmap",
        "url": "https://roadmap.sh/react",
        "type": "roadmap",
        "topic": "React",
        "level": "beginner",
        "free": True,
        "description": "Visual roadmap to become a React developer. Know exactly what to learn from basics to advanced concepts.",
        "learning_style": ["visual", "reference"],
        "pace": "self-paced",
        "goal": ["understand concepts", "learn tools"]
    },

    # ── NEW: OPEN SOURCE & GIT ────────────────────────────────────────────────
    {
        "title": "First Contributions - Open Source Guide",
        "url": "https://firstcontributions.github.io",
        "type": "course",
        "topic": "Open Source / Git",
        "level": "beginner",
        "free": True,
        "description": "Free guide to making your first open source contribution. Step-by-step with practice repo. Build your GitHub profile.",
        "learning_style": ["hands-on", "text"],
        "pace": "micro-learning",
        "goal": ["build projects", "learn tools"]
    },
    {
        "title": "Pro Git Book - Free Online",
        "url": "https://git-scm.com/book/en/v2",
        "type": "reference",
        "topic": "Git / Version Control",
        "level": "beginner",
        "free": True,
        "description": "The official free Git book. Complete reference for Git from basics to advanced. Available online at no cost.",
        "learning_style": ["text", "reference"],
        "pace": "self-paced",
        "goal": ["learn tools", "understand concepts"]
    },

    # ── NEW: AI / LLMs ────────────────────────────────────────────────────────
    {
        "title": "DeepLearning.AI - Short Courses",
        "url": "https://www.deeplearning.ai/short-courses",
        "type": "course",
        "topic": "AI / LLMs",
        "level": "intermediate",
        "free": True,
        "description": "Free short courses on LLMs, prompt engineering, and AI tools by Andrew Ng. 1-2 hours each, very practical.",
        "learning_style": ["visual", "hands-on"],
        "pace": "micro-learning",
        "goal": ["learn tools", "build projects", "understand concepts"]
    },
    {
        "title": "LangChain - Official Tutorials",
        "url": "https://python.langchain.com/docs/tutorials",
        "type": "reference",
        "topic": "AI / LLMs",
        "level": "intermediate",
        "free": True,
        "description": "Free official LangChain tutorials to build AI applications with LLMs. Best resource to start building AI-powered apps.",
        "learning_style": ["text", "hands-on", "reference"],
        "pace": "self-paced",
        "goal": ["build projects", "learn tools"]
    },

    # ── NEW: INTERVIEW PREP ───────────────────────────────────────────────────
    {
        "title": "InterviewBit - Tech Interview Preparation",
        "url": "https://www.interviewbit.com",
        "type": "practice",
        "topic": "Interview Preparation",
        "level": "intermediate",
        "free": True,
        "description": "Free platform popular with Indian students for placement prep. Covers DSA, system design and company-specific questions.",
        "learning_style": ["hands-on", "text"],
        "pace": "structured",
        "goal": ["get interview-ready"]
    },
    {
        "title": "Code360 - Coding Interview Preparation",
        "url": "https://www.naukri.com/code360/problems",
        "type": "practice",
        "topic": "Interview Preparation",
        "level": "beginner",
        "free": True,
        "description": "Free coding practice platform widely used by Indian engineering students for campus placements and internships.",
        "learning_style": ["hands-on"],
        "pace": "self-paced",
        "goal": ["get interview-ready"]
    },

    # ── NEW: MOBILE DEV ───────────────────────────────────────────────────────
    {
        "title": "Flutter - Official Codelabs",
        "url": "https://docs.flutter.dev/get-started/codelab",
        "type": "course",
        "topic": "Mobile Development",
        "level": "beginner",
        "free": True,
        "description": "Free official Flutter codelabs to build your first mobile app. Learn cross-platform iOS and Android development.",
        "learning_style": ["hands-on", "text"],
        "pace": "self-paced",
        "goal": ["build projects", "learn tools"]
    },
]

# Index all resources
success = 0
failed = 0
for resource in resources:
    try:
        client.index(index="cs-resources", body=resource)
        print(f"✅ {resource['title']}")
        success += 1
    except Exception as e:
        print(f"❌ FAILED: {resource['title']} — {e}")
        failed += 1

print(f"\n{'='*50}")
print(f"✅ Indexed: {success}")
print(f"❌ Failed:  {failed}")
print(f"📚 Total:   {success} resources in SkillPath")
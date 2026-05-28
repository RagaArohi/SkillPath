from elasticsearch import Elasticsearch

client = Elasticsearch(
    "https://my-elasticsearch-project-b4fa48.es.us-central1.gcp.elastic.cloud",
    api_key="RndsZ2FwNEI0U3MzYXpybFV3TXA6TGNkZVNzUl9YSnhhTXhkNkxhcUppUQ=="
)

resources = [
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
    }
]

for i, resource in enumerate(resources):
    client.index(index="cs-resources", id=i+1, document=resource)
    print(f"Indexed: {resource['title']}")

print(f"\nDone! {len(resources)} resources indexed with learning styles.")
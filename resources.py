"""
Phase 4 — "How to learn this, for free" layer.   OWNERS: Person A (fundamentals) + Person B (specialized)

This is a CURATED dictionary, not AI output. The AI invents fake course names and
URLs; this file is the trustworthy source. The AI's job (later) is only to produce
skills. THIS file determines what's real.

IMPORTANT (see PLAN.md gap #5): skills come back from the AI with messy names
("Data Analysis", "data analysis", "Pandas"). Match through normalize_skill() +
get_resources(), NOT a raw dict[skill] lookup, or almost everything will "miss".

⚠️ Both people edit this same file. Either work on ONE shared branch for this phase,
or merge one person's entries in before the other starts. See PLAN.md git notes.

The `free_certificate` flag must be honest:
    True  = course AND certificate are free
    False = course is free to take ("audit"), certificate costs money
    None  = no formal certificate exists
"""

LEARNING_RESOURCES = {

    # ── Fundamentals ──────────────────────────────────────────────────────────

    "python": {
        "basics": {
            "docs": "https://docs.python.org/3/tutorial/",
            "docs_scope": "Sections 3–9: control flow, data structures, modules, I/O, exceptions, classes, and stdlib overview",
            "style_guide": "https://peps.python.org/pep-0008/",
            "video": "Corey Schafer's Python Beginner + OOP playlist on YouTube",
            "course": "freeCodeCamp's Scientific Computing with Python certification",
            "free_certificate": True,
            "interactive_practice": "https://exercism.org/tracks/python",
            "interactive_practice_notes": "Mentor-reviewed exercises, fully free",
            "extra_practice": [
                "https://www.codewars.com",
                "https://www.hackerrank.com/domains/python",
                "https://pynative.com/python-exercises-with-solutions/",
            ],
            "interview_preparation": "https://leetcode.com",
            "project_ideas": [
                "CLI budget tracker using OOP, logging, and local file storage",
                "File-based todo app with search and tagging",
                "Text file analyzer that outputs a word-frequency report",
            ],
            "github_repos": [
                "https://github.com/vinta/awesome-python",          # curated libraries & tools
                "https://github.com/TheAlgorithms/Python",          # algorithm implementations in Python
                "https://github.com/practical-tutorials/project-based-learning#python",  # project-based curriculum
            ],
        },
    },

    "sql": {
        "basics": {
            "docs": "https://www.w3schools.com/sql/",
            "docs_scope": "SELECT, WHERE, JOIN, GROUP BY, HAVING, subqueries, indexes, constraints, and window functions",
            "style_guide": "https://sqlstyle.guide",
            "video": "\"SQL Tutorial – Full Database Course for Beginners\" by freeCodeCamp on YouTube",
            "course": "Kaggle Learn: Intro to SQL + Advanced SQL",
            "free_certificate": True,
            "interactive_practice": "https://sqlzoo.net",
            "interactive_practice_notes": "Browser-based exercises, no signup required",
            "extra_practice": [
                "https://www.hackerrank.com/domains/sql",
                "https://leetcode.com",
                "https://pgexercises.com",   # PostgreSQL-specific, great for real-world queries
            ],
            "interview_preparation": "https://leetcode.com",
            "project_ideas": [
                "E-commerce schema with constraints, indexes, and foreign keys",
                "Sales analytics pipeline using window functions and CTEs",
                "Student records database with enrollment and grade reporting queries",
            ],
            "github_repos": [
                "https://github.com/pingcap/awesome-database-learning",   # DB theory + SQL deep-dives
                "https://github.com/danhuss/awesome-sql",                 # curated SQL resources
                "https://github.com/getvmio/free-sql-resources",
            ],
        },
    },

    "git": {
        "basics": {
            "docs": "https://git-scm.com/book/en/v2",
            "docs_scope": "Chapters 1–3: Git basics, branching model, and working with remotes",
            "style_guide": "https://cbea.ms/git-commit/",   # \"How to Write a Git Commit Message\" — industry standard reference
            "video": "\"Git and GitHub for Beginners – Crash Course\" by freeCodeCamp on YouTube",
            "course": "The Odin Project: Foundations — Git Basics section",
            "free_certificate": None,
            "interactive_practice": "https://learngitbranching.js.org",
            "interactive_practice_notes": "Visual, gamified branching exercises — best interactive Git tool available",
            "extra_practice": [
                "https://ohmygit.org",          # open-source card game for learning Git
                "https://gitexercises.fracz.com",
            ],
            "interview_preparation": "https://www.interviewbit.com/git-interview-questions/",
            "project_ideas": [
                "Contribute a small fix or docs improvement to any open-source GitHub repo",
                "Set up a multi-branch feature workflow with rebasing and conflict resolution on a personal project",
            ],
            "github_repos": [
                "https://github.com/dictcp/awesome-git",              # curated Git tools and resources
                "https://github.com/firstcontributions/first-contributions",  # guided first open-source PR
            ],
        },
    },

    "data structures": {
        "basics": {
            "docs": "https://www.geeksforgeeks.org/data-structures/",
            "docs_scope": "Arrays, Linked Lists, Stacks, Queues, Hash Tables, Trees, Heaps, Graphs — focus on implementation + time complexity",
            "style_guide": None,
            "video": "\"Data Structures Easy to Advanced Course\" by William Fiset on freeCodeCamp YouTube",
            "course": "freeCodeCamp's JavaScript Algorithms and Data Structures certification (concepts are language-agnostic)",
            "free_certificate": True,
            "interactive_practice": "https://visualgo.net/en",
            "interactive_practice_notes": "Animated visualizations of every major data structure — essential for building mental models",
            "extra_practice": [
                "https://www.codewars.com",
                "https://leetcode.com",
                "https://www.hackerrank.com/domains/data-structures",
            ],
            "interview_preparation": "https://neetcode.io",   # free curated Leetcode roadmap by category
            "project_ideas": [
                "Implement a hash map from scratch in Python without using dict",
                "Build a graph-based maze solver using BFS and DFS",
                "Create a priority queue task scheduler using a min-heap",
            ],
            "github_repos": [
                "https://github.com/TheAlgorithms/Python",       # reference implementations
                "https://github.com/williamfiset/Algorithms",    # William Fiset's own repo (Java, pairs with his video)
                "https://github.com/tayllan/awesome-algorithms",
            ],
        },
    },

    "algorithms": {
        "basics": {
            "docs": "https://www.geeksforgeeks.org/fundamentals-of-algorithms/",
            "docs_scope": "Sorting, Searching, Recursion, Dynamic Programming, Greedy, Graph algorithms, Backtracking",
            "style_guide": None,
            "video": "\"Algorithms and Data Structures Tutorial – Full Course\" by freeCodeCamp on YouTube",
            "course": "MIT OpenCourseWare 6.006 Introduction to Algorithms (free lectures, problem sets, and exams)",
            "free_certificate": None,
            "interactive_practice": "https://neetcode.io",
            "interactive_practice_notes": "Free curated problem set organized by algorithm pattern — best structured roadmap available",
            "extra_practice": [
                "https://leetcode.com",
                "https://codeforces.com",          # competitive programming, harder problems
                "https://www.hackerrank.com/domains/algorithms",
            ],
            "interview_preparation": "https://leetcode.com",
            "reference_book": "\"Introduction to Algorithms\" (CLRS) — free via MIT OCW reading list; also at https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/",
            "project_ideas": [
                "Implement merge sort, quicksort, and heapsort; benchmark their performance on the same dataset",
                "Solve the 0/1 knapsack problem with both recursion + memoization and bottom-up DP",
                "Build a shortest-path visualizer using Dijkstra's algorithm",
            ],
            "github_repos": [
                "https://github.com/TheAlgorithms/Python",
                "https://github.com/tayllan/awesome-algorithms",
                "https://github.com/lnishan/awesome-competitive-programming",
            ],
        },
    },

    "linux": {
        "basics": {
            "docs": "https://linuxcommand.org/lc3_learning_the_shell.php",
            "docs_scope": "Shell basics, filesystem navigation, permissions, redirection, pipelines, and shell scripting",
            "style_guide": "https://google.github.io/styleguide/shellguide.html",  # Google Shell Style Guide
            "video": "\"Linux Command Line Full Course\" by freeCodeCamp on YouTube",
            "course": "The Odin Project: Foundations — Command Line Basics",
            "free_certificate": None,
            "interactive_practice": "https://overthewire.org/wargames/bandit/",
            "interactive_practice_notes": "Bandit wargame: learn Linux shell by solving security challenges over SSH — genuinely fun",
            "extra_practice": [
                "https://cmdchallenge.com",       # browser-based shell challenges
                "https://www.learnshell.org",
            ],
            "interview_preparation": "https://www.interviewbit.com/linux-interview-questions/",
            "project_ideas": [
                "Write a Bash script that backs up a directory, timestamps it, and removes backups older than 7 days",
                "Build a system monitor script that logs CPU and memory usage every minute to a CSV file",
                "Automate a dev environment setup with a single shell script (install packages, configure dotfiles)",
            ],
            "github_repos": [
                "https://github.com/alebcay/awesome-shell",         # curated shell tools and resources
                "https://github.com/jlevy/the-art-of-command-line", # must-read command-line reference
                "https://github.com/dylanaraps/pure-bash-bible",    # bash idioms and patterns
            ],
        },
    },

    "java": {
        "basics": {
            "docs": "https://docs.oracle.com/javase/tutorial/",
            "docs_scope": "Getting Started, Learning the Java Language (OOP, interfaces, generics), Essential Java Classes (collections, I/O, concurrency basics)",
            "style_guide": "https://google.github.io/styleguide/javaguide.html",
            "video": "\"Java Full Course\" by Mosh Hamedani on YouTube",
            "course": "MOOC.fi Java Programming — University of Helsinki (free, certificate free)",
            "free_certificate": True,
            "interactive_practice": "https://exercism.org/tracks/java",
            "interactive_practice_notes": "Mentor-reviewed exercises, free",
            "extra_practice": [
                "https://www.hackerrank.com/domains/java",
                "https://codingbat.com/java",     # logic exercises, great for beginners
                "https://leetcode.com",
            ],
            "interview_preparation": "https://www.interviewbit.com/java-interview-questions/",
            "project_ideas": [
                "Console-based bank account system using OOP, inheritance, and exception handling",
                "Multi-threaded file downloader that downloads chunks in parallel",
                "Simple HTTP server using Java's built-in ServerSocket",
            ],
            "github_repos": [
                "https://github.com/akullpp/awesome-java",          # curated Java libraries and tools
                "https://github.com/TheAlgorithms/Java",            # algorithm implementations
                "https://github.com/iluwatar/java-design-patterns", # GoF patterns with clean Java examples
            ],
        },
    },

    "javascript": {
        "basics": {
            "docs": "https://developer.mozilla.org/en-US/docs/Learn/JavaScript",
            "docs_scope": "Core language: variables, functions, arrays, objects, DOM, events, fetch/async, and ES6+ features",
            "style_guide": "https://google.github.io/styleguide/jsguide.html",
            "video": "\"JavaScript Full Course for Beginners\" by Dave Gray on YouTube",
            "course": "freeCodeCamp's JavaScript Algorithms and Data Structures certification",
            "free_certificate": True,
            "interactive_practice": "https://javascript.info",
            "interactive_practice_notes": "The Modern JavaScript Tutorial — best written JS reference; each section has exercises",
            "extra_practice": [
                "https://exercism.org/tracks/javascript",
                "https://www.codewars.com",
                "https://www.hackerrank.com/domains/javascript",
            ],
            "interview_preparation": "https://www.greatfrontend.com/questions/js",   # free JS interview questions
            "project_ideas": [
                "Vanilla JS weather app consuming a public REST API",
                "Drag-and-drop Kanban board using only HTML, CSS, and JS",
                "Real-time character/word counter with localStorage persistence",
            ],
            "github_repos": [
                "https://github.com/sorrycc/awesome-javascript",
                "https://github.com/leonardomso/33-js-concepts",     # 33 concepts every JS dev should know
                "https://github.com/you-dont-need/You-Dont-Need-Lodash-Underscore",  # idiomatic modern JS
            ],
        },
    },

    # ── Web & Frontend ────────────────────────────────────────────────────────

    "react": {
        "basics": {
            "docs": "https://react.dev/learn",
            "docs_scope": "Quick Start, Describing the UI, Adding Interactivity, Managing State, and Hooks reference",
            "style_guide": "https://react.dev/learn/thinking-in-react",   # official mental model guide
            "video": "\"React Course\" by Bob Ziroll on Scrimba's YouTube channel",
            "course": "The Odin Project: React path",
            "free_certificate": None,
            "interactive_practice": "https://scrimba.com/learn/learnreact",
            "interactive_practice_notes": "Free interactive course; you edit code in the browser alongside the video",
            "extra_practice": [
                "https://react.gg",    # free visual React course by ui.dev
                "https://www.freecodecamp.org/learn/front-end-development-libraries/",
            ],
            "interview_preparation": "https://github.com/sudheerj/reactjs-interview-questions",
            "project_ideas": [
                "Task manager with Context API for global state, no Redux",
                "GitHub profile viewer consuming the GitHub REST API",
                "Multi-step form wizard with validation and local state management",
            ],
            "github_repos": [
                "https://github.com/enaqx/awesome-react",
                "https://github.com/sudheerj/reactjs-interview-questions",
                "https://github.com/alan2207/bulletproof-react",    # production-level React architecture reference
            ],
        },
    },

    "html and css": {
        "basics": {
            "docs": "https://developer.mozilla.org/en-US/docs/Learn/HTML",
            "docs_scope": "HTML: document structure, semantic elements, forms, accessibility basics. CSS: box model, flexbox, grid, responsive design, custom properties",
            "style_guide": "https://google.github.io/styleguide/htmlcssguide.html",
            "video": "\"HTML & CSS Full Course\" by Dave Gray on YouTube",
            "course": "freeCodeCamp's Responsive Web Design certification",
            "free_certificate": True,
            "interactive_practice": "https://www.theodinproject.com/paths/foundations",
            "interactive_practice_notes": "The Odin Project Foundations path covers HTML/CSS with real projects",
            "extra_practice": [
                "https://flexboxfroggy.com",     # gamified Flexbox practice
                "https://cssgridgarden.com",     # gamified CSS Grid practice
                "https://www.frontendmentor.io/challenges",  # free design-to-code challenges
            ],
            "interview_preparation": "https://www.interviewbit.com/html-interview-questions/",
            "project_ideas": [
                "Pixel-perfect clone of a real landing page using only HTML and CSS",
                "Responsive personal portfolio with dark mode using CSS custom properties",
                "CSS-only card component library with hover animations",
            ],
            "github_repos": [
                "https://github.com/nicholasgasior/awesome-css",
                "https://github.com/micromata/awesome-css-learning",
                "https://github.com/AllThingsSmitty/css-protips",   # practical CSS tips
            ],
        },
    },

    "rest apis": {
        "basics": {
            "docs": "https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Client-side_web_APIs",
            "docs_scope": "Client-side APIs, fetch, HTTP verbs, status codes, authentication patterns, JSON handling",
            "style_guide": "https://github.com/microsoft/api-guidelines",  # Microsoft REST API guidelines — widely adopted
            "video": "\"APIs for Beginners – How to use an API\" by freeCodeCamp on YouTube",
            "course": "Postman's API Fundamentals Student Expert certification (free)",
            "free_certificate": True,
            "interactive_practice": "https://www.postman.com/postman/workspace/postman-public-workspace/",
            "interactive_practice_notes": "Use Postman's free tier to explore and test public APIs hands-on",
            "extra_practice": [
                "https://reqres.in",          # fake REST API for practice; no key required
                "https://jsonplaceholder.typicode.com",  # another popular free fake API
                "https://public-apis.io",     # directory of free public APIs to build with
            ],
            "interview_preparation": "https://www.interviewbit.com/rest-api-interview-questions/",
            "project_ideas": [
                "Weather dashboard consuming OpenWeatherMap's free API tier",
                "Movie search app using the free OMDb API",
                "Build and document your own REST API with FastAPI or Express",
            ],
            "github_repos": [
                "https://github.com/public-apis/public-apis",        # massive curated list of free APIs
                "https://github.com/microsoft/api-guidelines",
            ],
        },
    },

    # ── Data & ML ─────────────────────────────────────────────────────────────

    "data analysis": {
        "basics": {
            "docs": "https://pandas.pydata.org/docs/user_guide/10min.html",
            "docs_scope": "10 Minutes to pandas, then Indexing, GroupBy, Merge/Join, Time Series, and Visualization sections",
            "style_guide": "https://peps.python.org/pep-0008/",
            "video": "\"Data Analysis with Python\" full course by freeCodeCamp on YouTube",
            "course": "Kaggle Learn: Pandas + Data Visualization (both free with free certificates)",
            "free_certificate": True,
            "interactive_practice": "https://www.kaggle.com/learn/pandas",
            "interactive_practice_notes": "Kaggle's interactive notebooks run in the browser, no setup required",
            "extra_practice": [
                "https://www.kaggle.com/datasets",    # pick any dataset and explore it
                "https://www.hackerrank.com/domains/python",  # includes pandas challenges
            ],
            "interview_preparation": "https://www.interviewbit.com/pandas-interview-questions/",
            "project_ideas": [
                "Exploratory data analysis (EDA) on a Kaggle dataset with a full written report",
                "Titanic or NYC Airbnb dataset analysis with matplotlib/seaborn visualizations",
                "Automated CSV cleaner that detects nulls, duplicates, and type mismatches",
            ],
            "github_repos": [
                "https://github.com/jvns/pandas-cookbook",          # practical recipes, Julia Evans
                "https://github.com/guipsamora/pandas_exercises",   # 100+ exercises with solutions
                "https://github.com/jakevdp/PythonDataScienceHandbook",  # Jupyter notebooks, full textbook
            ],
        },
    },

    "machine learning": {
        "basics": {
            "docs": "https://scikit-learn.org/stable/getting_started.html",
            "docs_scope": "Getting Started, User Guide chapters 1–6: supervised models, preprocessing, model selection, evaluation, pipelines",
            "style_guide": None,
            "video": "StatQuest with Josh Starmer on YouTube — ML Fundamentals playlist",
            "course": "Kaggle Learn: Intro to ML + Intermediate ML",
            "free_certificate": True,
            "interactive_practice": "https://www.kaggle.com/learn/intro-to-machine-learning",
            "interactive_practice_notes": "Kaggle notebooks + competitions provide real labeled data to practice on",
            "extra_practice": [
                "https://www.kaggle.com/competitions",   # enter Titanic or Playground competitions
                "https://www.fast.ai",                  # practical ML before theory
            ],
            "interview_preparation": "https://www.interviewbit.com/machine-learning-interview-questions/",
            "reference_book": "\"Hands-On Machine Learning with Scikit-Learn, Keras & TensorFlow\" by Aurélien Géron — companion notebooks free at https://github.com/ageron/handson-ml3",
            "project_ideas": [
                "House price predictor with feature engineering and cross-validation",
                "Spam email classifier comparing Naive Bayes, Logistic Regression, and Random Forest",
                "Customer churn prediction pipeline with preprocessing, training, and evaluation",
            ],
            "github_repos": [
                "https://github.com/ageron/handson-ml3",              # Géron's book notebooks
                "https://github.com/josephmisiti/awesome-machine-learning",
                "https://github.com/GokuMohandas/Made-With-ML",       # end-to-end ML engineering curriculum
            ],
        },
    },

    "deep learning": {
        "basics": {
            "docs": "https://pytorch.org/tutorials/",
            "docs_scope": "Learning PyTorch with Examples, Neural Networks tutorial, then Computer Vision or NLP tracks depending on focus",
            "style_guide": None,
            "video": "3Blue1Brown's \"Neural Networks\" series on YouTube (watch before writing any code)",
            "course": "fast.ai: Practical Deep Learning for Coders (free, no certificate)",
            "free_certificate": None,
            "interactive_practice": "https://www.kaggle.com/learn/intro-to-deep-learning",
            "interactive_practice_notes": "Kaggle's DL course uses real notebooks; free certificate",
            "extra_practice": [
                "https://playground.tensorflow.org",   # visual neural network builder in the browser
                "https://www.kaggle.com/competitions", # image classification competitions
            ],
            "interview_preparation": "https://www.interviewbit.com/deep-learning-interview-questions/",
            "reference_book": "\"Dive into Deep Learning\" — free interactive textbook at https://d2l.ai with PyTorch, JAX, and TensorFlow code",
            "project_ideas": [
                "Train a CNN image classifier on CIFAR-10 or a custom dataset",
                "Fine-tune a pre-trained ResNet for a binary classification task",
                "Build a character-level language model with an LSTM from scratch",
            ],
            "github_repos": [
                "https://github.com/d2l-ai/d2l-en",                    # Dive into Deep Learning source
                "https://github.com/fleuret/Little-Book-of-Deep-Learning",  # concise free PDF textbook
                "https://github.com/Atcold/pytorch-Deep-Learning",     # NYU DL course notebooks (Yann LeCun)
            ],
        },
    },

    "statistics": {
        "basics": {
            "docs": "https://www.khanacademy.org/math/statistics-probability",
            "docs_scope": "Descriptive statistics, probability, distributions, hypothesis testing, confidence intervals, regression",
            "style_guide": None,
            "video": "StatQuest with Josh Starmer on YouTube — Statistics Fundamentals playlist",
            "course": "Khan Academy Statistics & Probability (free, self-paced, no formal certificate)",
            "free_certificate": None,
            "interactive_practice": "https://www.khanacademy.org/math/statistics-probability",
            "interactive_practice_notes": "Khan Academy's exercises and mastery system are embedded in the course",
            "extra_practice": [
                "https://www.hackerrank.com/domains/mathematics/probability",
                "https://seeing-theory.brown.edu",   # Brown University's visual probability & stats book
            ],
            "interview_preparation": "https://www.interviewbit.com/statistics-interview-questions/",
            "reference_book": "\"Statistics\" by OpenStax — free PDF at https://openstax.org/details/books/statistics",
            "project_ideas": [
                "A/B test simulation: generate data, run a t-test, interpret p-value and effect size",
                "Visualize the Central Limit Theorem by sampling from skewed distributions",
                "Regression analysis on a public dataset with residual diagnostics",
            ],
            "github_repos": [
                "https://github.com/rasbt/stat-overview",              # concise stats cheat sheets
                "https://github.com/guipsamora/pandas_exercises",      # overlaps with data analysis, stats exercises
            ],
        },
    },

    "data engineering": {
        "basics": {
            "docs": "https://docs.getdbt.com/docs/introduction",
            "docs_scope": "Introduction, Quickstart, Models, Tests, Documentation, and Sources sections",
            "style_guide": "https://docs.getdbt.com/best-practices/how-we-style/0-how-we-style-our-dbt-projects",
            "video": "\"Data Engineering Zoomcamp\" by DataTalks.Club on YouTube (free cohort + recordings)",
            "course": "dbt Learn: dbt Fundamentals course (free, certificate free)",
            "free_certificate": True,
            "interactive_practice": "https://www.getdbt.com/dbt-learn/",
            "interactive_practice_notes": "dbt's own free learning platform with hands-on labs",
            "extra_practice": [
                "https://www.kaggle.com/learn/intro-to-sql",   # SQL foundation needed for DE
                "https://github.com/DataTalksClub/data-engineering-zoomcamp",  # full free DE curriculum with projects
            ],
            "interview_preparation": "https://www.interviewbit.com/data-engineering-interview-questions/",
            "project_ideas": [
                "ELT pipeline: ingest a public CSV to a local Postgres DB, transform with dbt, visualize with Metabase",
                "Build a simple Airflow DAG that downloads daily weather data and loads it to a data warehouse",
                "Batch processing pipeline using PySpark on a public dataset (NYC Taxi, or similar)",
            ],
            "github_repos": [
                "https://github.com/DataTalksClub/data-engineering-zoomcamp",  # full free course with projects
                "https://github.com/andkret/Cookbook",   # The Data Engineering Cookbook (free PDF)
                "https://github.com/igorbarinov/awesome-data-engineering",
            ],
        },
    },

    # ── Systems & Infrastructure ──────────────────────────────────────────────

    "system design": {
        "basics": {
            "docs": "https://github.com/donnemartin/system-design-primer",
            "docs_scope": "Scalability basics, load balancing, caching, databases (SQL vs NoSQL), consistency, CAP theorem, common interview patterns",
            "style_guide": None,
            "video": "Gaurav Sen's System Design playlist on YouTube",
            "course": "ByteByteGo newsletter (free tier) + Alex Xu's YouTube channel",
            "free_certificate": None,
            "interactive_practice": "https://www.hellointerview.com/learn/system-design/in-a-hurry/introduction",
            "interactive_practice_notes": "Free structured system design interview prep guide with worked examples",
            "extra_practice": [
                "https://systemdesign.one",    # free system design newsletter + case studies
                "https://roadmap.sh/system-design",
            ],
            "interview_preparation": "https://www.hellointerview.com",
            "project_ideas": [
                "Design and document a URL shortener (include DB schema, API contract, and scaling plan)",
                "Write a technical design doc for a notification service supporting email, SMS, and push",
                "Diagram a distributed rate limiter and explain the tradeoffs of token bucket vs sliding window",
            ],
            "github_repos": [
                "https://github.com/donnemartin/system-design-primer",      # the canonical reference
                "https://github.com/binhnguyennus/awesome-scalability",     # real-world scalability patterns
                "https://github.com/karanpratapsingh/system-design",        # free open-source book
            ],
        },
    },

    "docker": {
        "basics": {
            "docs": "https://docs.docker.com/get-started/",
            "docs_scope": "Parts 1–7: containers, images, volumes, networking, Docker Compose, and multi-container apps",
            "style_guide": "https://docs.docker.com/develop/develop-images/dockerfile_best-practices/",
            "video": "\"Docker Tutorial for Beginners\" by TechWorld with Nana on YouTube",
            "course": "Play With Docker classroom at labs.play-with-docker.com (free, browser-based, no install needed)",
            "free_certificate": None,
            "interactive_practice": "https://labs.play-with-docker.com",
            "interactive_practice_notes": "Free 4-hour Docker playground in the browser, resets after session",
            "extra_practice": [
                "https://training.play-with-docker.com",   # structured Docker labs
                "https://kodekloud.com/courses/docker-for-the-absolute-beginner/",  # free tier available
            ],
            "interview_preparation": "https://www.interviewbit.com/docker-interview-questions/",
            "project_ideas": [
                "Containerize a Python Flask or Node.js app with a multi-stage Dockerfile",
                "Write a Docker Compose file for a web app + Postgres + Redis stack",
                "Set up a local CI simulation using Docker: lint → test → build image in sequence",
            ],
            "github_repos": [
                "https://github.com/veggiemonk/awesome-docker",
                "https://github.com/docker/awesome-compose",  # official Docker Compose sample apps
            ],
        },
    },

    "cloud (aws)": {
        "basics": {
            "docs": "https://docs.aws.amazon.com/getting-started/",
            "docs_scope": "Core services: EC2, S3, IAM, Lambda, RDS, CloudWatch — Getting Started guides for each",
            "style_guide": "https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html",  # AWS Well-Architected Framework
            "video": "\"AWS Certified Cloud Practitioner\" full course by freeCodeCamp on YouTube",
            "course": "AWS Skill Builder: Cloud Practitioner Essentials (free to take, certificate exam paid separately)",
            "free_certificate": False,
            "interactive_practice": "https://aws.amazon.com/free/",
            "interactive_practice_notes": "AWS Free Tier: 12-month free access to 100+ services including EC2 t2.micro and S3",
            "extra_practice": [
                "https://www.cloudskillsboost.google",  # Google's free cloud training (useful for cloud-agnostic concepts)
                "https://acloudguru.com/blog/engineering/which-aws-certifications-are-most-valuable-in-2024",
            ],
            "interview_preparation": "https://www.interviewbit.com/aws-interview-questions/",
            "project_ideas": [
                "Host a static website on S3 with CloudFront CDN and a custom domain",
                "Build a serverless image resizing pipeline using Lambda + S3 triggers",
                "Set up a VPC with public and private subnets, NAT gateway, and an EC2 bastion host",
            ],
            "github_repos": [
                "https://github.com/donnemartin/awesome-aws",
                "https://github.com/open-guides/og-aws",   # practical, community-maintained AWS guide
            ],
        },
    },

    "devops": {
        "basics": {
            "docs": "https://roadmap.sh/devops",
            "docs_scope": "Follow the roadmap in order: Linux → Networking → Git → Docker → CI/CD → Kubernetes → Monitoring",
            "style_guide": "https://sre.google/books/",  # Google SRE books, free online
            "video": "\"DevOps Engineering Course for Beginners\" by freeCodeCamp on YouTube",
            "course": "Google's Site Reliability Engineering books (free at sre.google/books/)",
            "free_certificate": None,
            "interactive_practice": "https://labs.play-with-docker.com",
            "interactive_practice_notes": "Combine with Killercoda for free Kubernetes labs: https://killercoda.com",
            "extra_practice": [
                "https://killercoda.com",       # free browser-based Kubernetes + Linux labs
                "https://github.com/bregman-arie/devops-exercises",  # 2,600+ DevOps interview questions and exercises
            ],
            "interview_preparation": "https://github.com/bregman-arie/devops-exercises",
            "project_ideas": [
                "Set up a GitHub Actions CI/CD pipeline that runs tests, builds a Docker image, and pushes to Docker Hub",
                "Deploy a containerized app to a free Kubernetes cluster (use k3s locally or Civo's free tier)",
                "Implement infrastructure as code for a 3-tier app using Terraform's free local provider",
            ],
            "github_repos": [
                "https://github.com/bregman-arie/devops-exercises",
                "https://github.com/Tikam02/DevOps-Guide",
                "https://github.com/wmariuss/awesome-devops",
            ],
        },
    },

    "networking": {
        "basics": {
            "docs": "https://www.khanacademy.org/computing/computers-and-internet",
            "docs_scope": "How the Internet works, IP, DNS, TCP/IP, HTTP/HTTPS, routing, and firewalls",
            "style_guide": None,
            "video": "Professor Messer's CompTIA Network+ course on YouTube (free, full course)",
            "course": "Cisco Networking Academy: Networking Basics (free, certificate free)",
            "free_certificate": True,
            "interactive_practice": "https://www.netacad.com/courses/networking-basics",
            "interactive_practice_notes": "Cisco's Packet Tracer simulation tool is free with Netacad enrollment",
            "extra_practice": [
                "https://www.practiceexams.com/networking/",
                "https://gns3.com",   # free network simulator for more advanced practice
            ],
            "interview_preparation": "https://www.interviewbit.com/networking-interview-questions/",
            "reference_book": "\"Computer Networks: A Top-Down Approach\" by Kurose & Ross — lecture slides free at gaia.cs.umass.edu/kurose_ross/",
            "project_ideas": [
                "Build a port scanner in Python using raw sockets",
                "Set up a home DNS resolver using Pi-hole on a Raspberry Pi or VM",
                "Write a simple TCP chat server and client from scratch in Python",
            ],
            "github_repos": [
                "https://github.com/nyquist/awesome-networking",
                "https://github.com/facyber/awesome-networking",
            ],
        },
    },

    # ── AI Engineering ────────────────────────────────────────────────────────

    "llm / ai engineering": {
        "basics": {
            "docs": "https://platform.openai.com/docs/guides/prompt-engineering",
            "docs_scope": "Prompt engineering guide, function calling, embeddings, fine-tuning overview; supplement with Anthropic's prompt engineering docs at docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview",
            "style_guide": None,
            "video": "\"LangChain for LLM Application Development\" by DeepLearning.AI (free short course at learn.deeplearning.ai)",
            "course": "DeepLearning.AI Short Courses at learn.deeplearning.ai (free, no certificate)",
            "free_certificate": None,
            "interactive_practice": "https://github.com/anthropics/prompt-eng-interactive-tutorial",
            "interactive_practice_notes": "Anthropic's official prompt engineering tutorial — Jupyter notebooks, free",
            "extra_practice": [
                "https://learnprompting.org",   # open-source prompt engineering guide
                "https://www.promptingguide.ai", # DAIR.AI prompting guide
            ],
            "interview_preparation": "https://www.interviewbit.com/llm-interview-questions/",
            "project_ideas": [
                "RAG-based Q&A chatbot over your own documents using LangChain or LlamaIndex and a free model",
                "LLM-powered resume analyzer that extracts skills and suggests improvements",
                "Tool-calling agent that answers questions by routing to web search and a calculator",
            ],
            "github_repos": [
                "https://github.com/anthropics/prompt-eng-interactive-tutorial",
                "https://github.com/dair-ai/Prompt-Engineering-Guide",
                "https://github.com/tensorchord/Awesome-LLMOps",      # LLM deployment and ops
            ],
        },
    },

    "natural language processing": {
        "basics": {
            "docs": "https://huggingface.co/learn/nlp-course/chapter1/1",
            "docs_scope": "Chapters 1–7: transformers, tokenizers, fine-tuning, datasets library, and sharing models",
            "style_guide": None,
            "video": "\"Natural Language Processing with Python\" by freeCodeCamp on YouTube",
            "course": "Hugging Face NLP Course (free, certificate free)",
            "free_certificate": True,
            "interactive_practice": "https://huggingface.co/learn/nlp-course",
            "interactive_practice_notes": "Hugging Face course notebooks run in Google Colab for free",
            "extra_practice": [
                "https://www.kaggle.com/competitions?search=nlp",   # active NLP competitions with free compute
                "https://nltk.org/book/",   # free NLTK book for classical NLP foundations
            ],
            "interview_preparation": "https://www.interviewbit.com/nlp-interview-questions/",
            "reference_book": "\"Speech and Language Processing\" by Jurafsky & Martin — free draft at https://web.stanford.edu/~jurafsky/slp3/",
            "project_ideas": [
                "Sentiment analysis pipeline on Twitter/X data using a pre-trained transformer",
                "Named entity recognition (NER) system fine-tuned on a domain-specific dataset",
                "Text summarizer comparing extractive (TF-IDF) vs abstractive (BART/T5) approaches",
            ],
            "github_repos": [
                "https://github.com/keon/awesome-nlp",
                "https://github.com/huggingface/transformers",       # the canonical transformers library
                "https://github.com/explosion/spaCy",                # industrial-strength NLP library
            ],
        },
    },
}


# ── Aliases ────────────────────────────────────────────────────────────────────

_ALIASES = {
    "py": "python",
    "ml": "machine learning",
    "ai": "llm / ai engineering",
    "ds": "data structures",
    "dsa": "algorithms",
    "css": "html and css",
    "html": "html and css",
    "html/css": "html and css",
    "pandas": "data analysis",
    "numpy": "data analysis",
    "pytorch": "deep learning",
    "tensorflow": "deep learning",
    "keras": "deep learning",
    "scikit-learn": "machine learning",
    "sklearn": "machine learning",
    "nlp": "natural language processing",
    "llm": "llm / ai engineering",
    "aws": "cloud (aws)",
    "cloud": "cloud (aws)",
    "kubernetes": "devops",
    "k8s": "devops",
    "ci/cd": "devops",
    "rest": "rest apis",
    "api": "rest apis",
    "apis": "rest apis",
    "version control": "git",
    "github": "git",
    # new aliases to cover the expanded entries
    "shell": "linux",
    "bash": "linux",
    "command line": "linux",
    "cli": "linux",
    "node": "javascript",
    "node.js": "javascript",
    "ts": "javascript",          # typescript shares most fundamentals
    "vue": "react",              # close enough for fundamentals routing
    "svelte": "react",
    "data viz": "data analysis",
    "visualization": "data analysis",
    "seaborn": "data analysis",
    "matplotlib": "data analysis",
    "neural networks": "deep learning",
    "cnn": "deep learning",
    "rnn": "deep learning",
    "transformer": "natural language processing",
    "bert": "natural language processing",
    "gpt": "llm / ai engineering",
    "langchain": "llm / ai engineering",
    "llamaindex": "llm / ai engineering",
    "rag": "llm / ai engineering",
    "airflow": "data engineering",
    "spark": "data engineering",
    "kafka": "data engineering",
    "etl": "data engineering",
    "k8s": "devops",
    "terraform": "devops",
    "ansible": "devops",
    "jenkins": "devops",
    "tcp/ip": "networking",
    "http": "networking",
    "dns": "networking",
    "ec2": "cloud (aws)",
    "s3": "cloud (aws)",
    "lambda": "cloud (aws)",
    "oop": "python",
    "object oriented": "python",
    "design patterns": "java",
    "load balancing": "system design",
    "caching": "system design",
    "microservices": "system design",

    # ML / AI roles — common LLM outputs that need routing
    "data science": "machine learning",
    "data sciences": "machine learning",
    "ml algorithms": "machine learning",
    "machine learning algorithms": "machine learning",
    "machine learning models": "machine learning",
    "predictive modeling": "machine learning",
    "predictive modelling": "machine learning",
    "supervised learning": "machine learning",
    "unsupervised learning": "machine learning",
    "feature engineering": "machine learning",
    "model training": "machine learning",
    "model evaluation": "machine learning",
    "regression": "machine learning",
    "classification": "machine learning",
    "clustering": "machine learning",
    "computer vision": "deep learning",
    "cv": "deep learning",
    "object detection": "deep learning",
    "image recognition": "deep learning",
    "reinforcement learning": "deep learning",
    "rl": "deep learning",
    "mlops": "devops",
    "ml ops": "devops",
    "model deployment": "devops",
    "model serving": "devops",
    "a/b testing": "statistics",
    "hypothesis testing": "statistics",
    "probability": "statistics",
    "linear algebra": "statistics",
    "calculus": "statistics",
    "math": "statistics",
    "mathematics": "statistics",
    "statistical modeling": "statistics",
    "statistical modelling": "statistics",
    "time series": "machine learning",
    "time series analysis": "machine learning",
    "anomaly detection": "machine learning",
    "recommendation systems": "machine learning",
    "generative ai": "llm / ai engineering",
    "large language models": "llm / ai engineering",
    "prompt engineering": "llm / ai engineering",
    "fine-tuning": "llm / ai engineering",
    "fine tuning": "llm / ai engineering",
    "data preprocessing": "data analysis",
    "data wrangling": "data analysis",
    "data cleaning": "data analysis",
    "exploratory data analysis": "data analysis",
    "eda": "data analysis",
    "data collection": "data analysis",
    "web scraping": "python",
    "scripting": "python",
    "typescript": "javascript",
    "angular": "react",
    "next.js": "react",
    "nextjs": "react",
    "databases": "sql",
    "database": "sql",
    "postgresql": "sql",
    "mysql": "sql",
    "mongodb": "data engineering",
    "nosql": "data engineering",
    "redis": "system design",
    "message queues": "data engineering",
    "rabbitmq": "data engineering",
    "containerization": "docker",
    "containers": "docker",
    "virtual machines": "linux",
    "networking fundamentals": "networking",
    "computer networks": "networking",
}


def normalize_skill(skill: str) -> str:
    """Lowercase + strip so AI skill names match dictionary keys."""
    return skill.strip().lower()


def get_resources(skill: str) -> dict | None:
    """
    Look up curated resources for a skill.

    Normalises the input, checks aliases, then does an exact key match.
    Returns the resource dict (nested under 'basics') if found, None otherwise.
    """
    key = normalize_skill(skill)

    if not key:
        return None

    key = _ALIASES.get(key, key)
    return LEARNING_RESOURCES.get(key, None)


if __name__ == "__main__":
    import json
    print(json.dumps(get_resources("Python"), indent=2))
    print(json.dumps(get_resources("ML"), indent=2))
    print(json.dumps(get_resources("RAG"), indent=2))      # alias → llm / ai engineering
    print(json.dumps(get_resources("Kafka"), indent=2))    # alias → data engineering
    print(json.dumps(get_resources("Quantum Magic"), indent=2))  # → None
"""
Job simulations layer.

This is hand-picked, not something I'd trust an AI to generate — it'll
just make up simulations that don't actually exist. So instead of linking
to one specific module (which platforms retire all the time), I'm linking
to each platform's catalog/search page and leaving a note like
"search '[Role]' here" so the link doesn't go stale.

Two different things live in this file, and I'm keeping them separate
on purpose:

  JOB_SIMULATIONS       -> practice doing a watered-down version of the job
  INTERVIEW_SIMULATORS  -> practice the interview conversation itself

These test completely different skills, so don't let the UI blend them
together into one list.
"""

JOB_SIMULATIONS = {

    # ── Software Engineering ──────────────────────────────────────────────────

    "senior software engineer": [
        {"name": "Forage: Software Engineering career path", "link": "https://www.theforage.com/simulations?careers=software-engineering"},
        {"name": "JPMorgan Chase Software Engineering", "link": "https://www.theforage.com/simulations/jpmorgan/advanced-software-engineering-r0fm"},
        {"name": "Electronic Arts Software Engineering", "link": "https://www.theforage.com/simulations/electronic-arts/software-engineering-awbf"},
        {"name": "InterSECT Job Simulations", "link": "https://intersectjobsims.com/"},
    ],

    "software engineer": [
        {"name": "Forage: Software Engineering career path", "link": "https://www.theforage.com/simulations?careers=software-engineering"},
        {"name": "JPMorgan Chase Software Engineering", "link": "https://www.theforage.com/simulations/jpmorgan/advanced-software-engineering-r0fm"},
        {"name": "Electronic Arts Software Engineering", "link": "https://www.theforage.com/simulations/electronic-arts/software-engineering-awbf"},
        {"name": "Blackbird Software Engineering", "link": "https://www.theforage.com/simulations/blackbird/software-engineering-4mt9"},
        {"name": "InterSECT Job Simulations", "link": "https://intersectjobsims.com/"},
    ],

    "frontend engineer": [
        {"name": "Frontend Mentor (real design-to-code challenges)", "link": "https://www.frontendmentor.io/"},
        {"name": "GreatFrontEnd (frontend engineering interview prep)", "link": "https://www.greatfrontend.com/"},
        {"name": "Forage: Software Engineering career path", "link": "https://www.theforage.com/simulations?careers=software-engineering"},
    ],

    "backend engineer": [
        {"name": "Forage: Software Engineering career path", "link": "https://www.theforage.com/simulations?careers=software-engineering"},
        {"name": "JPMorgan Chase Software Engineering", "link": "https://www.theforage.com/simulations/jpmorgan/advanced-software-engineering-r0fm"},
        {"name": "InterSECT Job Simulations", "link": "https://intersectjobsims.com/"},
    ],

    "full stack engineer": [
        {"name": "Forage: Software Engineering career path", "link": "https://www.theforage.com/simulations?careers=software-engineering"},
        {"name": "Frontend Mentor", "link": "https://www.frontendmentor.io/"},
        {"name": "GreatFrontEnd", "link": "https://www.greatfrontend.com/"},
        {"name": "InterSECT Job Simulations", "link": "https://intersectjobsims.com/"},
    ],

    "mobile developer": [
        {"name": "Forage: Software Engineering career path", "link": "https://www.theforage.com/simulations?careers=software-engineering"},
        {"name": "InterSECT Job Simulations", "link": "https://intersectjobsims.com/"},
    ],

    "qa engineer": [
        {"name": "Frontend Mentor (build + test real UIs)", "link": "https://www.frontendmentor.io/"},
        {"name": "GreatFrontEnd", "link": "https://www.greatfrontend.com/"},
        {"name": "Forage: Software Engineering career path", "link": "https://www.theforage.com/simulations?careers=software-engineering"},
    ],

    # ── Data ──────────────────────────────────────────────────────────────────

    "data analyst": [
        {"name": "Forage: Browse all Data Analyst simulations", "link": "https://www.theforage.com/simulations?careers=data"},
        {"name": "Tata GenAI Powered Data Analytics", "link": "https://www.theforage.com/simulations/tata/data-analytics-t3zr"},
        {"name": "Kaggle Learn: Pandas + Data Visualisation", "link": "https://www.kaggle.com/learn"},
    ],

    "business intelligence analyst": [
        {"name": "Forage: Browse all Data Analyst simulations", "link": "https://www.theforage.com/simulations?careers=data"},
        {"name": "Kaggle Learn: SQL + Data Viz", "link": "https://www.kaggle.com/learn"},
    ],

    "data scientist": [
        {"name": "Kaggle Learn", "link": "https://www.kaggle.com/learn"},
        {"name": "Forage: Browse all Data Scientist simulations", "link": "https://www.theforage.com/simulations?careers=data"},
        {"name": "Kaggle Competitions (Titanic, Playground Series)", "link": "https://www.kaggle.com/competitions"},
        {"name": "Omdena (real-world collaborative ML projects)", "link": "https://omdena.com/"},
    ],

    "machine learning engineer": [
        {"name": "Kaggle Learn: Intro to ML + Intermediate ML", "link": "https://www.kaggle.com/learn"},
        {"name": "Omdena (real collaborative ML challenges)", "link": "https://omdena.com/"},
        {"name": "Kaggle Competitions", "link": "https://www.kaggle.com/competitions"},
        {"name": "Forage: Tech simulations", "link": "https://www.theforage.com/simulations"},
    ],

    "ai engineer": [
        {"name": "Kaggle Learn: AI tracks", "link": "https://www.kaggle.com/learn"},
        {"name": "Omdena (real collaborative AI projects)", "link": "https://omdena.com/"},
        {"name": "DeepLearning.AI Short Courses (hands-on AI engineering)", "link": "https://learn.deeplearning.ai/"},
        {"name": "Forage: Tech simulations", "link": "https://www.theforage.com/simulations"},
    ],

    "data engineer": [
        {"name": "DataTalks.Club Data Engineering Zoomcamp (free)", "link": "https://github.com/DataTalksClub/data-engineering-zoomcamp"},
        {"name": "Kaggle Learn: SQL", "link": "https://www.kaggle.com/learn/intro-to-sql"},
        {"name": "dbt Learn: dbt Fundamentals", "link": "https://www.getdbt.com/dbt-learn/"},
        {"name": "Forage: Software Engineering career path", "link": "https://www.theforage.com/simulations?careers=software-engineering"},
        {"name": "InterSECT Job Simulations", "link": "https://intersectjobsims.com/"},
    ],

    "quantitative analyst": [
        {"name": "Forage: Finance & banking simulations", "link": "https://www.theforage.com/simulations?careers=banking-and-financial-services"},
        {"name": "Kaggle Competitions (tabular prediction)", "link": "https://www.kaggle.com/competitions"},
        {"name": "Two Sigma Quantitative Finance (via Kaggle)", "link": "https://www.kaggle.com/c/two-sigma-financial-news"},
    ],

    # ── Infrastructure & Security ─────────────────────────────────────────────

    "cybersecurity analyst": [
        {"name": "Forage: Cybersecurity career path", "link": "https://www.theforage.com/simulations?careers=cybersecurity"},
        {"name": "TryHackMe (guided cybersecurity learning paths)", "link": "https://tryhackme.com/"},
        {"name": "PicoCTF (beginner-friendly CTF competitions)", "link": "https://picoctf.org/"},
        {"name": "CyberStart", "link": "https://www.cyberstart.com/"},
        {"name": "Hack The Box (intermediate/advanced)", "link": "https://www.hackthebox.com/"},
    ],

    "cloud engineer": [
        {"name": "AWS Skill Builder (free tier)", "link": "https://skillbuilder.aws/"},
        {"name": "Google Cloud Skills Boost", "link": "https://cloudskillsboost.google/"},
        {"name": "Microsoft Learn (Azure paths)", "link": "https://learn.microsoft.com/"},
        {"name": "Forage: Engineering or tech simulations", "link": "https://www.theforage.com/simulations"},
        {"name": "Play With Docker (free browser-based labs)", "link": "https://labs.play-with-docker.com/"},
    ],

    "devops engineer": [
        {"name": "AWS Skill Builder", "link": "https://skillbuilder.aws/"},
        {"name": "Killercoda (free Kubernetes + Linux labs)", "link": "https://killercoda.com/"},
        {"name": "Play With Docker", "link": "https://labs.play-with-docker.com/"},
        {"name": "Microsoft Learn (Azure DevOps)", "link": "https://learn.microsoft.com/"},
        {"name": "Forage: Software Engineering career path", "link": "https://www.theforage.com/simulations?careers=software-engineering"},
    ],

    "site reliability engineer": [
        {"name": "AWS Skill Builder", "link": "https://skillbuilder.aws/"},
        {"name": "Killercoda (free Kubernetes labs)", "link": "https://killercoda.com/"},
        {"name": "Microsoft Learn", "link": "https://learn.microsoft.com/"},
        {"name": "Forage: Software Engineering career path", "link": "https://www.theforage.com/simulations?careers=software-engineering"},
    ],

    # ── Business & Management ─────────────────────────────────────────────────

    "product manager": [
        {"name": "Forage: Browse all job simulations (search 'product')", "link": "https://www.theforage.com/simulations"},
        {"name": "InterSECT Job Simulations", "link": "https://intersectjobsims.com/"},
        {"name": "EntryLevel Product Management course (free tier)", "link": "https://www.entrylevel.net/"},
    ],

    "consulting": [
        {"name": "Forage: Browse all job simulations (search 'consulting')", "link": "https://www.theforage.com/simulations"},
        {"name": "McKinsey Forward Programme (free)", "link": "https://www.mckinsey.com/forward/overview"},
        {"name": "InterSECT Job Simulations", "link": "https://intersectjobsims.com/"},
    ],

    "technical program manager": [
        {"name": "Forage: Project / software / consulting simulations", "link": "https://www.theforage.com/simulations"},
        {"name": "Google Project Management Certificate (Coursera, audit free)", "link": "https://www.coursera.org/professional-certificates/google-project-management"},
        {"name": "InterSECT Job Simulations", "link": "https://intersectjobsims.com/"},
    ],

    # ── Design ────────────────────────────────────────────────────────────────

    "ux designer": [
        {"name": "Forage: UX / design simulations", "link": "https://www.theforage.com/simulations"},
        {"name": "Frontend Mentor (design handoff to code)", "link": "https://www.frontendmentor.io/"},
        {"name": "Google UX Design Certificate (Coursera, audit free)", "link": "https://www.coursera.org/professional-certificates/google-ux-design"},
        {"name": "Figma Community challenges", "link": "https://www.figma.com/community/"},
    ],

    # ── General ───────────────────────────────────────────────────────────────

    "entry-level tech generalist": [
        {"name": "Forage: Free job simulations catalog", "link": "https://www.theforage.com/simulations"},
        {"name": "InterSECT Job Simulations", "link": "https://intersectjobsims.com/"},
        {"name": "EntryLevel (multiple tracks, free tier)", "link": "https://www.entrylevel.net/"},
    ],
}


INTERVIEW_SIMULATORS = [
    # Technical & coding
    {"name": "Interviewing.io (mock technical interviews)", "link": "https://interviewing.io/"},
    {"name": "Pramp (free peer-to-peer mock interviews)", "link": "https://www.pramp.com/"},
    {"name": "OnlineInterview.io", "link": "https://onlineinterview.io/"},
    {"name": "Intervu.dev", "link": "https://intervu.dev/"},

    # AI-driven behavioral & general
    {"name": "Google Interview Warmup (behavioral, free)", "link": "https://grow.google/certificates/interview-warmup/"},
    {"name": "Codecademy Interview Simulator", "link": "https://www.codecademy.com/interview-simulator"},
    {"name": "InterviewSchool AI Simulator", "link": "https://interviewsimulator.io/"},
    {"name": "FreeMockInterview.com", "link": "https://freemockinterview.com/"},

    # No-signup / quick practice
    {"name": "NoBsResume Interview Simulator", "link": "https://nobsresume.com/interview/english"},
]


# ── Role matching ─────────────────────────────────────────────────────────────
# Maps keyword phrases → canonical JOB_SIMULATIONS keys.
#
# ORDER MATTERS — more specific phrases must come before broader ones.
# The matching algorithm picks the LONGEST keyword that matches, so
# "machine learning engineer" (3 words) beats "machine learning" (2 words)
# automatically regardless of order here. But it's still good practice
# to list specific roles first for readability.
#
# Every key here MUST exist in JOB_SIMULATIONS — if you add a new key
# here, add a matching entry there too, or the match silently returns [].

_ROLE_KEYWORDS = {
    # ── Most specific first ───────────────────────────────────────────────────

    "site reliability engineer": [
        "site reliability engineer", "sre"
    ],

    "machine learning engineer": [
        "machine learning engineer", "ml engineer", "mlops engineer",
        "model engineer", "mlops"
    ],

    "senior software engineer": [
        "senior software engineer", "staff software engineer",
        "principal software engineer", "lead software engineer",
        "sr software engineer", "swe ii", "swe 2", "swe iii", "swe 3",
        "senior swe", "staff swe"
    ],

    # Note: senior SWE roles map to the same simulations as mid-level —
    # Forage targets all experience levels under the same tracks.

    "full stack engineer": [
        "full stack engineer", "fullstack engineer",
        "full stack developer", "fullstack developer", "full-stack"
    ],

    "frontend engineer": [
        "frontend engineer", "front end engineer", "front-end engineer",
        "ui engineer", "web engineer", "javascript engineer", "react engineer",
        "frontend developer", "front end developer"
    ],

    "backend engineer": [
        "backend engineer", "back end engineer", "back-end engineer",
        "api engineer", "server engineer", "backend developer"
    ],

    "mobile developer": [
        "mobile developer", "mobile engineer", "ios engineer",
        "android engineer", "flutter developer", "react native developer",
        "mobile app"
    ],

    "technical program manager": [
        "technical program manager", "tpm", "technical project manager"
    ],

    "business intelligence analyst": [
        "business intelligence analyst", "bi analyst",
        "business intelligence engineer", "bi engineer", "bi developer"
    ],

    "quantitative analyst": [
        "quantitative analyst", "quant analyst", "quantitative researcher",
        "quant researcher", "quantitative developer", "quant developer",
        "quantitative trader", "quant trader"
        # intentionally no bare "quant" — it's a substring of "quantum", "quantity", etc.
    ],

    "data engineer": [
        "data engineer", "analytics engineer", "etl engineer",
        "pipeline engineer", "data platform engineer", "data infrastructure"
    ],

    "data scientist": [
        "data scientist", "applied scientist", "research scientist",
        "decision scientist"
    ],

    "data analyst": [
        "data analyst", "analytics analyst", "business analyst",
        "data reporting", "analytics associate"
    ],

    "cybersecurity analyst": [
        "cybersecurity analyst", "cyber security analyst", "security analyst",
        "soc analyst", "security engineer", "blue team", "threat analyst",
        "information security", "infosec", "cybersecurity engineer"
    ],

    "devops engineer": [
        "devops engineer", "devops", "build engineer",
        "release engineer", "platform engineer", "infrastructure engineer"
    ],

    "cloud engineer": [
        "cloud engineer", "cloud platform engineer",
        "cloud architect", "cloud developer", "aws engineer", "gcp engineer",
        "azure engineer"
    ],

    "ai engineer": [
        "ai engineer", "artificial intelligence engineer",
        "llm engineer", "genai engineer", "generative ai engineer",
        "ai/ml engineer", "ai developer", "machine learning", "deep learning",
        "ai researcher"
    ],

    "software engineer": [
        "software engineer", "software developer", "swe",
        "application engineer", "product engineer",
        "software engineering intern", "swe intern",
        "software engineer intern", "software developer intern"
    ],

    "product manager": [
        "product manager", "product management", "pm", "associate pm",
        "apm", "product lead", "product owner"
    ],

    "consulting": [
        "consulting", "consultant", "strategy intern",
        "management consulting", "technology consulting",
        "business consulting", "advisory"
    ],

    "qa engineer": [
        "qa engineer", "quality assurance", "test engineer",
        "software test engineer", "sdet", "automation tester",
        "quality engineer"
    ],

    "ux designer": [
        "ux designer", "ui designer", "ux/ui designer", "ui/ux designer",
        "product designer", "interaction designer", "user experience designer",
        "ux researcher", "design intern"
    ],

    "entry-level tech generalist": [
        "entry level", "entry-level", "associate engineer",
        "junior developer", "new grad", "graduate engineer",
        "early career"
    ],
}


def _match_role(role: str) -> str | None:
    """
    Map free-typed role text to a canonical JOB_SIMULATIONS key.

    Finds ALL keyword matches and returns the one with the LONGEST matching
    keyword — this naturally prefers specific matches over broad ones.
    Example: "machine learning engineer" (25 chars) beats "machine learning"
    (16 chars) even if the shorter one appears first in the dict.

    Returns None if nothing is close enough.
    """
    text = role.strip().lower()
    if not text:
        return None

    best_key = None
    best_length = 0

    for canonical_key, keywords in _ROLE_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text and len(keyword) > best_length:
                best_length = len(keyword)
                best_key = canonical_key

    return best_key


def get_simulations(role: str) -> list[dict]:
    """
    Look up curated job simulations for a given role.

    Takes whatever messy text the user typed in, tries to match it to one
    of the roles I've curated, and returns that list. If nothing matches,
    returns an empty list — the UI should point people to search
    Forage/Kaggle directly rather than show a wrong recommendation.

    Returns:
        list[dict] — each item looks like {"name": str, "link": str}.
        Empty list means "nothing curated yet for this role."
    """
    matched_key = _match_role(role)
    if matched_key is None:
        return []
    return JOB_SIMULATIONS.get(matched_key, [])


def get_interview_simulators() -> list[dict]:
    """Return the full list of interview practice platforms."""
    return INTERVIEW_SIMULATORS


if __name__ == "__main__":
    test_roles = [
        "AI Engineer",
        "SWE Intern at Meta",
        "machine learning engineer at Google",  # was wrongly matching "ai engineer" before
        "Senior Software Engineer",              # was silently returning [] before
        "Product Manager at Apple",             # was silently returning [] before
        "UX Designer",                          # new category
        "Quantitative Analyst at a hedge fund", # new category
        "Quantum Wizard",                        # no match → []
    ]

    for role in test_roles:
        result = get_simulations(role)
        print(f"{role!r:45} → {len(result)} simulation(s)")




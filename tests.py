"""
Test suite for the Career Coach app.

HOW TO RUN:
    cd DuckPath
    python -m pytest tests.py -v

The -v flag means "verbose" — it prints each test name and PASSED/FAILED
instead of just dots. Much easier to read.

HOW TO READ THE OUTPUT:
    PASSED = test worked correctly
    FAILED = something is broken (or the function is still a stub)
    ERROR  = Python crashed before the test could even run

WHAT "stub" means in the comments below:
    Several functions are not finished yet (they say "raise NotImplementedError").
    Tests for those functions are marked # STUB — they will FAIL now and PASS
    once you implement the function. That's expected and correct. When all tests
    pass, your implementation is done.

NO INTERNET NEEDED:
    Tests that call the real API or real AI are replaced with "mocks" —
    fake versions of the network call that return pretend data. This means
    tests run instantly and don't eat your rate limits.
"""

import json
import requests
import pytest
from unittest.mock import patch, MagicMock

# ── Imports from our own files ────────────────────────────────────────────────
from resources import LEARNING_RESOURCES, normalize_skill, get_resources
from simulations import JOB_SIMULATIONS, INTERVIEW_SIMULATORS, get_simulations
from practice import PRACTICE_RESOURCES, get_practice
from outreach import COLD_EMAIL_TEMPLATE, OUTREACH_QUESTIONS, build_outreach_kit
from analysis import rank_skills, analyze_postings
from jobs import fetch_postings


# ══════════════════════════════════════════════════════════════════════════════
# resources.py
# ══════════════════════════════════════════════════════════════════════════════

class TestLearningResourcesData:
    """Validate the LEARNING_RESOURCES dictionary is correctly shaped.

    These tests run against the raw data — no functions needed. They catch
    typos like a missing key or a wrong type for free_certificate.
    """

    REQUIRED_KEYS = {"docs", "video", "course", "free_certificate"}

    def test_dict_is_not_empty(self):
        assert len(LEARNING_RESOURCES) > 0, "LEARNING_RESOURCES is empty — add entries"

    def test_every_entry_has_required_keys(self):
        for skill, entry in LEARNING_RESOURCES.items():
            missing = self.REQUIRED_KEYS - set(entry.keys())
            assert not missing, f"'{skill}' is missing keys: {missing}"

    def test_free_certificate_is_bool_or_none(self):
        # True = cert is free, False = audit free but cert costs money, None = no cert
        for skill, entry in LEARNING_RESOURCES.items():
            val = entry["free_certificate"]
            assert isinstance(val, (bool, type(None))), (
                f"'{skill}': free_certificate must be True, False, or None — got {val!r}"
            )

    def test_docs_is_a_non_empty_string(self):
        for skill, entry in LEARNING_RESOURCES.items():
            assert isinstance(entry["docs"], str) and entry["docs"].strip(), (
                f"'{skill}': docs must be a non-empty string"
            )

    def test_video_is_a_non_empty_string(self):
        for skill, entry in LEARNING_RESOURCES.items():
            assert isinstance(entry["video"], str) and entry["video"].strip(), (
                f"'{skill}': video must be a non-empty string"
            )

    def test_course_is_a_non_empty_string(self):
        for skill, entry in LEARNING_RESOURCES.items():
            assert isinstance(entry["course"], str) and entry["course"].strip(), (
                f"'{skill}': course must be a non-empty string"
            )

    def test_all_keys_are_lowercase(self):
        # Keys must be lowercase so normalize_skill() can match them
        for skill in LEARNING_RESOURCES:
            assert skill == skill.lower(), (
                f"Key '{skill}' is not lowercase — normalize_skill() won't find it"
            )


class TestNormalizeSkill:
    """normalize_skill() is already implemented — these should all pass now."""

    def test_lowercases_input(self):
        assert normalize_skill("Python") == "python"

    def test_strips_leading_whitespace(self):
        assert normalize_skill("  python") == "python"

    def test_strips_trailing_whitespace(self):
        assert normalize_skill("python  ") == "python"

    def test_strips_both_ends(self):
        assert normalize_skill("  SQL  ") == "sql"

    def test_multi_word_skill(self):
        assert normalize_skill("Data Analysis") == "data analysis"

    def test_already_normalised_passes_through(self):
        assert normalize_skill("python") == "python"

    def test_empty_string(self):
        assert normalize_skill("") == ""

    def test_only_whitespace(self):
        assert normalize_skill("   ") == ""


class TestGetResources:
    """
    get_resources() is a STUB — these tests will FAIL until Phase 4 is done.
    They define the contract your implementation must satisfy.
    """

    def test_exact_lowercase_match(self):
        # "python" is in LEARNING_RESOURCES — must find it
        result = get_resources("python")
        assert result is not None

    def test_case_insensitive_match(self):
        # The user/AI might type "Python" — must still find it
        result = get_resources("Python")
        assert result is not None

    def test_strips_whitespace(self):
        result = get_resources("  python  ")
        assert result is not None

    def test_returns_dict_with_required_keys(self):
        result = get_resources("python")
        assert isinstance(result, dict)
        for key in ("docs", "video", "course", "free_certificate"):
            assert key in result, f"result is missing key '{key}'"

    def test_unknown_skill_returns_none(self):
        result = get_resources("quantum brain surgery")
        assert result is None

    def test_empty_string_returns_none(self):
        result = get_resources("")
        assert result is None

    def test_known_multi_word_skill(self):
        # "data analysis" is in LEARNING_RESOURCES
        result = get_resources("data analysis")
        assert result is not None

    def test_multi_word_case_insensitive(self):
        result = get_resources("Data Analysis")
        assert result is not None


# ══════════════════════════════════════════════════════════════════════════════
# simulations.py
# ══════════════════════════════════════════════════════════════════════════════

class TestSimulationsData:
    """Validate JOB_SIMULATIONS and INTERVIEW_SIMULATORS data shape."""

    def test_job_simulations_is_not_empty(self):
        assert len(JOB_SIMULATIONS) > 0

    def test_every_simulation_has_name_and_link(self):
        for role, sims in JOB_SIMULATIONS.items():
            assert isinstance(sims, list), f"'{role}' value must be a list"
            for sim in sims:
                assert "name" in sim, f"simulation under '{role}' missing 'name'"
                assert "link" in sim, f"simulation under '{role}' missing 'link'"

    def test_all_links_start_with_http(self):
        for role, sims in JOB_SIMULATIONS.items():
            for sim in sims:
                assert sim["link"].startswith("http"), (
                    f"'{role}' → '{sim['name']}': link must start with http"
                )

    def test_interview_simulators_is_a_list(self):
        assert isinstance(INTERVIEW_SIMULATORS, list)

    def test_interview_simulators_not_empty(self):
        assert len(INTERVIEW_SIMULATORS) > 0

    def test_every_interview_simulator_has_name_and_link(self):
        for sim in INTERVIEW_SIMULATORS:
            assert "name" in sim
            assert "link" in sim
            assert sim["link"].startswith("http")


class TestGetSimulations:
    """
    get_simulations() is a STUB — these tests will FAIL until Phase 7 is done.
    """

    def test_known_role_returns_a_list(self):
        result = get_simulations("AI Engineer")
        assert isinstance(result, list)

    def test_known_role_returns_non_empty_list(self):
        result = get_simulations("AI Engineer")
        assert len(result) > 0

    def test_each_result_has_name_and_link(self):
        result = get_simulations("AI Engineer")
        for sim in result:
            assert "name" in sim
            assert "link" in sim

    def test_unknown_role_returns_empty_list(self):
        # Not [] means the UI would show a wrong simulation — must be strictly []
        result = get_simulations("professional interpretive dancer")
        assert result == []

    def test_case_insensitive(self):
        lower = get_simulations("ai engineer")
        upper = get_simulations("AI ENGINEER")
        assert lower == upper

    def test_returns_list_not_none(self):
        # Must return [] on no match, not None — callers iterate the result
        result = get_simulations("something completely unknown xyz")
        assert result is not None
        assert isinstance(result, list)


# ══════════════════════════════════════════════════════════════════════════════
# practice.py
# ══════════════════════════════════════════════════════════════════════════════

class TestPracticeResourcesData:
    """Validate the PRACTICE_RESOURCES dictionary."""

    def test_not_empty(self):
        assert len(PRACTICE_RESOURCES) > 0

    def test_every_category_is_a_non_empty_list(self):
        for category, items in PRACTICE_RESOURCES.items():
            assert isinstance(items, list), f"'{category}' must be a list"
            assert len(items) > 0, f"'{category}' list is empty"

    def test_every_item_is_a_non_empty_string(self):
        for category, items in PRACTICE_RESOURCES.items():
            for item in items:
                assert isinstance(item, str) and item.strip(), (
                    f"'{category}' contains an empty or non-string item"
                )


class TestGetPractice:
    """
    get_practice() is a STUB — these tests will FAIL until Phase 5 is done.
    """

    def test_known_category_returns_list(self):
        result = get_practice("coding_interviews")
        assert isinstance(result, list)

    def test_known_category_returns_non_empty_list(self):
        result = get_practice("coding_interviews")
        assert len(result) > 0

    def test_each_item_is_a_string(self):
        result = get_practice("coding_interviews")
        for item in result:
            assert isinstance(item, str)

    def test_unknown_category_returns_empty_list(self):
        result = get_practice("something_that_does_not_exist")
        assert result == []

    def test_empty_string_returns_empty_list(self):
        result = get_practice("")
        assert result == []

    def test_system_design_category_works(self):
        result = get_practice("system_design")
        assert isinstance(result, list)
        assert len(result) > 0

    def test_behavioral_category_works(self):
        result = get_practice("behavioral")
        assert isinstance(result, list)
        assert len(result) > 0


# ══════════════════════════════════════════════════════════════════════════════
# outreach.py
# ══════════════════════════════════════════════════════════════════════════════

class TestOutreachData:
    """Validate the hand-written outreach constants."""

    def test_cold_email_has_name_placeholder(self):
        assert "{name}" in COLD_EMAIL_TEMPLATE

    def test_cold_email_has_role_placeholder(self):
        assert "{role}" in COLD_EMAIL_TEMPLATE

    def test_cold_email_has_company_placeholder(self):
        assert "{company}" in COLD_EMAIL_TEMPLATE

    def test_cold_email_has_your_name_placeholder(self):
        assert "{your_name}" in COLD_EMAIL_TEMPLATE

    def test_cold_email_template_is_not_blank(self):
        assert len(COLD_EMAIL_TEMPLATE.strip()) > 50

    def test_outreach_questions_is_a_list(self):
        assert isinstance(OUTREACH_QUESTIONS, list)

    def test_outreach_questions_has_at_least_two(self):
        assert len(OUTREACH_QUESTIONS) >= 2, (
            "Add at least 2 outreach questions — you only have "
            f"{len(OUTREACH_QUESTIONS)}"
        )

    def test_every_question_is_a_non_empty_string(self):
        for q in OUTREACH_QUESTIONS:
            assert isinstance(q, str) and q.strip()


class TestBuildOutreachKit:
    """
    build_outreach_kit() is a STUB — these tests will FAIL until Phase 8 is done.
    """

    def test_returns_a_dict(self):
        result = build_outreach_kit("AI Engineer", "Google")
        assert isinstance(result, dict)

    def test_has_linkedin_terms_key(self):
        result = build_outreach_kit("AI Engineer", "Google")
        assert "linkedin_terms" in result

    def test_linkedin_terms_is_a_non_empty_list(self):
        result = build_outreach_kit("AI Engineer", "Google")
        assert isinstance(result["linkedin_terms"], list)
        assert len(result["linkedin_terms"]) > 0

    def test_has_questions_key(self):
        result = build_outreach_kit("AI Engineer", "Google")
        assert "questions" in result

    def test_has_email_template_key(self):
        result = build_outreach_kit("AI Engineer", "Google")
        assert "email_template" in result

    def test_email_template_is_a_string(self):
        result = build_outreach_kit("AI Engineer", "Google")
        assert isinstance(result["email_template"], str)

    def test_company_name_appears_in_linkedin_terms(self):
        result = build_outreach_kit("AI Engineer", "Google")
        combined = " ".join(result["linkedin_terms"]).lower()
        assert "google" in combined

    def test_default_company_works(self):
        # company has a default so calling with just role must not crash
        result = build_outreach_kit("AI Engineer")
        assert isinstance(result, dict)


# ══════════════════════════════════════════════════════════════════════════════
# analysis.py — rank_skills (IMPLEMENTED)
# ══════════════════════════════════════════════════════════════════════════════

class TestRankSkills:
    """rank_skills() is fully implemented — all of these must pass right now."""

    def test_most_frequent_skill_comes_first(self):
        result = rank_skills([["Python", "SQL"], ["python", "SQL"], ["python"]])
        assert result[0] == "python"

    def test_second_most_frequent_is_second(self):
        result = rank_skills([["Python", "SQL"], ["python", "SQL"], ["python"]])
        assert result[1] == "sql"

    def test_output_has_no_duplicates(self):
        result = rank_skills([["Python", "SQL"], ["python", "SQL"]])
        assert len(result) == len(set(result)), "Output contains duplicate skills"

    def test_normalises_whitespace(self):
        # "Python " and "python" must count as the same skill
        result = rank_skills([["Python  ", "python"]])
        assert result == ["python"]

    def test_normalises_to_lowercase(self):
        result = rank_skills([["SQL"], ["sql"], ["SQL"]])
        assert result == ["sql"]

    def test_empty_input_returns_empty_list(self):
        assert rank_skills([]) == []

    def test_single_sublist(self):
        result = rank_skills([["Python", "SQL", "Git"]])
        assert set(result) == {"python", "sql", "git"}

    def test_single_skill_repeated(self):
        result = rank_skills([["Python"], ["Python"], ["Python"]])
        assert result == ["python"]

    def test_all_unique_skills_all_appear(self):
        result = rank_skills([["Python", "SQL", "Git"]])
        assert len(result) == 3

    def test_empty_sublists_ignored(self):
        result = rank_skills([[], ["Python"], []])
        assert result == ["python"]

    def test_mixed_real_data(self):
        # Mirrors the smoke test in analysis.py
        mock_data = [
            ["Python", "SQL", "Communication"],
            ["python ", "AWS", "SQL"],
            ["Docker", "Python", "Kubernetes"],
        ]
        result = rank_skills(mock_data)
        assert result[0] == "python"    # appears 3 times
        assert result[1] == "sql"       # appears 2 times
        assert "aws" in result
        assert "docker" in result
        assert "kubernetes" in result
        assert "communication" in result


# ══════════════════════════════════════════════════════════════════════════════
# analysis.py — analyze_postings (IMPLEMENTED, uses LLM — mocked)
# ══════════════════════════════════════════════════════════════════════════════

class TestAnalyzePostings:
    """
    analyze_postings() calls the real LLM. We replace the LLM with a fake
    (a "mock") so tests run instantly and never spend API credits.

    The mock returns a pre-written JSON string exactly as the real LLM would.
    """

    FAKE_AI_RESPONSE = json.dumps({
        "core_skills": ["Python", "SQL", "pandas"],
        "interview_focus": ["LeetCode mediums", "SQL window functions"],
        "experience_signals": ["Tableau", "AWS"],
    })

    def _make_mock_response(self):
        mock = MagicMock()
        mock.choices[0].message.content = self.FAKE_AI_RESPONSE
        return mock

    def test_empty_descriptions_returns_empty_contract(self):
        # Guard clause — must NOT call the AI at all
        result = analyze_postings("Data Analyst", [])
        assert result == {
            "core_skills": [],
            "interview_focus": [],
            "experience_signals": [],
        }

    def test_returns_dict(self):
        with patch("analysis.client.chat.completions.create",
                   return_value=self._make_mock_response()):
            result = analyze_postings("Data Analyst", ["Python and SQL required"])
        assert isinstance(result, dict)

    def test_has_core_skills_key(self):
        with patch("analysis.client.chat.completions.create",
                   return_value=self._make_mock_response()):
            result = analyze_postings("Data Analyst", ["Python and SQL required"])
        assert "core_skills" in result

    def test_has_interview_focus_key(self):
        with patch("analysis.client.chat.completions.create",
                   return_value=self._make_mock_response()):
            result = analyze_postings("Data Analyst", ["Python and SQL required"])
        assert "interview_focus" in result

    def test_has_experience_signals_key(self):
        with patch("analysis.client.chat.completions.create",
                   return_value=self._make_mock_response()):
            result = analyze_postings("Data Analyst", ["Python and SQL required"])
        assert "experience_signals" in result

    def test_core_skills_is_a_list(self):
        with patch("analysis.client.chat.completions.create",
                   return_value=self._make_mock_response()):
            result = analyze_postings("Data Analyst", ["Python and SQL required"])
        assert isinstance(result["core_skills"], list)

    def test_multiple_descriptions_are_bundled(self):
        # Verify that multiple descriptions are joined and sent as one call
        with patch("analysis.client.chat.completions.create",
                   return_value=self._make_mock_response()) as mock_create:
            analyze_postings("Data Analyst", ["Posting one", "Posting two"])
        call_args = mock_create.call_args
        user_content = call_args[1]["messages"][1]["content"]
        assert "Posting one" in user_content
        assert "Posting two" in user_content

    def test_role_is_included_in_prompt(self):
        with patch("analysis.client.chat.completions.create",
                   return_value=self._make_mock_response()) as mock_create:
            analyze_postings("Senior Data Analyst", ["Some posting"])
        call_args = mock_create.call_args
        user_content = call_args[1]["messages"][1]["content"]
        assert "Senior Data Analyst" in user_content


# ══════════════════════════════════════════════════════════════════════════════
# jobs.py — fetch_postings (IMPLEMENTED, uses HTTP — mocked)
# ══════════════════════════════════════════════════════════════════════════════

class TestFetchPostings:
    """
    fetch_postings() calls the JSearch API over the internet. We mock
    requests.get so tests never touch the network.
    """

    def _make_ok_response(self, descriptions: list[str]) -> MagicMock:
        mock = MagicMock()
        mock.status_code = 200
        mock.json.return_value = {
            "data": [{"job_description": d} for d in descriptions]
        }
        return mock

    def test_success_returns_list_of_strings(self):
        with patch("jobs.requests.get", return_value=self._make_ok_response(["desc 1", "desc 2"])):
            result = fetch_postings("Data Analyst")
        assert isinstance(result, list)
        assert all(isinstance(d, str) for d in result)

    def test_descriptions_match_api_data(self):
        with patch("jobs.requests.get", return_value=self._make_ok_response(["Python required", "SQL needed"])):
            result = fetch_postings("Data Analyst")
        assert result[0] == "Python required"
        assert result[1] == "SQL needed"

    def test_bad_status_code_returns_empty_list(self):
        mock = MagicMock()
        mock.status_code = 401
        with patch("jobs.requests.get", return_value=mock):
            result = fetch_postings("Data Analyst")
        assert result == []

    def test_500_error_returns_empty_list(self):
        mock = MagicMock()
        mock.status_code = 500
        with patch("jobs.requests.get", return_value=mock):
            result = fetch_postings("Data Analyst")
        assert result == []

    def test_network_exception_returns_empty_list(self):
        with patch("jobs.requests.get", side_effect=requests.RequestException("timeout")):
            result = fetch_postings("Data Analyst")
        assert result == []

    def test_missing_data_key_returns_empty_list(self):
        mock = MagicMock()
        mock.status_code = 200
        mock.json.return_value = {"status": "OK"}  # no "data" key
        with patch("jobs.requests.get", return_value=mock):
            result = fetch_postings("Data Analyst")
        assert result == []

    def test_empty_data_list_returns_empty_list(self):
        mock = MagicMock()
        mock.status_code = 200
        mock.json.return_value = {"data": []}
        with patch("jobs.requests.get", return_value=mock):
            result = fetch_postings("Data Analyst")
        assert result == []

    def test_skips_jobs_with_no_description(self):
        mock = MagicMock()
        mock.status_code = 200
        mock.json.return_value = {
            "data": [
                {"job_description": "Real description"},
                {"job_description": None},        # missing — must be skipped
                {"job_description": ""},           # blank — must be skipped
                {"job_description": "Another one"},
            ]
        }
        with patch("jobs.requests.get", return_value=mock):
            result = fetch_postings("Data Analyst")
        assert len(result) == 2
        assert "Real description" in result
        assert "Another one" in result

    def test_respects_postings_to_analyze_limit(self):
        from config import POSTINGS_TO_ANALYZE
        many = [f"posting {i}" for i in range(POSTINGS_TO_ANALYZE + 10)]
        with patch("jobs.requests.get", return_value=self._make_ok_response(many)):
            result = fetch_postings("Data Analyst")
        assert len(result) <= POSTINGS_TO_ANALYZE

"""
Tests for busca_vagas_junior.py
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# noqa: E402

from busca_vagas_junior import (  # noqa: E402
    is_relevant_junior,
    is_valid_location,
    parse_relative_date,
    is_within_two_weeks,
)


class TestIsRelevantJunior:
    """Tests for is_relevant_junior function"""

    def test_junior_java_developer(self):
        assert is_relevant_junior("Junior Java Developer") is True

    def test_jr_java_backend(self):
        assert is_relevant_junior("Jr Java Backend Developer") is True

    def test_estagiario_java(self):
        assert is_relevant_junior("Estagiario Java") is True

    def test_trainee_software(self):
        assert is_relevant_junior("Trainee Software Engineer Java") is True

    def test_pleno_backend(self):
        assert is_relevant_junior("Desenvolvedor Backend Pleno") is True

    def test_entry_level_java(self):
        assert is_relevant_junior("Entry Level Java Developer") is True

    def test_senior_java_should_exclude(self):
        assert is_relevant_junior("Senior Java Developer") is False

    def test_tech_lead_should_exclude(self):
        assert is_relevant_junior("Tech Lead Java") is False

    def test_frontend_should_exclude(self):
        assert is_relevant_junior("Junior Frontend Developer") is False

    def test_php_should_exclude(self):
        assert is_relevant_junior("Junior PHP Developer") is False

    def test_node_should_exclude(self):
        assert is_relevant_junior("Junior Node.js Developer") is False

    def test_react_should_exclude(self):
        assert is_relevant_junior("Junior React Developer") is False

    def test_mobile_should_exclude(self):
        assert is_relevant_junior("Junior Mobile Developer") is False

    def test_spring_boot_junior(self):
        assert is_relevant_junior("Junior Spring Boot Developer") is True

    def test_backend_junior(self):
        assert is_relevant_junior("Backend Junior") is True

    def test_empty_title(self):
        assert is_relevant_junior("") is False

    def test_senior_with_junior_keyword(self):
        assert is_relevant_junior("Senior Developer Junior") is False


class TestIsValidLocation:
    """Tests for is_valid_location function"""

    def test_remoto(self):
        assert is_valid_location("Remoto") is True

    def test_sao_paulo(self):
        assert is_valid_location("Sao Paulo, SP") is True

    def test_sao_paulo_with_accent(self):
        assert is_valid_location("São Paulo, SP") is True

    def test_brasil(self):
        assert is_valid_location("Brasil") is True

    def test_home_office(self):
        assert is_valid_location("Home Office") is True

    def test_hibrido(self):
        assert is_valid_location("Hibrido") is True

    def test_india_should_exclude(self):
        assert is_valid_location("India") is False

    def test_usa_should_exclude(self):
        assert is_valid_location("USA") is False

    def test_estados_unidos_should_exclude(self):
        assert is_valid_location("Estados Unidos") is False

    def test_europa_should_exclude(self):
        assert is_valid_location("Europa") is False

    def test_empty_location(self):
        assert is_valid_location("") is True

    def test_none_location(self):
        assert is_valid_location(None) is True


class TestParseRelativeDate:
    """Tests for parse_relative_date function"""

    def test_hoje(self):
        result = parse_relative_date("hoje")
        assert result is not None
        assert len(result) == 10

    def test_today(self):
        result = parse_relative_date("today")
        assert result is not None

    def test_ontem(self):
        result = parse_relative_date("ontem")
        assert result is not None

    def test_yesterday(self):
        result = parse_relative_date("yesterday")
        assert result is not None

    def test_1_semana(self):
        result = parse_relative_date("1 semana atras")
        assert result is not None

    def test_2_semanas(self):
        result = parse_relative_date("2 semanas atras")
        assert result is not None

    def test_5_dias(self):
        result = parse_relative_date("5 dias atras")
        assert result is not None

    def test_hora(self):
        result = parse_relative_date("ha 2 horas")
        assert result is not None

    def test_empty_date(self):
        result = parse_relative_date("")
        assert result is not None


class TestIsWithinTwoWeeks:
    """Tests for is_within_two_weeks function"""

    def test_today_is_within(self):
        from datetime import datetime
        today = datetime.now().strftime("%Y-%m-%d")
        assert is_within_two_weeks(today) is True

    def test_yesterday_is_within(self):
        from datetime import datetime, timedelta
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        assert is_within_two_weeks(yesterday) is True

    def test_7_days_ago_is_within(self):
        from datetime import datetime, timedelta
        date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        assert is_within_two_weeks(date) is True

    def test_13_days_ago_is_within(self):
        from datetime import datetime, timedelta
        date = (datetime.now() - timedelta(days=13)).strftime("%Y-%m-%d")
        assert is_within_two_weeks(date) is True

    def test_15_days_ago_is_not_within(self):
        from datetime import datetime, timedelta
        date = (datetime.now() - timedelta(days=15)).strftime("%Y-%m-%d")
        assert is_within_two_weeks(date) is False

    def test_30_days_ago_is_not_within(self):
        from datetime import datetime, timedelta
        date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        assert is_within_two_weeks(date) is False

    def test_none_date(self):
        assert is_within_two_weeks(None) is True

    def test_empty_date(self):
        assert is_within_two_weeks("") is True

    def test_invalid_date(self):
        assert is_within_two_weeks("invalid") is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

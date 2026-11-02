from datetime import datetime
from pathlib import Path
import unittest

from django.conf import settings
from django.test.runner import DiscoverRunner


class DocumentingDiscoverRunner(DiscoverRunner):
    def run_suite(self, suite, **kwargs):
        tests = list(self._iter_tests(suite))
        result = super().run_suite(suite, **kwargs)
        self._write_documentation(tests, result)
        return result

    @classmethod
    def _iter_tests(cls, suite):
        for test in suite:
            if isinstance(test, unittest.TestSuite):
                yield from cls._iter_tests(test)
            else:
                yield test

    @staticmethod
    def _write_documentation(tests, result):
        failures = {test.id() for test, _ in result.failures}
        errors = {test.id() for test, _ in result.errors}
        skipped = {test.id(): reason for test, reason in result.skipped}
        expected_failures = {
            test.id() for test, _ in result.expectedFailures
        }
        unexpected_successes = {
            test.id() for test in result.unexpectedSuccesses
        }

        def status_for(test):
            test_id = test.id()
            if test_id in errors:
                return "Ошибка"
            if test_id in failures or test_id in unexpected_successes:
                return "Не пройден"
            if test_id in skipped:
                return f"Пропущен: {skipped[test_id]}"
            if test_id in expected_failures:
                return "Ожидаемый сбой"
            return "Пройден"

        passed = (
            result.testsRun
            - len(failures)
            - len(errors)
            - len(skipped)
            - len(expected_failures)
            - len(unexpected_successes)
        )
        lines = [
            "# Документация тестирования",
            "",
            f"Сформировано автоматически: {datetime.now().astimezone().isoformat(timespec='seconds')}.",
            "",
            "Документ обновляется при каждом запуске `python manage.py test`.",
            "",
            "## Результаты",
            "",
            f"- Всего тестов: {result.testsRun}",
            f"- Пройдено: {passed}",
            f"- Не пройдено: {len(failures) + len(unexpected_successes)}",
            f"- Ошибок: {len(errors)}",
            f"- Пропущено: {len(skipped)}",
            f"- Ожидаемых сбоев: {len(expected_failures)}",
            "",
            "## Проверки",
            "",
            "| Тест | Сценарий | Результат |",
            "| --- | --- | --- |",
        ]

        for test in tests:
            description = (
                test.shortDescription()
                or test._testMethodName.replace("test_", "").replace("_", " ")
            ).replace("|", "\\|")
            lines.append(
                f"| `{test.id()}` | {description} | {status_for(test)} |"
            )

        documentation_path = (
            Path(settings.BASE_DIR) / "docs" / "test_documentation.md"
        )
        documentation_path.parent.mkdir(parents=True, exist_ok=True)
        documentation_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

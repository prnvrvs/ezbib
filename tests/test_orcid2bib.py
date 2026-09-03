#!/usr/bin/env python3
"""
Unit tests for orcid2bib.
Zero external test dependencies - uses Python's standard unittest module.
"""

import unittest
import orcid2bib


class TestSanitizeLatex(unittest.TestCase):
    def test_mathml_conversion(self):
        sample = "Effect of <mml:math xmlns:mml='http://www.w3.org/1998/Math/MathML'><mml:mi>α</mml:mi></mml:math>-Fe matrix"
        expected = r"Effect of $\alpha$-Fe matrix"
        self.assertEqual(orcid2bib.sanitize_latex(sample), expected)

    def test_sigma_conversion(self):
        sample = "Grain boundary <mml:math><mml:mi>Σ</mml:mi></mml:math>3 structure"
        expected = r"Grain boundary $\Sigma$3 structure"
        self.assertEqual(orcid2bib.sanitize_latex(sample), expected)

    def test_html_unescape(self):
        sample = "Phase Transitions &amp; Microstructure &ndash; High-Entropy Alloys"
        expected = "Phase Transitions & Microstructure – High-Entropy Alloys"
        self.assertEqual(orcid2bib.sanitize_latex(sample), expected)

    def test_empty_none(self):
        self.assertEqual(orcid2bib.sanitize_latex(None), "")
        self.assertEqual(orcid2bib.sanitize_latex(""), "")


class TestBibtexFormatting(unittest.TestCase):
    def test_reorder_and_clean_bibtex(self):
        raw_bib = """@article{Test2024,
  year = {2024},
  title = {A study on metals},
  author = {Doe, John and Smith, Jane},
  journal = {Acta Materialia},
  doi = {10.1016/j.actamat.2024.100000}
}"""
        formatted = orcid2bib.pretty_format_bibtex(raw_bib, extra_keywords="quality_assured")
        self.assertIn("@article{Test2024,", formatted)
        self.assertIn("author = {Doe, John and Smith, Jane}", formatted)
        self.assertIn("keywords = {quality_assured}", formatted)

        # Ensure author comes before year in preferred order
        author_pos = formatted.find("author =")
        year_pos = formatted.find("year =")
        self.assertTrue(author_pos != -1 and year_pos != -1 and author_pos < year_pos)


class TestDoiDetection(unittest.TestCase):
    def test_bare_doi(self):
        self.assertTrue(orcid2bib.is_doi("10.1016/j.actamat.2025.121319"))
        self.assertTrue(orcid2bib.is_doi(" 10.1038/s41563-024-00000-x "))

    def test_url_doi(self):
        self.assertTrue(orcid2bib.is_doi("https://doi.org/10.1016/j.actamat.2025.121319"))
        self.assertTrue(orcid2bib.is_doi("http://dx.doi.org/10.1016/j.actamat.2025.121319"))

    def test_orcid_is_not_doi(self):
        self.assertFalse(orcid2bib.is_doi("0000-0002-1825-0097"))
        self.assertFalse(orcid2bib.is_doi("https://orcid.org/0000-0002-1825-0097"))


class TestCliParser(unittest.TestCase):
    def test_parser_defaults(self):
        parser = orcid2bib.build_parser()
        args = parser.parse_args(["0000-0002-1825-0097"])
        self.assertEqual(args.target, "0000-0002-1825-0097")
        self.assertEqual(args.format, "bibtex")
        self.assertEqual(args.style, "apa")
        self.assertFalse(args.no_dedup)

    def test_parser_custom_flags(self):
        parser = orcid2bib.build_parser()
        args = parser.parse_args([
            "10.1016/j.actamat.2025.121319",
            "-y", "2021",
            "--max-year", "2025",
            "-f", "text",
            "-s", "nature",
            "-o", "output.txt",
            "--no-dedup"
        ])
        self.assertEqual(args.min_year, 2021)
        self.assertEqual(args.max_year, 2025)
        self.assertEqual(args.format, "text")
        self.assertEqual(args.style, "nature")
        self.assertEqual(args.output, "output.txt")
        self.assertTrue(args.no_dedup)


if __name__ == "__main__":
    unittest.main()

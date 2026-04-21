# DSA Practice in Python

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![LeetCode](https://img.shields.io/badge/LeetCode-Problems-FFA116?style=for-the-badge&logo=leetcode&logoColor=white)](https://leetcode.com/)
[![Problems](https://img.shields.io/badge/Problems_Solved-12-22C55E?style=for-the-badge&logo=checkmarx&logoColor=white)](DSA/)
[![Docs](https://img.shields.io/badge/Docs-Detailed-F97316?style=for-the-badge&logo=readthedocs&logoColor=white)](DSA/)

[![License: MIT](https://img.shields.io/badge/License-MIT-F7DF1E?style=for-the-badge&logo=opensourceinitiative&logoColor=black)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/Status-Active%20Learning-22C55E?style=for-the-badge&logo=statuspage&logoColor=white)](https://github.com/RJ-Gamer/dsa)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-6366F1?style=for-the-badge&logo=github&logoColor=white)](http://makeapullrequest.com)

[![Stars](https://img.shields.io/github/stars/RJ-Gamer/DSA-SOLVED?style=social)](https://github.com/RJ-Gamer/DSA-SOLVED)
[![Sponsor](https://img.shields.io/badge/Sponsor-GitHub-ff69b4?logo=github&style=social)](https://github.com/sponsors/RJ-Gamer)

**Tags:** `dsa` `algorithms` `python` `leetcode` `interview-prep` `problem-solving`

This repository contains Data Structures and Algorithms problems solved in
Python, with detailed markdown explanations for each problem. The focus is not
just on writing code that passes, but on documenting the reasoning, trade-offs,
patterns, and real-world applications behind each solution.

The documentation style is guided by [CLAUDE.md](CLAUDE.md),
which defines a consistent structure for every problem note.

---

## Highlights

- Python solutions organized problem-by-problem
- Detailed markdown notes for each problem folder
- Problem-solving walkthroughs before code
- Brute force and optimal approaches where useful
- Common mistakes, pattern recognition, and real-world use cases
- Repo-level community files for clean collaboration

---

## Repository Structure

```text
dsa_practice/
|-- .github/
|   |-- ISSUE_TEMPLATE/
|   |-- workflows/
|   `-- PULL_REQUEST_TEMPLATE.md
|-- DSA/
|   |-- 01_two_sum/
|   |-- 53_maximum_subarray/
|   |-- 121_best_time_to_buy_and_sell/
|   |-- 125_valid_palindrome/
|   |-- 217_contains_duplicate/
|   |-- 242_valid_anagram/
|   |-- 516_longest_palindrome_subsequence/
|   |-- 62_unique_paths/
|   |-- 63_unique_paths_II/
|   |-- 647_palindrome_substrings/
|   |-- 72_min_distance/
|   `-- 1143_longest_common_subsequence/
|-- .editorconfig
|-- .gitattributes
|-- .gitignore
|-- CLAUDE.md
|-- CODE_OF_CONDUCT.md
|-- CONTRIBUTING.md
|-- LICENSE
|-- README.md
`-- SECURITY.md
```

---

## Documentation Standard

Every problem folder should contain:

1. A Python solution file
2. A markdown explanation file (`README.md`) with:
   - Problem statement and constraints
   - Thinking process before implementation
   - Brute force and optimal approaches
   - Step-by-step solution breakdown
   - Common mistakes
   - Pattern recognition
   - Real-world use cases
   - Key takeaways

This keeps the repo useful both as a practice log and as a study resource.

---

## Problem Index

| # | Problem | Difficulty | Topics | Solution |
|---|---------|------------|--------|----------|
| 01 | Two Sum | Easy | Array, Hash Map | [Notes](DSA/01_two_sum/) |
| 53 | Maximum Subarray | Medium | Array, Dynamic Programming | [Notes](DSA/53_maximum_subarray/) |
| 121 | Best Time to Buy and Sell Stock | Easy | Array, Two Pointers, Greedy | [Notes](DSA/121_best_time_to_buy_and_sell/) |
| 125 | Valid Palindrome | Easy | String, Two Pointers | [Notes](DSA/125_valid_palindrome/) |
| 217 | Contains Duplicate | Easy | Array, Hash Map | [Notes](DSA/217_contains_duplicate/) |
| 242 | Valid Anagram | Easy | String, Hash Map | [Notes](DSA/242_valid_anagram/) |
| 516 | Longest Palindromic Subsequence | Medium | String, Dynamic Programming | [Notes](DSA/516_longest_palindrome_subsequence/) |
| 62 | Unique Paths | Medium | Dynamic Programming, Math | [Notes](DSA/62_unique_paths/) |
| 63 | Unique Paths II | Medium | Dynamic Programming | [Notes](DSA/63_unique_paths_II/) |
| 647 | Palindromic Substrings | Medium | String, Dynamic Programming | [Notes](DSA/647_palindrome_substrings/) |
| 72 | Edit Distance | Medium | String, Dynamic Programming | [Notes](DSA/72_min_distance/) |
| 1143 | Longest Common Subsequence | Medium | String, Dynamic Programming | [Notes](DSA/1143_longest_common_subsequence/) |

---

## How to Use This Repo

### Read a problem

Open a folder inside `DSA/` and read:

- the `.py` file for the implementation
- the `README.md` file for the explanation

### Add a new problem

1. Create a new folder using the naming convention:
   - `{number}_{snake_case_name}/`
2. Add:
   - `{number}_lc_{snake_case_name}.py`
   - `README.md`
3. Follow the exact documentation structure in `CLAUDE.md`
4. Update the table in this `README.md`

Example:

```text
DSA/242_valid_anagram/
|-- 242_lc_valid_anagram.py
`-- README.md
```

---

## Naming Conventions

| Item | Format | Example |
|------|--------|---------|
| Problem folder | `{number}_{snake_case_name}/` | `125_valid_palindrome/` |
| Python file | `{number}_lc_{snake_case_name}.py` | `125_lc_valid_palindrome.py` |
| Markdown file | `README.md` | `README.md` |

---

## Topics Covered

- Array
- String
- Hash Map
- Two Pointers
- Greedy
- Dynamic Programming
- Math

More topics will be added as the problem set grows.

---

## Local Workflow

```powershell
git clone <your-repo-url>
cd dsa_practice
python DSA/125_valid_palindrome/125_lc_valid_palindrome.py
```

To verify Python syntax for all solutions:

```powershell
python -m compileall DSA
```

---

## Contributing

Contributions are welcome if they preserve the repo's educational style and
structure.

Before opening a pull request:

- read [CONTRIBUTING.md](CONTRIBUTING.md)
- follow the format in [CLAUDE.md](CLAUDE.md)
- keep explanations detailed and beginner-friendly
- update the problem index in this README

---

## Community Standards

- Contribution guide: [CONTRIBUTING.md](CONTRIBUTING.md)
- Code of conduct: [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
- Security policy: [SECURITY.md](SECURITY.md)
- Support: [SUPPORT.md](SUPPORT.md)
- License: [LICENSE](LICENSE)

---

## License

This project is licensed under the MIT License.

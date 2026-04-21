# Contributing Guide

Thanks for contributing to this repository.

The goal of this project is to build a clean, educational collection of DSA
problems in Python with detailed markdown documentation that teaches problem
solving, not just implementation.

---

## Ground Rules

- Keep folder and file naming consistent with `CLAUDE.md`
- Every problem folder must include both a `.py` file and a `README.md` file
- Every `README.md` must follow the full structure defined in `CLAUDE.md`:
  - LeetCode header, Problem Statement, How to Think, Approaches, Solution Breakdown,
    Quick Summary, Common Mistakes, Pattern Recognition, Real World Use Cases,
    Key Takeaways, Where to Practice
- Keep explanations clear, detailed, and structured
- Prefer readable Python over overly clever shortcuts
- Do not remove or rewrite existing material unless it improves correctness or clarity

---

## Problem File Format

For each problem, create:

- `DSA/{number}_{snake_case_name}/`
- `DSA/{number}_{snake_case_name}/{number}_lc_{snake_case_name}.py`
- `DSA/{number}_{snake_case_name}/README.md`

Use the documentation template and quality rules defined in `CLAUDE.md`.

> Each problem's markdown file must be named `README.md` so GitHub renders
> it automatically when browsing the problem folder.

---

## Before You Open a Pull Request

- Confirm the Python solution works
- Confirm the markdown file matches the actual solution
- Update `README.md` with the new problem entry
- Keep formatting and naming consistent with the rest of the repo
- Avoid unrelated changes in the same pull request

---

## Commit Style

Suggested commit prefixes:

- `docs:` for markdown or README updates
- `feat:` for new problems
- `fix:` for corrections to logic or explanation
- `chore:` for repo maintenance files

Examples:

```text
feat: add 242 valid anagram solution and notes
docs: improve maximum subarray explanation
fix: handle punctuation-only case in valid palindrome
```

---

## Pull Request Checklist

- I followed the naming conventions
- I added both the Python solution and `README.md` explanation
- I updated `README.md`
- I checked the solution for correctness
- I kept the change focused and easy to review

---

## Code Style

- Use Python type hints where practical
- Keep functions small and readable
- Add comments only when they clarify reasoning
- Match the repo's existing style instead of introducing a new format

---

## Questions or Suggestions

If you want to contribute a new pattern, improve documentation quality, or
standardize problem notes further, open an issue first so the change can be
discussed before implementation.

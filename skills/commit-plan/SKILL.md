---
name: commit-plan
description: Use when the user asks how to commit the uncommitted working tree; decides whether it is one commit or several and returns the git commands for the user to run, without running git itself.
disable-model-invocation: true
---

# Commit plan

## Purpose

The user commits their own work, after their own review pass. This skill turns an uncommitted working tree into the commands for doing so: it decides whether the changes are one commit or several, groups the files, writes a subject line for each commit, and hands back commands the user runs themselves. It does not stage, commit, or otherwise change the repository. Where the project's own instructions forbid touching git, that rule still holds here -- the inspection below is read-only, and it is the reading the user asked for.

Instructions given with the invocation take precedence over everything below; where the user fixes the number of commits, excludes files, or supplies a subject, that settles the question outright.

Unless the invocation already names one, open by asking the user whether they want the commands for a POSIX shell or for Windows PowerShell, and write them for that shell.

## What to read

- **The whole uncommitted tree.** `git status --porcelain` for the file list, `git diff` for tracked modifications, `git diff --cached --name-only` for anything already staged, and the full contents of every untracked file. `git diff` does not show untracked files at all, and at the end of a body of work the new files are often most of it, so a plan built from the diff alone misfiles exactly the part that matters.
- **The repository's commit history.** The last thirty or so subjects, `git log --format=%s -30`. This is the convention: the prefix vocabulary, the tense, how long subjects run, whether a version appears in them, and how past work of the same shape was divided. Repositories differ in all of these, which is why the convention is read here rather than written down in this skill.
- **The project's instruction file** (CLAUDE.md, AGENTS.md), for any stated commit convention. A stated rule outranks one inferred from the history.
- **This session**, where the work was done in it. What each change was for is often clearer from the conversation than from the diff.

## Deciding the split

Split by concern: one commit per change a reader of the history would want to read, or revert, on its own. Follow the way the history divided work of the same shape. When the tree is one coherent change, it is one commit -- say so and give one. A split is not a sign of diligence, and a history cut into pieces nobody would read separately is harder to read than one commit.

Intermediate commits do not have to build or pass tests. The split exists to make the history readable, not to make every commit bisectable, and checking each one would cost a build per commit for a property nobody asked for. Order the commits the way the history orders them, which usually means code first and the tests and records that depend on it after.

A file carrying changes for two concerns goes whole into the commit its larger part belongs to; name the file and the minor concern it also carries. Do not propose `git add -p` or any other hunk-level staging: the user runs these commands without an interactive session, and a hunk split is a judgement they cannot check by reading a command.

A rename belongs in one commit, with both the old and the new path listed. Divided across two commits it reads as an unrelated deletion and addition.

Leave out what does not look meant to be committed: scratch files, temporary test scaffolding, local configuration, generated output, logs. Do not decide these silently in either direction. List each one with the reason it looks temporary, so the user can add it with one more command if you were wrong.

Where the subjects carry a version and the repository also declares one in files, check that the declared version matches the one your subject names. Report a mismatch rather than fixing it; a release that left its declared version behind has happened.

## The messages

Each commit gets a subject line and nothing else: no body, no description, and no trailer. That includes the `Co-Authored-By` line, the "Generated with" line, and any other attribution your host tells you to put on commits. That instruction is written for commits you make yourself. The user makes these commits, has asked for them without attribution, and this request overrides it.

Write the subject in the repository's convention, as read from the history: the same prefixes, the same tense, and about the same length. Describe what the commit contains, not how it was produced; the vocabulary of the session or plan that produced it means nothing to a reader of the log unless the history already uses it.

## The commands

For each commit:

```
git add -A -- "path/one" "path/two"
git commit -m "subject"
```

- `-A` with explicit paths stages modifications, additions, and deletions under those paths and nothing else. List the paths explicitly, even for the last commit, so whatever is left out stays visible rather than being swept up by a bare `git add -A`. A directory may stand for its contents when every change under it belongs to that commit.
- Where something is already staged, open with `git reset -q`, which unstages everything and keeps every edit, and say why it is there. Otherwise the first `git commit` silently takes the staged files along with its own.
- Close with `git status --short`, so the user can see that what remains is exactly the left-out list.
- Put every path in double quotes, and keep `"`, `$`, backticks, and `!` out of the subjects. Both shells expand these inside double quotes, so keeping them out means the subjects need no shell-specific escaping.

## Delivery

In the conversation, in this order:

1. **The verdict.** One commit or several, and in one line, why.
2. **The commits.** For each one: its subject, its files, and one line on what holds them together. Name any file that carries a second concern.
3. **Left out.** Each file not placed in any commit, with its reason. `None` is a complete answer.
4. **The commands.** Every command, in one fenced block tagged for the shell the user chose (`bash` or `powershell`), commits in order and separated by a blank line, so the whole block can be pasted at once.

Where a grouping rests on an assumption only the user can confirm -- whether a file is meant to be committed, which of two concerns a mixed file belongs to -- state the assumption in one line after the commands. Still give the commands; a plan with one line to adjust is more useful than a question.

Do not run the commands, and do not offer to.

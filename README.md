<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="skills/docketdial/assets/docketdial-dark.png">
    <img src="skills/docketdial/assets/docketdial.png" width="400" alt="DocketDial, a double-D pocket watch with a gold crown">
  </picture>
</p>

# DocketDial

For lawyers who can reconstruct a client’s entire Tuesday but can’t remember their own. DocketDial turns emails, calls, texts, and calendar events into draft time entries.

Ask for a day or a billing period. DocketDial groups the work it can substantiate by client and matter, cites the record behind each entry, and flags the questions only you can answer. You review and amend the draft before entering time in your billing system.

## Get started

| Where you work | How to add DocketDial |
| --- | --- |
| Microsoft 365 Copilot Cowork | Open [DocketDial.md](copilot/DocketDial.md) and choose **Download raw file** on GitHub. In Cowork, open **Customize → Skills**, then the arrow beside **Add → Upload skill**. Select the downloaded file. [Microsoft’s guide](https://learn.microsoft.com/en-us/copilot/cowork/use-cowork#upload-a-skill) |
| Codex | Copy the [docketdial folder](skills/docketdial) into `~/.agents/skills/`. [Codex skills guide](https://developers.openai.com/codex/skills/) |
| Claude | Download the [ready-to-upload skill ZIP](https://github.com/m66se/docketdial/releases/latest/download/docketdial.zip). Open **Plugins** (or **Customize → Skills**), choose the option to upload a skill, select the ZIP, and enable DocketDial. [Claude’s skill guide](https://support.claude.com/en/articles/12512180-use-skills-in-claude) |

## Run DocketDial

| Where you work | How to start a docket |
| --- | --- |
| Claude | In a new conversation, type `/docketdial Draft my dockets for yesterday.` If your account still has separate Chat and Cowork modes, open Cowork first. [Claude’s rollout guide](https://support.claude.com/en/articles/16761823-claude-cowork-and-chat-are-one-claude) |
| Microsoft 365 Copilot Cowork | In a new task, type `/` to open the picker. If the **Skills** tab is available, select **Skills → docketdial**, then enter `Draft my dockets for yesterday.` You can also type `Use DocketDial to draft my dockets for yesterday.` Check **Skills** in the session side panel to see what loaded. [Cowork guide](https://learn.microsoft.com/en-us/copilot/cowork/use-cowork) |
| Codex | Type `$docketdial Draft my dockets for yesterday.` |

In your firm’s approved workspace, give the assistant access to the relevant work records or attach exports. For phone activity, attach call-log or message screenshots that show the event date and time. Include a matter list with client, matter ID, matter name, contact, full phone number, and email where available. Add existing time entries to check for duplicates. For fee subtotals, include the matter’s billing rules, rates, and currency.

> Draft my dockets for yesterday from my sent email, calendar, and the phone screenshots I attached. Match them to my open matters, flag anything I already entered, and show me which entries still need a duration or matter.

## Try a fictional workday

[Try the Alder Mill example](examples/alder-mill/README.md) with two phone screenshots, a matter register, and a workday extract. Its first prompt works with the supplied files alone. After reviewing your draft, open the separate answer key or try the lawyer’s amendment.

The private review copy keeps the evidence alongside the entries. You can request an editable workbook or a client-facing draft containing only the entries you confirm.

## Build the downloads

Edit [SKILL.md](skills/docketdial/SKILL.md) for shared behavior and [copilot-section.md](scripts/copilot-section.md) for Microsoft-specific guidance. Run `python3 scripts/build.py` to refresh [DocketDial.md](copilot/DocketDial.md). Commit the generated file with its source changes.

Run `python3 scripts/build.py --check --output dist` to check for drift and build both install files. To publish a release, add its notes under `release/` and update `release/VERSION` on the main branch. The release workflow validates the downloads, publishes them at that commit, and marks the version latest.

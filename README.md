<p align="center">
  <img src="skills/docketdial/assets/docketdial.png" width="400" alt="DocketDial, a navy double-D pocket watch with a gold crown">
</p>

# DocketDial

For lawyers who can reconstruct a client’s entire Tuesday but can’t remember their own. DocketDial turns emails, calls, texts, and calendar events into draft time entries.

Ask for a day or a billing period. DocketDial groups the work it can substantiate by client and matter, cites the record behind each entry, and flags the questions only you can answer. You review and amend the draft before entering time in your billing system.

## Get started

| Where you work | How to add DocketDial |
| --- | --- |
| Microsoft 365 Copilot Cowork | Open [DocketDial.md](copilot/DocketDial.md) and choose **Download raw file** on GitHub. In Cowork, open **Customize → Skills**, then the arrow beside **Add → Upload skill**. Select the downloaded file. [Microsoft’s guide](https://learn.microsoft.com/en-us/copilot/cowork/use-cowork#upload-a-skill) |
| Codex | Copy the [docketdial folder](skills/docketdial) into `~/.agents/skills/`. Start a prompt with `$docketdial`. [Codex skills guide](https://developers.openai.com/codex/skills/) |
| Claude Cowork | Download the repository, unzip it, then zip just the [docketdial folder](skills/docketdial) with `docketdial/SKILL.md` inside the archive. Upload that ZIP in **Customize → Skills** and enable it. [Claude’s guide](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills) |

In your firm’s approved workspace, give the assistant access to the relevant work records or attach exports. For phone activity, attach call-log or message screenshots that show the event date and time. Include a matter list with client, matter ID, matter name, contact, full phone number, and email where available. Add existing time entries to check for duplicates. For fee subtotals, include the matter’s billing rules, rates, and currency.

> Draft my dockets for yesterday from my sent email, calendar, and the phone screenshots I attached. Match them to my open matters, flag anything I already entered, and show me which entries still need a duration or matter.

## What the draft looks like

Here’s a fictional example. A call log shows a connected call of 12 minutes and 40 seconds. Its number matches a contact on two files. A text from that contact identifies the purchase agreement for Alder Mill. A later email shows that the lawyer sent a revised clause on the same matter.

| ID | Client / matter | Draft narrative | Worked time | Review | Evidence |
| --- | --- | --- | --- | --- | --- |
| D1 | Alder Mill / AM-12 | Discuss purchase agreement with client | 12m 40s, connected call | Proposed | Call log, 10:04 and text identifying AM-12 |
| D2 | Alder Mill / AM-12 | Send revised indemnity clause to client | | Needs duration | Sent email, 11:18 |

The call and the text support one entry. The email establishes what was sent and when. You can amend the second row by saying, “I spent 15 minutes revising and sending the clause. Update D2.” DocketDial then recalculates any fees it can support under the matter’s billing rules.

The private review copy keeps the evidence alongside the rows. You can ask for an editable workbook or a client-facing draft containing only the entries you confirmed. Posting time and issuing invoices stay with the timekeeper.

- If you see "$" printed in/near the Price or Dollar Amount region, treat it as a visual marker only.
  - Do NOT output "$" as a separate cell.
  - Output only the numeric part (keep commas if present).
- Keep commas inside large numbers (example: 23,452,564.00).
- Keep decimals exactly as shown.

Right-anchoring rule (CRITICAL to avoid shifting):
- Identify the rightmost stable column: Reference Number.
  - Reference Number is typically a long numeric id (often 8+ digits) and appears at the far right.
- For each row, lock Reference Number first.
- Then extract the numeric block immediately to the left of Reference Number in this order:
  Shares (left of Reference Number),
  Dollar Amount (left of Shares),
  Price (left of Dollar Amount).
- If a value is absent, output _EMPTY_ in that column but keep the column position.

Price / Dollar Amount / Shares disambiguation:
- Treat these three as separate columns even if the document shows a "$" sub-column.
- Assignment rules:
  1) If three numeric values exist in the block, map them in visual left-to-right order as:
     Price, Dollar Amount, Shares (after removing any standalone "$").
  2) If only two numeric values exist in the block:
     - Use visual alignment: the one closest to Reference Number is Shares.
     - The one immediately left of Shares is Dollar Amount.
     - Price becomes _EMPTY_.
  3) If only one numeric value exists in the block:
     - Place it in Shares if it is closest to Reference Number; otherwise place by nearest header alignment.
     - Fill the other two with _EMPTY_.

Output rules:
- Output ONLY the Markdown table (header + separator + rows).
- No explanations, no extra text.
"""

user_prompt = """
Extract the 'Trade Activity Summary' table from the image.
Return ONLY the Markdown table using the exact 12 output columns and rules from the system prompt.
Key: anchor from the right using Reference Number, and never output '$' as a separate cell.
"""

# Conductor Compatibility Rule (Antigravity)

The Conductor skills in this repository were written targeting the `ask_user` tool, which uses structured JSON payloads (types like `choice`, `yesno`, `text`, and arrays of `options`).

**Your environment does not have the `ask_user` tool. You must use your native user interaction or questioning tool instead.**

## Tool Translation Protocol
Whenever a Conductor skill instructs you to call `ask_user`, you MUST perform an **on-the-fly translation** to leverage your native interactive UI capabilities:

1.  **Extract the Intent:** Read the `question`, `type`, and `options` from the skill's instructions.
2.  **Batching:** If a skill instructs you to batch multiple questions into a single tool call, you MUST use your platform's native support for grouped or batched questions.
3.  **Synthesize the Prompt:** 
    -   **If `type: "choice"`:** Use your platform's native multiple-choice UI component. Map the skill's options directly to your selectable options. Support multi-select if the skill specifies it.
    -   **If `type: "yesno"`:** Provide a boolean or Yes/No choice using your native UI.
    -   **If `type: "text"`:** Use a standard text input field.
4.  **Execute:** Present the synthesized, interactive prompt to the user and wait for their response.

## File Operations Mapping
- If a skill mentions `write_file`, use your native file creation tool.
- If a skill mentions `replace`, use your native file editing/patching tool.

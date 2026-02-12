# Local LLM interaction

import subprocess
import shutil
import os

# Configuration (Environment override supported)
DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5")
TIMEOUT_SECONDS = 45

# Handles process execution, timeouts, and output extraction. 
class OllamaClient:
    def __init__(self, model=DEFAULT_MODEL):
        self.model = model

    # Internal Utilities
    # Checks if Ollama is installed and in the system path.
    def _ollama_exists(self):
        return shutil.which("ollama") is not None

    # Executes Ollama CLI safely.
    def _run_ollama(self, prompt):
        if not self._ollama_exists():
            return False, "Ollama CLI not found. Please install Ollama and ensure it is in PATH."

        try:
            process = subprocess.run(
                ["ollama", "run", self.model],
                input=prompt,
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=TIMEOUT_SECONDS
            )

            if process.returncode != 0:
                stderr = (process.stderr or "").lower()

                # Error for missing model
                if "pull" in stderr or "not found" in stderr:
                    return False, (
                        f"Model '{self.model}' not found. "
                        f"Run: ollama pull {self.model}"
                    )

                return False, f"Ollama Error (Code {process.returncode}): {process.stderr.strip()}"

            output = process.stdout.strip()
            if not output:
                return False, "Ollama returned empty output."

            return True, output

        except subprocess.TimeoutExpired:
            return False, f"Timeout: Model exceeded {TIMEOUT_SECONDS} seconds."

        except Exception as exc:
            return False, f"System Error: {str(exc)}"

    # Extracts content strictly between defined markers, robust against prompt echoing.
    def _extract_between_markers(self, text, start_marker, end_marker):
        start_idx = text.rfind(start_marker)
        end_idx = text.rfind(end_marker)

        if start_idx == -1 or end_idx == -1 or end_idx <= start_idx:
            return None

        content_start = start_idx + len(start_marker)
        return text[content_start:end_idx].strip()

    # Wraps the base prompt with strict output formatting instructions.
    def _wrap_prompt(self, base_prompt, start_marker, end_marker):
        return (
            f"{base_prompt}\n\n"
            "SYSTEM INSTRUCTION:\n"
            f"- Your entire response MUST be enclosed between:\n"
            f"{start_marker}\n"
            f"{end_marker}\n"
            "- Do not include anything outside these markers."
        )

    # Public API
    # Generates analysis based on the provided prompt.
    def generate_analysis(self, prompt):
        START = "===BEGIN ANALYSIS==="
        END = "===END ANALYSIS==="

        safe_prompt = self._wrap_prompt(prompt, START, END)
        success, output = self._run_ollama(safe_prompt)

        if not success:
            return f"[AI System Message] {output}"

        extracted = self._extract_between_markers(output, START, END)
        return extracted if extracted else f"[Raw Output]\n{output[:1000]}"

    # Generates interview questions.
    def generate_questions(self, prompt):
        START = "===BEGIN QUESTIONS==="
        END = "===END QUESTIONS==="

        safe_prompt = self._wrap_prompt(prompt, START, END)
        success, output = self._run_ollama(safe_prompt)

        if not success:
            return f"[AI System Message] {output}"

        extracted = self._extract_between_markers(output, START, END)
        return extracted if extracted else f"[Raw Output]\n{output[:1000]}"

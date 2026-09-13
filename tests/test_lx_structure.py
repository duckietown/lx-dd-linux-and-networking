"""Sanity tests for the Linux and Networking learning experience.

Run from the LX root with:

    pytest tests/

These tests validate learner material without requiring ROS dependencies, so they
can run both inside the editor container and on a plain host Python.
"""

import ast
import json
import re
import subprocess
from itertools import pairwise
from pathlib import Path
from unittest.mock import patch

from packages import checkpoint_self_check

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_DIR = ROOT / "notebooks"
EXERCISE_DIR = ROOT / "packages" / "shell_exercises"
README_PATH = ROOT / "README.md"
NETWORK_DIAGRAM_PATH = (
    ROOT / "assets" / "images" / "Sample-network-diagram.png"
)
CHECKPOINT_DATA_DIR = ROOT / "checkpoint_data"
CHECKPOINT_SELF_CHECK_PATH = ROOT / "packages" / "checkpoint_self_check.py"
LIST_ITEM = re.compile(r"^\s*(?:[-*+] |\d+\. )")
VSCODE_HEADING_PUNCTUATION = "[]!/'\"#$%&()*+,./:;<=>?@\\^{}|~`"
REQUIRED_NOTEBOOKS = {
    "notebooks/1-linux-foundations-and-distributions.ipynb": "# Linux Foundations and Distributions",
    "notebooks/2-linux-shell-and-navigation.ipynb": "# Linux Shell and Navigation",
    "notebooks/3-shell-variables-quoting-and-environment.ipynb": "# Shell Variables, Quoting, and Environment",
    "notebooks/4-create-and-manage-files.ipynb": "# Create and Manage Files",
    "notebooks/5-filenames-wildcards-and-search.ipynb": "# Filenames, Wildcards, and Search",
    "notebooks/6-shell-help-errors-and-exit-status.ipynb": "# Shell Help, Errors, and Exit Status",
    "notebooks/7-standard-streams-and-redirection.ipynb": "# Standard Streams and Redirection",
    "notebooks/8-pipes-and-data-processing.ipynb": "# Pipes and Data Processing",
    "notebooks/9-shell-scripts-and-execution.ipynb": "# Shell Scripts and Execution",
    "notebooks/10-users-ownership-and-permissions.ipynb": "# Users, Ownership, and Permissions",
    "notebooks/11-processes-monitoring-and-job-control.ipynb": "# Processes, Monitoring, and Job Control",
    "notebooks/12-shell-exercises-and-output-verification.ipynb": "# Shell Exercises and Output Verification",
    "notebooks/13-network-addressing-and-routing.ipynb": "# Network Addressing and Routing",
    "notebooks/14-network-protocols-and-quality.ipynb": "# Network Protocols and Quality",
    "notebooks/15-localhost-and-service-binding.ipynb": "# Localhost and Service Binding",
    "notebooks/16-network-configuration-and-access-policy.ipynb": "# Network Configuration and Access Policy",
    "notebooks/17-network-names-and-service-discovery.ipynb": "# Network Names and Service Discovery",
    "notebooks/18-network-diagnostics-and-testing.ipynb": "# Network Diagnostics and Testing",
    "notebooks/19-physical-duckiedrone-ssh-access.ipynb": "# Secure Shell Access to a Physical Duckiedrone",
    "notebooks/20-virtual-duckiedrone-connections.ipynb": "# Virtual Duckiedrone Connections",
    "notebooks/21-duckiedrone-filesystem-inspection.ipynb": "# Duckiedrone Filesystem Inspection",
    "notebooks/22-duckiedrone-process-inspection.ipynb": "# Duckiedrone Process Inspection",
}
INTERACTIVE_CHECKPOINT_NOTEBOOKS = set(REQUIRED_NOTEBOOKS)
CHECKPOINT_CODE_SOURCE = [
    "import sys",
    "from pathlib import Path",
    "",
    "working_directory = Path.cwd()",
    "parent_directory = working_directory.parent",
    'if (parent_directory / "packages").is_dir():',
    "    parent_directory_path = str(parent_directory)",
    "    sys.path.insert(0, parent_directory_path)",
    "",
    "from packages.checkpoint_self_check import display_checkpoint_self_checks",
    "",
    "display_checkpoint_self_checks()",
]


def vscode_heading_fragment(heading: str) -> str:
    """Return the fragment assigned to an ASCII Markdown heading by VS Code."""
    normalized_heading = re.sub(r"\s+", "-", heading.strip().lower())
    fragment_characters = [
        character
        for character in normalized_heading
        if character not in VSCODE_HEADING_PUNCTUATION
    ]
    return "".join(fragment_characters).strip("-")


def checkpoint_data_path(notebook_relative_path: str) -> Path:
    """Return the sidecar path implied by a numbered notebook path."""
    notebook_name = Path(notebook_relative_path).stem
    _, separator, checkpoint_name = notebook_name.partition("-")
    assert separator and checkpoint_name
    return CHECKPOINT_DATA_DIR / f"{checkpoint_name}.json"


def test_notebooks_directory_does_not_duplicate_shared_packages() -> None:
    """Keep shared code in the LX-level packages directory only."""
    notebook_packages_path = NOTEBOOK_DIR / "packages"
    assert not notebook_packages_path.exists()
    assert not notebook_packages_path.is_symlink()


def test_notebook_cells_have_consistent_metadata() -> None:
    """Keep the granular notebook set usable in the editor."""
    expected_paths = {
        ROOT / relative_path for relative_path in REQUIRED_NOTEBOOKS
    }
    assert expected_paths == set(NOTEBOOK_DIR.glob("*.ipynb"))

    for relative_path, expected_h1 in REQUIRED_NOTEBOOKS.items():
        notebook_path = ROOT / relative_path
        notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
        assert notebook["nbformat"] == 4
        expected_cell_count = (
            2 if relative_path in INTERACTIVE_CHECKPOINT_NOTEBOOKS else 1
        )
        assert len(notebook["cells"]) == expected_cell_count

        for cell in notebook["cells"]:
            assert isinstance(cell.get("id"), str) and cell["id"]
            assert cell["id"] == cell["metadata"]["id"]

        markdown_cell = notebook["cells"][0]
        assert markdown_cell["cell_type"] == "markdown"
        assert markdown_cell["metadata"]["language"] == "markdown"
        assert "".join(markdown_cell["source"]).splitlines()[0] == expected_h1

        if relative_path in INTERACTIVE_CHECKPOINT_NOTEBOOKS:
            code_cell = notebook["cells"][1]
            assert code_cell["cell_type"] == "code"
            assert code_cell["metadata"]["language"] == "python"


def assert_reveal_self_check(
    notebook_relative_path: str,
    checkpoint_path: Path,
) -> None:
    """Check one interactive checkpoint without embedding its data."""
    notebook_path = ROOT / notebook_relative_path
    notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
    markdown_source = "".join(notebook["cells"][0]["source"])
    code_source = "".join(notebook["cells"][1]["source"])
    notebook_source = markdown_source + code_source
    checkpoint_data = json.loads(checkpoint_path.read_text(encoding="utf-8"))

    assert set(checkpoint_data) == {"checkpoints"}
    assert code_source.splitlines() == CHECKPOINT_CODE_SOURCE
    checkpoints = checkpoint_data["checkpoints"]
    assert isinstance(checkpoints, list)
    assert (
        "Write or select a response before revealing the answer."
        in markdown_source
    )
    assert ".checkpoint-source:target" not in markdown_source
    assert "<style>" not in markdown_source
    assert "<mark>Checkpoint source</mark>" not in markdown_source

    found_checkpoint_ids = set()
    for checkpoint in checkpoints:
        assert isinstance(checkpoint, dict)
        required_checkpoint_fields = {
            "id",
            "question",
            "model_answer",
            "evidence",
        }
        checkpoint_id = checkpoint["id"]
        question = checkpoint["question"]
        model_answer = checkpoint["model_answer"]
        evidence = checkpoint["evidence"]
        assert isinstance(checkpoint_id, str) and checkpoint_id
        assert isinstance(question, str) and question
        assert isinstance(model_answer, str) and model_answer
        assert isinstance(evidence, list) and evidence
        if "choices" in checkpoint:
            assert set(checkpoint) == required_checkpoint_fields | {
                "choices",
                "correct_choice",
            }
            choices = checkpoint["choices"]
            correct_choice = checkpoint["correct_choice"]
            assert isinstance(choices, list) and len(choices) >= 2
            assert all(
                isinstance(choice, str) and choice.strip()
                for choice in choices
            )
            assert len(choices) == len(set(choices))
            assert (
                isinstance(correct_choice, str) and correct_choice in choices
            )
        else:
            assert set(checkpoint) == required_checkpoint_fields
        assert question not in notebook_source
        assert model_answer not in notebook_source
        found_checkpoint_ids.add(checkpoint_id)
        for evidence_item in evidence:
            assert set(evidence_item) == {"label", "anchor"}
            source_section = evidence_item["label"]
            anchor = evidence_item["anchor"]
            assert isinstance(source_section, str) and source_section
            assert isinstance(anchor, str) and anchor.startswith("#")
            assert f"## {source_section}" in markdown_source
            assert anchor == f"#{vscode_heading_fragment(source_section)}"
    assert len(checkpoints) == len(found_checkpoint_ids)

    for required_text in (
        "from packages.checkpoint_self_check import display_checkpoint_self_checks",
        "display_checkpoint_self_checks",
    ):
        assert required_text in code_source

    for checkpoint_id in found_checkpoint_ids:
        assert checkpoint_id not in code_source


def test_shared_checkpoint_self_check_helper_is_valid() -> None:
    """Keep the reusable checkpoint implementation available and syntactically valid."""
    helper_source = CHECKPOINT_SELF_CHECK_PATH.read_text(encoding="utf-8")
    ast.parse(helper_source, filename=str(CHECKPOINT_SELF_CHECK_PATH))

    for required_text in (
        "class CheckpointSelfCheck",
        "def load_checkpoint_definitions",
        "def load_model_answer",
        "def load_correct_choice",
        "def render_model_answer",
        "def render_choice_result",
        "def render_status",
        "Checkbox",
        "Reveal answer",
        "Try again",
        "def display_checkpoint_self_checks",
        "checkpoint_name: str | None = None",
        "get_checkpoint_name_from_notebook_context",
    ):
        assert required_text in helper_source
    assert "notebook_name" not in helper_source
    assert (
        "Compare the model answer with your response and revisit the linked source "
        "sections above as needed."
    ) not in helper_source
    for removed_prompt in (
        "Write an answer to enable confirmation.",
        "Select an answer to enable confirmation.",
        "Confirm answer",
        "Edit answer",
        "Reveal model answer",
    ):
        assert removed_prompt not in helper_source


def test_checkpoint_name_is_derived_from_vs_code_notebook_context() -> None:
    """Keep the no-argument notebook call free of an embedded checkpoint name."""

    class Kernel:
        def get_parent(self) -> dict[str, object]:
            return {
                "metadata": {
                    "cellId": (
                        "vscode-notebook-cell://dev-container/workspace/notebooks/"
                        "2-linux-shell-and-navigation.ipynb#checkpoint"
                    ),
                },
            }

    class Shell:
        kernel = Kernel()

    with patch.object(
        checkpoint_self_check, "get_ipython", return_value=Shell()
    ):
        checkpoint_name = (
            checkpoint_self_check.get_checkpoint_name_from_notebook_context()
        )

    assert checkpoint_name == "linux-shell-and-navigation"


def test_checkpoint_display_does_not_return_widget_state() -> None:
    """Keep notebook output limited to the explicitly displayed widgets."""
    with patch.object(checkpoint_self_check, "display") as display:
        result = checkpoint_self_check.display_checkpoint_self_checks(
            "linux-shell-and-navigation",
        )

    assert result is None
    display.assert_called_once()
    displayed_widget = display.call_args.args[0]
    assert "checkpoint-self-checks" in displayed_widget._dom_classes
    control_style = displayed_widget.children[0]
    assert control_style.value == checkpoint_self_check.CHECKPOINT_WIDGET_STYLE
    assert control_style.layout.display == "none"
    first_checkpoint = displayed_widget.children[1]
    first_question = first_checkpoint.children[0]
    assert "Question 1 of " in first_question.value


def test_checkpoint_initialization_error_is_announced() -> None:
    """Keep unavailable checkpoint data visible to assistive technology."""
    with (
        patch.object(
            checkpoint_self_check,
            "load_checkpoint_definitions",
            side_effect=checkpoint_self_check.CheckpointDataError(
                "The checkpoint data could not be read.",
            ),
        ),
        patch.object(checkpoint_self_check, "display") as display,
    ):
        result = checkpoint_self_check.display_checkpoint_self_checks(
            "linux-shell-and-navigation",
        )

    assert result is None
    display.assert_called_once()
    error_message = display.call_args.args[0]
    assert "Checkpoint unavailable." in error_message.value
    assert "role='status'" in error_message.value
    assert "aria-live='polite'" in error_message.value


def test_bounded_checkpoint_questions_use_multiple_choice_responses() -> None:
    """Render finite-answer checkpoints as initially unselected choice groups."""
    with patch.object(checkpoint_self_check, "display") as display:
        checkpoint_self_check.display_checkpoint_self_checks(
            "linux-foundations-and-distributions",
        )

    displayed_widget = display.call_args.args[0]
    shell_layer_checkpoint = displayed_widget.children[2]
    choice_response = shell_layer_checkpoint.children[1]
    assert isinstance(choice_response, checkpoint_self_check.widgets.VBox)
    choice_label, *choice_options = choice_response.children
    assert isinstance(choice_label, checkpoint_self_check.widgets.HTML)
    assert choice_label.value == "<strong>Your answer:</strong>"
    assert all(
        isinstance(choice_option, checkpoint_self_check.widgets.Checkbox)
        for choice_option in choice_options
    )
    assert tuple(
        choice_option.description for choice_option in choice_options
    ) == (
        "The kernel",
        "User space",
    )
    assert not any(choice_option.value for choice_option in choice_options)
    assert "checkpoint-choice-answer" in choice_response._dom_classes


def test_checkpoint_definitions_reject_invalid_multiple_choice_options() -> (
    None
):
    """Reject incomplete, blank, or duplicate multiple-choice options."""
    invalid_choice_sets: tuple[list[str], ...] = (
        [],
        ["User space"],
        ["", "User space"],
        ["User space", "User space"],
    )
    for invalid_choices in invalid_choice_sets:
        checkpoint_data = {
            "checkpoints": [
                {
                    "id": "checkpoint",
                    "question": "Question",
                    "choices": invalid_choices,
                },
            ],
        }
        with patch.object(
            checkpoint_self_check,
            "load_checkpoint_data",
            return_value=checkpoint_data,
        ):
            try:
                checkpoint_self_check.load_checkpoint_definitions(
                    Path("checkpoint_data/checkpoint.json"),
                )
            except checkpoint_self_check.CheckpointDataError as error:
                assert str(error) == "The checkpoint choices are invalid."
            else:
                failure_message = (
                    "Invalid multiple-choice options were accepted."
                )
                raise AssertionError(failure_message)


def test_checkpoint_definitions_reject_invalid_correct_choice() -> None:
    """Require each multiple-choice checkpoint to name one listed answer."""
    invalid_checkpoints: tuple[dict[str, object], ...] = (
        {
            "id": "checkpoint",
            "question": "Question",
            "choices": ["The kernel", "User space"],
        },
        {
            "id": "checkpoint",
            "question": "Question",
            "choices": ["The kernel", "User space"],
            "correct_choice": "",
        },
        {
            "id": "checkpoint",
            "question": "Question",
            "choices": ["The kernel", "User space"],
            "correct_choice": "Neither",
        },
    )
    for invalid_checkpoint in invalid_checkpoints:
        checkpoint_data: dict[str, object] = {
            "checkpoints": [invalid_checkpoint]
        }
        with patch.object(
            checkpoint_self_check,
            "load_checkpoint_data",
            return_value=checkpoint_data,
        ):
            try:
                checkpoint_self_check.load_checkpoint_definitions(
                    Path("checkpoint_data/checkpoint.json"),
                )
            except checkpoint_self_check.CheckpointDataError as error:
                assert (
                    str(error) == "The checkpoint correct choice is invalid."
                )
            else:
                failure_message = "Invalid correct choice was accepted."
                raise AssertionError(failure_message)


def test_checkpoint_reveal_button_is_the_only_initial_control() -> None:
    """Keep the response and reveal control stable and accessible."""
    self_check = checkpoint_self_check.CheckpointSelfCheck(
        question_number=1,
        question="Question",
        checkpoint_id="checkpoint",
        checkpoint_data_relative_path=Path("checkpoint_data/checkpoint.json"),
        question_count=4,
    )

    assert "Question 1 of 4" in self_check.question.value
    assert self_check.reveal_button.description == "Reveal answer"
    assert self_check.reveal_button.layout.width == "140px"
    assert self_check.reveal_button.layout.min_width == "140px"
    assert self_check.reveal_button.layout.display is None
    assert self_check.reveal_button.disabled
    assert self_check.controls.children == (
        self_check.reveal_button,
        self_check.retry_button,
    )
    assert not hasattr(self_check, "confirm_button")
    assert not hasattr(self_check, "edit_button")
    assert self_check.answer.description == "Your answer:"
    assert self_check.answer.rows == 1
    assert self_check.answer.layout.height is None
    assert self_check.answer.layout.min_height is None
    assert self_check.answer.layout.width == "fit-content"
    assert self_check.answer.layout.max_width == "100%"
    assert self_check.answer.layout.margin == "0 0 12px 0"
    assert self_check.answer.layout.flex == "0 0 auto"
    assert self_check.widget.layout.width == "calc(100% - 24px)"
    assert self_check.widget.layout.margin == "0 12px 24px"
    assert "checkpoint-self-check" in self_check.widget._dom_classes
    assert (
        "field-sizing: content"
        in checkpoint_self_check.CHECKPOINT_WIDGET_STYLE
    )
    assert "width: auto" in checkpoint_self_check.CHECKPOINT_WIDGET_STYLE
    assert "max-width: 100%" in checkpoint_self_check.CHECKPOINT_WIDGET_STYLE
    assert "height: auto" in checkpoint_self_check.CHECKPOINT_WIDGET_STYLE
    textarea_rule_start = checkpoint_self_check.CHECKPOINT_WIDGET_STYLE.index(
        ".checkpoint-self-check .checkpoint-answer.widget-textarea textarea {",
    )
    textarea_rule_end = checkpoint_self_check.CHECKPOINT_WIDGET_STYLE.index(
        "}",
        textarea_rule_start,
    )
    textarea_rule = checkpoint_self_check.CHECKPOINT_WIDGET_STYLE[
        textarea_rule_start:textarea_rule_end
    ]
    assert "min-height" not in textarea_rule
    assert (
        "overflow-y: hidden" in checkpoint_self_check.CHECKPOINT_WIDGET_STYLE
    )
    assert "resize: none" in checkpoint_self_check.CHECKPOINT_WIDGET_STYLE
    assert (
        "border-radius: 4px" in checkpoint_self_check.CHECKPOINT_WIDGET_STYLE
    )
    assert (
        "--vscode-editor-background"
        in checkpoint_self_check.CHECKPOINT_WIDGET_STYLE
    )
    assert (
        "box-shadow: 0 0 0 8px "
        "var(--vscode-editor-background, var(--jp-layout-color0));"
    ) in checkpoint_self_check.CHECKPOINT_WIDGET_STYLE
    assert (
        "--vscode-editor-foreground"
        in checkpoint_self_check.CHECKPOINT_WIDGET_STYLE
    )
    assert (
        "--vscode-input-background"
        in checkpoint_self_check.CHECKPOINT_WIDGET_STYLE
    )
    assert (
        "--vscode-button-background"
        in checkpoint_self_check.CHECKPOINT_WIDGET_STYLE
    )
    assert (
        "--vscode-button-secondaryBackground"
        in checkpoint_self_check.CHECKPOINT_WIDGET_STYLE
    )
    assert (
        "--vscode-textLink-foreground"
        in checkpoint_self_check.CHECKPOINT_WIDGET_STYLE
    )
    assert (
        ".jupyter-widgets.widget-html"
        in checkpoint_self_check.CHECKPOINT_WIDGET_STYLE
    )
    assert (
        ".checkpoint-self-check .checkpoint-model-answer .widget-html-content p {"
        "line-height: 1.5;"
        "margin: 0 0 8px;"
        "}"
        in checkpoint_self_check.CHECKPOINT_WIDGET_STYLE
    )
    assert (
        ".widget-textarea .widget-label"
        in checkpoint_self_check.CHECKPOINT_WIDGET_STYLE
    )
    assert (
        ".checkpoint-self-check .checkpoint-choice-answer,"
        in checkpoint_self_check.CHECKPOINT_WIDGET_STYLE
    )
    assert (
        ".checkpoint-choice-answer label"
        in checkpoint_self_check.CHECKPOINT_WIDGET_STYLE
    )
    assert (
        ".checkpoint-choice-answer .widget-label-basic"
        in checkpoint_self_check.CHECKPOINT_WIDGET_STYLE
    )
    assert (
        "align-items: center" in checkpoint_self_check.CHECKPOINT_WIDGET_STYLE
    )
    assert (
        ".checkpoint-self-check .checkpoint-response .widget-label {"
        "font-weight: 700;"
        "}"
    ) in checkpoint_self_check.CHECKPOINT_WIDGET_STYLE
    assert "appearance: none" in checkpoint_self_check.CHECKPOINT_WIDGET_STYLE
    assert (
        "input[type='checkbox']:checked"
        in checkpoint_self_check.CHECKPOINT_WIDGET_STYLE
    )
    assert (
        "input[type='checkbox']:disabled"
        in checkpoint_self_check.CHECKPOINT_WIDGET_STYLE
    )
    assert (
        "input[type='checkbox']:disabled:checked"
        in checkpoint_self_check.CHECKPOINT_WIDGET_STYLE
    )
    assert (
        "checkpoint-choice-result-correct"
        in checkpoint_self_check.CHECKPOINT_WIDGET_STYLE
    )
    assert (
        "checkpoint-choice-result-incorrect"
        in checkpoint_self_check.CHECKPOINT_WIDGET_STYLE
    )
    assert (
        "button.checkpoint-control"
        in checkpoint_self_check.CHECKPOINT_WIDGET_STYLE
    )
    assert (
        ".checkpoint-control button"
        in checkpoint_self_check.CHECKPOINT_WIDGET_STYLE
    )
    assert (
        "button.checkpoint-control:disabled"
        in checkpoint_self_check.CHECKPOINT_WIDGET_STYLE
    )
    assert "checkpoint-answer" in self_check.answer._dom_classes
    assert "checkpoint-model-answer" in self_check.model_answer._dom_classes
    assert self_check.status.value == ""
    assert self_check.status.layout.display == "none"
    rendered_status = checkpoint_self_check.render_status("Status")
    assert "role='status'" in rendered_status
    assert "aria-live='polite'" in rendered_status
    assert "aria-atomic='true'" in rendered_status
    assert "cursor: default" in checkpoint_self_check.CHECKPOINT_WIDGET_STYLE
    assert (
        "pointer-events: none" in checkpoint_self_check.CHECKPOINT_WIDGET_STYLE
    )
    assert self_check.reveal_button.button_style == ""
    assert self_check.retry_button.button_style == ""
    assert (
        "checkpoint-primary-control" in self_check.reveal_button._dom_classes
    )
    assert (
        "checkpoint-secondary-control" in self_check.retry_button._dom_classes
    )
    for control_button in (
        self_check.reveal_button,
        self_check.retry_button,
    ):
        assert "checkpoint-control" in control_button._dom_classes


def test_multiple_choice_checkpoint_requires_a_selection() -> None:
    """Require one choice, allow deselection, and clear it on retry."""
    self_check = checkpoint_self_check.CheckpointSelfCheck(
        question_number=1,
        question="Which layer includes the shell?",
        checkpoint_id="checkpoint",
        checkpoint_data_relative_path=Path("checkpoint_data/checkpoint.json"),
        choices=("The kernel", "User space"),
    )

    assert isinstance(self_check.answer, checkpoint_self_check.widgets.VBox)
    assert len(self_check.choice_options) == 2
    assert not any(
        choice_option.value for choice_option in self_check.choice_options
    )
    assert self_check.reveal_button.disabled
    assert self_check.status.value == ""
    assert self_check.status.layout.display == "none"

    kernel_option, user_space_option = self_check.choice_options
    user_space_option.value = True
    assert self_check.get_response_value() == "User space"
    assert not self_check.reveal_button.disabled
    user_space_option.value = False
    assert self_check.get_response_value() == ""
    assert self_check.reveal_button.disabled

    kernel_option.value = True
    user_space_option.value = True
    assert not kernel_option.value
    assert user_space_option.value
    assert self_check.get_response_value() == "User space"

    with (
        patch.object(
            checkpoint_self_check,
            "load_model_answer",
            return_value=(
                "Answer",
                [{"label": "Source", "anchor": "#source"}],
            ),
        ),
        patch.object(
            checkpoint_self_check,
            "load_correct_choice",
            return_value="User space",
        ),
    ):
        self_check.reveal_answer(self_check.reveal_button)

    assert self_check.choice_result.layout.display == ""
    assert "checkpoint-choice-result-correct" in self_check.choice_result.value
    assert "aria-label='Correct'" in self_check.choice_result.value
    assert "&#10003;" in self_check.choice_result.value
    assert (
        "<strong>Correct answer:</strong> User space"
        in self_check.choice_result.value
    )
    assert (
        "<strong>Explanation:</strong> Answer" in self_check.model_answer.value
    )
    assert self_check.status.value == ""
    assert self_check.status.layout.display == "none"

    self_check.retry_answer(self_check.retry_button)
    assert not any(
        choice_option.value for choice_option in self_check.choice_options
    )
    assert all(
        not choice_option.disabled
        for choice_option in self_check.choice_options
    )
    assert self_check.reveal_button.disabled
    assert self_check.reveal_button.layout.display == ""
    assert self_check.choice_result.value == ""
    assert self_check.choice_result.layout.display == "none"
    assert self_check.status.value == ""
    assert self_check.status.layout.display == "none"


def test_multiple_choice_checkpoint_shows_cross_for_incorrect_response() -> (
    None
):
    """Show an incorrect outcome next to a locked choice response."""
    self_check = checkpoint_self_check.CheckpointSelfCheck(
        question_number=1,
        question="Which layer includes the shell?",
        checkpoint_id="checkpoint",
        checkpoint_data_relative_path=Path("checkpoint_data/checkpoint.json"),
        choices=("The kernel", "User space"),
    )
    self_check.choice_options[0].value = True

    with (
        patch.object(
            checkpoint_self_check,
            "load_model_answer",
            return_value=(
                "Answer",
                [{"label": "Source", "anchor": "#source"}],
            ),
        ),
        patch.object(
            checkpoint_self_check,
            "load_correct_choice",
            return_value="User space",
        ),
    ):
        self_check.reveal_answer(self_check.reveal_button)

    assert self_check.choice_result.layout.display == ""
    assert (
        "checkpoint-choice-result-incorrect" in self_check.choice_result.value
    )
    assert "aria-label='Incorrect'" in self_check.choice_result.value
    assert "&#10007;" in self_check.choice_result.value
    assert (
        "<strong>Correct answer:</strong> User space"
        in self_check.choice_result.value
    )
    assert (
        "<strong>Explanation:</strong> Answer" in self_check.model_answer.value
    )


def test_checkpoint_reveal_is_gated_and_locks_after_reveal() -> None:
    """Keep reveal unavailable without a response and lock it after reveal."""
    self_check = checkpoint_self_check.CheckpointSelfCheck(
        question_number=1,
        question="Question",
        checkpoint_id="checkpoint",
        checkpoint_data_relative_path=Path("checkpoint_data/checkpoint.json"),
    )

    self_check.reveal_answer(self_check.reveal_button)
    assert not self_check.answer.disabled
    assert self_check.model_answer.value == ""

    self_check.answer.value = " "
    assert self_check.reveal_button.disabled
    self_check.answer.value = "R"
    assert not self_check.reveal_button.disabled

    with patch.object(
        checkpoint_self_check,
        "load_model_answer",
        return_value=("Answer", [{"label": "Source", "anchor": "#source"}]),
    ):
        self_check.reveal_answer(self_check.reveal_button)

    assert self_check.answer.disabled
    assert self_check.reveal_button.disabled
    assert self_check.reveal_button.layout.display == "none"
    assert not self_check.retry_button.disabled
    assert self_check.retry_button.layout.display == ""
    assert self_check.status.value == ""
    assert self_check.status.layout.display == "none"

    self_check.retry_answer(self_check.retry_button)
    assert self_check.answer.value == ""
    assert not self_check.answer.disabled
    assert self_check.reveal_button.disabled
    assert self_check.reveal_button.layout.display == ""
    assert self_check.retry_button.disabled
    assert self_check.retry_button.layout.display == "none"
    assert self_check.model_answer.value == ""
    assert self_check.model_answer.layout.display == "none"


def test_checkpoint_model_answer_failure_remains_retryable() -> None:
    """Keep unavailable or corrupt model-answer data recoverable."""
    self_check = checkpoint_self_check.CheckpointSelfCheck(
        question_number=1,
        question="Question",
        checkpoint_id="checkpoint",
        checkpoint_data_relative_path=Path("checkpoint_data/checkpoint.json"),
    )
    self_check.answer.value = "Response"

    with patch.object(
        checkpoint_self_check,
        "load_model_answer",
        side_effect=checkpoint_self_check.CheckpointDataError(
            "The checkpoint data could not be read.",
        ),
    ):
        self_check.reveal_answer(self_check.reveal_button)

    assert not self_check.answer.disabled
    assert not self_check.reveal_button.disabled
    assert self_check.reveal_button.layout.display is None
    assert self_check.retry_button.disabled
    assert self_check.retry_button.layout.display == "none"
    assert self_check.model_answer.value == ""
    assert self_check.model_answer.layout.display == "none"
    assert "Model answer unavailable." in self_check.status.value
    assert "role='status'" in self_check.status.value

    with patch.object(
        checkpoint_self_check,
        "load_model_answer",
        return_value=("Answer", [{"label": "Source", "anchor": "#source"}]),
    ):
        self_check.reveal_answer(self_check.reveal_button)

    assert self_check.answer.disabled
    assert self_check.reveal_button.disabled
    assert self_check.reveal_button.layout.display == "none"
    assert not self_check.retry_button.disabled
    assert self_check.model_answer.layout.display == ""
    assert (
        "<strong>Model answer:</strong> Answer"
        in self_check.model_answer.value
    )
    assert (
        "<strong>Model answer:</strong> Answer"
        in self_check.model_answer.value
    )


def test_model_answer_links_to_source_sections() -> None:
    """Keep source links usable without adding visible source highlights."""
    rendered_answer = checkpoint_self_check.render_model_answer(
        "Answer",
        [{"label": "Source", "anchor": "#source"}],
    )

    assert (
        "<strong>Source sections above:</strong> "
        "<a href='#source' onclick='event.preventDefault()'>Source</a>."
    ) in rendered_answer
    assert "target=" not in rendered_answer


def test_checkpoint_data_matches_interactive_notebooks() -> None:
    """Keep every interactive Linux notebook paired with one sidecar."""
    expected_paths = {
        checkpoint_data_path(notebook_relative_path)
        for notebook_relative_path in INTERACTIVE_CHECKPOINT_NOTEBOOKS
    }
    assert set(CHECKPOINT_DATA_DIR.glob("*.json")) == expected_paths

    for notebook_relative_path in sorted(INTERACTIVE_CHECKPOINT_NOTEBOOKS):
        assert_reveal_self_check(
            notebook_relative_path,
            checkpoint_data_path(notebook_relative_path),
        )


def test_markdown_lists_are_spaced() -> None:
    """Keep numbered and bullet lists readable in rendered documentation."""
    markdown_documents = [README_PATH.read_text(encoding="utf-8")]

    for notebook_path in sorted(NOTEBOOK_DIR.glob("*.ipynb")):
        notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
        markdown_documents.extend(
            "".join(cell["source"])
            for cell in notebook["cells"]
            if cell["cell_type"] == "markdown"
        )

    for document in markdown_documents:
        lines = document.splitlines()
        has_tight_list = any(
            LIST_ITEM.match(line) and LIST_ITEM.match(next_line)
            for line, next_line in pairwise(lines)
        )
        assert not has_tight_list


def test_network_diagram_exists() -> None:
    """Keep the networking concepts illustration available to the notebook."""
    assert NETWORK_DIAGRAM_PATH.is_file()


def test_exercise_starters_are_valid() -> None:
    """Keep all Python and shell exercise starters syntactically valid."""
    expected_files = {
        "__init__.py",
        "hello.sh",
        "hello_1.py",
        "hello_2.py",
        "my_cat.py",
        "my_reverse_sort.py",
        "my_sort_status.py",
    }
    assert expected_files == {path.name for path in EXERCISE_DIR.iterdir()}

    for python_path in sorted(EXERCISE_DIR.glob("*.py")):
        ast.parse(
            python_path.read_text(encoding="utf-8"), filename=str(python_path)
        )

    subprocess.run(["bash", "-n", EXERCISE_DIR / "hello.sh"], check=True)

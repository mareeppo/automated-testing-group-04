import pytest
from playwright.sync_api import Page, expect

URL = "https://demo.playwright.dev/todomvc/"


# Test 1: Add a task
def test_add_task(page: Page):
    page.goto(URL)

    task_input = page.get_by_placeholder(
        "What needs to be done?",
        exact=True,
    )
    task_items = page.locator(".todo-list li")
    task_labels = task_items.locator("label")

    expect(task_items).to_have_count(0)

    task_input.fill("Read testing notes")
    task_input.press("Enter")

    expect(task_items).to_have_count(1)
    expect(task_labels).to_have_text(["Read testing notes"])
    expect(task_input).to_have_value("")

# Test 2: Complete a task
def test_complete_task(page: Page):
    page.goto(URL)

    task_input = page.get_by_placeholder(
        "What needs to be done?",
        exact=True,
    )
    task_items = page.locator(".todo-list li")

    expect(task_items).to_have_count(0)

    task_input.fill("Practise automated testing")
    task_input.press("Enter")

    expect(task_items).to_have_count(1)

    checkbox = task_items.first.get_by_role("checkbox")
    checkbox.check()

    expect(checkbox).to_be_checked()

    page.get_by_role("link", name="Completed", exact=True).click()

    expect(task_items).to_have_count(1)
    expect(task_items.locator("label")).to_have_text(
        ["Practise automated testing"]
    )

# Test 3: Blank task validation
@pytest.mark.parametrize(
    "task_text",
    ["", " ", "   "],
    ids=["empty", "one-space", "three-spaces"],
)
def test_blank_task_is_not_added(page: Page, task_text: str):
    page.goto(URL)

    task_input = page.get_by_placeholder(
        "What needs to be done?",
        exact=True,
    )
    task_items = page.locator(".todo-list li")

    expect(task_items).to_have_count(0)

    task_input.fill(task_text)
    task_input.press("Enter")

    expect(task_items).to_have_count(0)

# Test 4: Login with correct details
def test_login_with_correct_details(page: Page):
    page.goto("https://the-internet.herokuapp.com/login")

    page.get_by_label("Username").fill("tomsmith")
    page.get_by_label("Password").fill("SuperSecretPassword!")
    page.get_by_role("button", name="Login").click()

    expect(
        page.get_by_role(
            "heading",
            name="Secure Area",
            exact=True,
        )
    ).to_be_visible()

# Test 5: Login with incorrect password
def test_login_with_incorrect_password(page: Page):
    page.goto("https://the-internet.herokuapp.com/login")

    page.get_by_label("Username").fill("tomsmith")
    page.get_by_label("Password").fill("WrongPassword123")
    page.get_by_role("button", name="Login").click()

    expect(
        page.get_by_text("Your password is invalid!")
    ).to_be_visible()

    expect(
        page.get_by_role("button", name="Login")
    ).to_be_visible()

# Helper function: Add a task
def add_task(page: Page, task_name: str):
    task_input = page.get_by_placeholder(
        "What needs to be done?",
        exact=True,
    )
    task_input.fill(task_name)
    task_input.press("Enter")

# Test 6: Add two tasks
def test_add_two_tasks(page: Page):
    page.goto(URL)

    task_items = page.locator(".todo-list li")

    expect(task_items).to_have_count(0)

    add_task(page, "Read the instructions")
    add_task(page, "Practise the examples")

    expect(task_items).to_have_count(2)
    expect(task_items.locator("label")).to_have_text(
        ["Read the instructions", "Practise the examples"]
    )

# Step 12.4, Step 3. Comments! - Additional Test 1
# Scenario: Active filter with mixed items.
# Condition: Fresh session and empty list.
# Values: "Crying in my prom dress" and "Every other day, I'm wondering".
# Description: Add two epic tasks, complete the first, then select Active.
# Expected outcome: Only the unfinished task appears.

def test_active_filter_with_mixed_items(page: Page):
    page.goto(URL)

    add_task(page, "Crying in my prom dress")
    add_task(page, "Every other day, I'm wondering")

    task_items = page.locator(".todo-list li")

    # Complete the first task.
    task_items.nth(0).locator("input.toggle").check()

    # Select the Active filter.
    page.get_by_role("link", name="Active", exact=True).click()

    # Only the unfinished task should be visible.
    active_items = page.locator(".todo-list li:visible")

    expect(active_items).to_have_count(1)
    expect(active_items.locator("label")).to_have_text(
        ["Every other day, I'm wondering"]
    )

    # Save screenshot evidence.
    page.screenshot(
        path="docs/evidence/member-1/extra-test-1-active-filter.png",
        full_page=True,
    )

# Step 12.4 - Additional Test 2
# Scenario: Delete an active task.
# Condition: Fresh session with two tasks.
# Values: "High cortisol doing this" and "I wish I had low cortisol 24/7".
# Description: Add two tasks and delete the first one.
# Expected outcome: The second task remains in the list.

def test_delete_an_active_task(page: Page):
    page.goto(URL)

    add_task(page, "High cortisol doing this")
    add_task(page, "I wish I had low cortisol 24/7")

    task_items = page.locator(".todo-list li")

    expect(task_items).to_have_count(2)

    # Hover over the first task to reveal its delete button.
    first_task = task_items.nth(0)
    first_task.hover()
    first_task.locator("button.destroy").click()

    # Check that only the second task remains.
    expect(task_items).to_have_count(1)
    expect(task_items.locator("label")).to_have_text(
        ["I wish I had low cortisol 24/7"]
    )

    # Save screenshot evidence.
    page.screenshot(
        path="docs/evidence/member-1/extra-test-2-delete-task.png",
        full_page=True,
    )

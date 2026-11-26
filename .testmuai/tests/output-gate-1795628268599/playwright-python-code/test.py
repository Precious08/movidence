import os
import testmu
from testmu import expect, var, set_var
from playwright.async_api import Page

testmu.configure(
    build="eb8b7b9f-e221-456c-9040-e765f5c7d529",
    name="Incomplete Instruction List",
    tc_id="TC-8",
    network=os.getenv("NETWORK", "false").lower() == "true",
    auto_heal_version="AH2",
    default_action_timeout_ms=60000,
    default_navigation_timeout_ms=60000,
    kane_run_v4=True,
)

@testmu.test
async def test(page: Page):
    async with testmu.step('Navigate to http://localhost:8000/samples/blank.mp4', instruction_id='73a5f7d9-8541-4ed4-addb-c3f779229b72'):
        await page.goto("http://localhost:8000/samples/blank.mp4")


if __name__ == "__main__":
    testmu.run(test)
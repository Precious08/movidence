import os
import testmu
from testmu import expect, var, set_var
from playwright.async_api import Page

testmu.configure(
    build="e1ab6da1-b041-4908-b170-7b93a27bf671",
    name="Incomplete Instruction List",
    tc_id="TC-4",
    network=os.getenv("NETWORK", "false").lower() == "true",
    auto_heal_version="AH2",
    default_action_timeout_ms=60000,
    default_navigation_timeout_ms=60000,
    kane_run_v4=True,
)

@testmu.test
async def test(page: Page):
    async with testmu.step('Navigate to http://localhost:8000/player?v=http%3A%2F%2Flocalhost%3A8000%2Fsamples%2Fgood.mp4', instruction_id='f392f777-01f2-451e-91ae-c7c4866ddf57'):
        await page.goto("http://localhost:8000/player?v=http%3A%2F%2Flocalhost%3A8000%2Fsamples%2Fgood.mp4")
    
    async with testmu.step('Opening the media player page', instruction_id='11a56732-4784-496b-a934-3d5659a32dfa'):
        await page.wait_for_timeout(500)


if __name__ == "__main__":
    testmu.run(test)
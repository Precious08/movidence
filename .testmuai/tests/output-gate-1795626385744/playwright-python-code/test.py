import os
import testmu
from testmu import expect, var, set_var
from playwright.async_api import Page

testmu.configure(
    build="de43833b-0324-4fee-9b99-a5e451b76dd6",
    name="Incomplete Instruction List",
    tc_id="TC-5",
    network=os.getenv("NETWORK", "false").lower() == "true",
    auto_heal_version="AH2",
    default_action_timeout_ms=60000,
    default_navigation_timeout_ms=60000,
    kane_run_v4=True,
)

@testmu.test
async def test(page: Page):
    async with testmu.step('Navigate to http://localhost:8000/player?v=http%3A%2F%2Flocalhost%3A8000%2Fsamples%2Fblank.mp4', instruction_id='adb5709a-2918-4818-841e-1c425b721d61'):
        await page.goto("http://localhost:8000/player?v=http%3A%2F%2Flocalhost%3A8000%2Fsamples%2Fblank.mp4")


if __name__ == "__main__":
    testmu.run(test)
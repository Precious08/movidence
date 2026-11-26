import os
import testmu
from testmu import expect, var, set_var
from playwright.async_api import Page

testmu.configure(
    build="bfcb4922-a45b-4b34-a764-16753052954b",
    name="Delivery",
    tc_id="TC-7",
    network=os.getenv("NETWORK", "false").lower() == "true",
    auto_heal_version="AH2",
    default_action_timeout_ms=60000,
    default_navigation_timeout_ms=60000,
    kane_run_v4=True,
)

@testmu.test
async def test(page: Page):
    async with testmu.step('Navigate to http://localhost:8000/samples/blank.mp4', instruction_id='3d0853b7-cac3-48e5-82ad-d65ac9b41e55'):
        await page.goto("http://localhost:8000/samples/blank.mp4")


if __name__ == "__main__":
    testmu.run(test)
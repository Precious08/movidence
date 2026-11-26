import os
import testmu
from testmu import expect, var, set_var
from playwright.async_api import Page

testmu.configure(
    build="77eaf7ea-a632-4aa9-b0d5-2c7deb1229f4",
    name="Delivery",
    tc_id="TC-6",
    network=os.getenv("NETWORK", "false").lower() == "true",
    auto_heal_version="AH2",
    default_action_timeout_ms=60000,
    default_navigation_timeout_ms=60000,
    kane_run_v4=True,
)

@testmu.test
async def test(page: Page):
    async with testmu.step('Navigate to http://localhost:8000/player?v=http%3A%2F%2Flocalhost%3A8000%2Fsamples%2Fblank.mp4', instruction_id='5e7964f2-ca14-4a9a-960d-d647864b6e03'):
        await page.goto("http://localhost:8000/player?v=http%3A%2F%2Flocalhost%3A8000%2Fsamples%2Fblank.mp4")
    
    async with testmu.step('Clicking play in the video player controls', instruction_id='1c4ecf97-4d6e-4982-8738-e4e7589a0404'):
        _loc_1 = page.locator("role=button[name='play']")
        
        await _loc_1.click()
    _condition_met = False
    _until_retries = 0
    while _until_retries < 10:
        print(f"[until-loop] iteration {_until_retries + 1}/10")
        async with testmu.step('Waiting for video playback to finish', instruction_id='85bfb206-ea5f-4e6b-ab16-c928fc5b3824'):
            await page.wait_for_timeout(1000)
        await page.wait_for_timeout(500)
        if await testmu.check_until_condition(page, 'the video control button is labeled "play"'):
            _condition_met = True
            break
        _until_retries += 1
    set_var("__result__", {"condition_met": _condition_met, "retries": _until_retries + 1})


if __name__ == "__main__":
    testmu.run(test)
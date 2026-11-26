import os
import testmu
from testmu import expect, var, set_var
from playwright.async_api import Page

testmu.configure(
    build="06c03212-5abc-410e-a276-e104ef839e73",
    name="Delivery",
    tc_id="TC-9",
    network=os.getenv("NETWORK", "false").lower() == "true",
    auto_heal_version="AH2",
    default_action_timeout_ms=60000,
    default_navigation_timeout_ms=60000,
    kane_run_v4=True,
)

@testmu.test
async def test(page: Page):
    async with testmu.step('Navigate to http://localhost:8000/samples/good.mp4', instruction_id='1493ad19-88a8-44a0-8c73-ec64ab60a801'):
        await page.goto("http://localhost:8000/samples/good.mp4")
    
    async with testmu.step("Hover over 'the centered video player'", instruction_id='66d9ee66-6894-4f93-8590-54e9c2fc1b68'):
        coords = await testmu.get_vision_coordinates(page, "Hover over 'the centered video player'", "click", 960, 540)
        await page.mouse.move(coords['x'], coords['y'])
        
    
    async with testmu.step('PRIMARY: Delivery; role=button; text="Play" | HINTS: position=bottom-left of the centered video player\'s control bar', instruction_id='cf98c2f9-1343-4a77-a46e-8a64916c0595'):
        coords = await testmu.get_vision_coordinates(page, 'PRIMARY: Delivery; role=button; text="Play" | HINTS: position=bottom-left of the centered video player\'s control bar', "click", 662, 669)
        await page.mouse.click(coords['x'], coords['y'])
        
    _condition_met = False
    _until_retries = 0
    while _until_retries < 10:
        print(f"[until-loop] iteration {_until_retries + 1}/10")
        async with testmu.step('Waiting for the video to finish playing', instruction_id='a4176c59-57ce-4208-8b97-88656512a81b'):
            await page.wait_for_timeout(1000)
        await page.wait_for_timeout(500)
        if await testmu.check_until_condition(page, 'the video reaches its end time indicator "0:06 / 0:06"'):
            _condition_met = True
            break
        _until_retries += 1
    set_var("__result__", {"condition_met": _condition_met, "retries": _until_retries + 1})


if __name__ == "__main__":
    testmu.run(test)
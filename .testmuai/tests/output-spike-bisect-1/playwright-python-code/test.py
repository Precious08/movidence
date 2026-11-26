import os
import testmu
from testmu import expect, var, set_var
from playwright.async_api import Page

testmu.configure(
    build="8d2d2501-9482-48d1-a1ef-1b7594966970",
    name="Verify Video Playback Quality",
    tc_id="TC-11",
    network=os.getenv("NETWORK", "false").lower() == "true",
    variables={"video_playing_check": "false", "moving_video_content_visible": "true", "black_or_blank_screen": "false"},
    auto_heal_version="AH2",
    default_action_timeout_ms=60000,
    default_navigation_timeout_ms=60000,
    kane_run_v4=True,
)

@testmu.test
async def test(page: Page):
    async with testmu.step('Navigate to http://localhost:8000/samples/good.mp4', instruction_id='f1631c49-e471-4a9d-be89-c621b7f3527c'):
        await page.goto("http://localhost:8000/samples/good.mp4")
    
    async with testmu.step('whether the file http://localhost:8000/samples/good.mp4 is playing in the visible video player', instruction_id='8575d9b0-7fd1-4beb-94da-0ca47b59d5c4'):
        set_var('video_playing_check', await testmu.vision_query(page, "whether the file http://localhost:8000/samples/good.mp4 is playing in the visible video player", ""))
    if await testmu.evaluate_branch(sub_checks=[{'description': 'The file http://localhost:8000/samples/good.mp4 is not already playing.', 'store_key': 'video_playing_check', 'expected_value': 'false', 'stored_value': '{{video_playing_check}}', 'extracted_value': '{{video_playing_check}}', 'operator': 'equals', 'transforms': []}], composite_operator="and"):
        async with testmu.step('Pressing play', instruction_id='04d02476-76c5-4517-a958-579be110d6bf'):
            _loc_1 = page.locator("role=button[name='play']")
            
            await _loc_1.click()
    
    async with testmu.step('Waiting for the video to play for several seconds', instruction_id='c06c5f9e-0653-4a44-966e-628badf7206d'):
        await page.wait_for_timeout(4000)
    
    async with testmu.step('whether moving video frames with real visible picture content are visible in the video player at the center of the screen', instruction_id='36918ae0-f66b-4f79-b1bf-b727b744243f'):
        set_var('moving_video_content_visible', await testmu.vision_query(page, "whether moving video frames with real visible picture content are visible in the video player at the center of the screen", ""))
    
    async with testmu.step('whether the video player in the center of the viewport displays a black or blank screen instead of a picture frame', instruction_id='f4dc37ff-e75e-40e4-9924-446750d0a696'):
        set_var('black_or_blank_screen', await testmu.vision_query(page, "whether the video player in the center of the viewport displays a black or blank screen instead of a picture frame", ""))
    
    async with testmu.step('Assertion check', instruction_id='5901a1da-bab4-42f2-a78e-f9d8f37d1838'):
        await testmu.verify_assertion(page, 'Assertion check', {'operator': ['equals'], 'assertion_operands': [], 'left_operand': None, 'right_operand': None, 'operands': [], 'sub_results': [{'description': 'Moving video frames with real visible picture content are on screen.', 'passed': True, 'operator': 'equals', 'transforms': [], 'json_path': None, 'expected': 'true', 'extracted_value': '{{moving_video_content_visible}}', 'store_key': 'moving_video_content_visible', 'variable_refs': {'{{moving_video_content_visible}}': 'true'}}, {'description': 'A black or blank screen is not on screen.', 'passed': True, 'operator': 'equals', 'transforms': [], 'json_path': None, 'expected': 'false', 'extracted_value': '{{black_or_blank_screen}}', 'store_key': 'black_or_blank_screen', 'variable_refs': {'{{black_or_blank_screen}}': 'false'}}], 'sub_checks': [{'description': 'Moving video frames with real visible picture content are on screen.', 'store_key': 'moving_video_content_visible', 'expected_value': 'true', 'extracted_value': '{{moving_video_content_visible}}', 'operator': 'equals', 'transforms': []}, {'description': 'A black or blank screen is not on screen.', 'store_key': 'black_or_blank_screen', 'expected_value': 'false', 'extracted_value': '{{black_or_blank_screen}}', 'operator': 'equals', 'transforms': []}], 'composite_operator': 'and', 'claim': 'Moving video frames with real visible picture content are on screen -- not a black or blank screen.'})


if __name__ == "__main__":
    testmu.run(test)
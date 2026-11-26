import os
import testmu
from testmu import expect, var, set_var
from playwright.async_api import Page

testmu.configure(
    build="9df0c6c3-8406-4c09-80b4-381385ed109a",
    name="Verify Video Playback Quality",
    tc_id="TC-13",
    network=os.getenv("NETWORK", "false").lower() == "true",
    variables={"video_playing_check": "false", "black_or_blank_screen": "false", "moving_video_frames_visible": "true"},
    auto_heal_version="AH2",
    default_action_timeout_ms=60000,
    default_navigation_timeout_ms=60000,
    kane_run_v4=True,
)

@testmu.test
async def test(page: Page):
    async with testmu.step('Navigate to http://localhost:8000/samples/good.mp4', instruction_id='d88427a8-3bb3-450b-9f57-d6673ace3573'):
        await page.goto("http://localhost:8000/samples/good.mp4")
    
    async with testmu.step('whether the video is playing in the centered media player', instruction_id='73e8d2bf-7aaa-4573-b1ae-9b0bf2212d21'):
        set_var('video_playing_check', await testmu.vision_query(page, "whether the video is playing in the centered media player", ""))
    if await testmu.evaluate_branch(sub_checks=[{'description': 'The video is not already playing.', 'store_key': 'video_playing_check', 'expected_value': 'false', 'stored_value': '{{video_playing_check}}', 'extracted_value': '{{video_playing_check}}', 'operator': 'equals', 'transforms': []}], composite_operator="and"):
        async with testmu.step('Clicking play button in video controls', instruction_id='4a08a787-4797-423f-80d0-889f4e11a355'):
            _loc_1 = page.locator("role=button[name='play']")
            
            await _loc_1.click()
    
    async with testmu.step('Waiting for the MP4 to play for several seconds', instruction_id='67291fc8-d5ec-4118-83e6-7a9275efc047'):
        await page.wait_for_timeout(4000)
    
    async with testmu.step('whether a black or blank screen is present in the visible video player at the center of the screen', instruction_id='51b7572a-a18d-41f8-9542-02f6b10718cd'):
        set_var('black_or_blank_screen', await testmu.vision_query(page, "whether a black or blank screen is present in the visible video player at the center of the screen", ""))
    
    async with testmu.step('whether the central video player visibly displays a colorful color-bar test picture with animated graphic elements and an on-frame time counter', instruction_id='1349d887-7043-4244-840e-b3098845794f'):
        set_var('moving_video_frames_visible', await testmu.vision_query(page, "whether the central video player visibly displays a colorful color-bar test picture with animated graphic elements and an on-frame time counter", ""))
    
    async with testmu.step('Assertion check', instruction_id='bb9e3020-7ba5-48d7-91e3-ae77f071a600'):
        await testmu.verify_assertion(page, 'Assertion check', {'operator': ['equals'], 'assertion_operands': [], 'left_operand': None, 'right_operand': None, 'operands': [], 'sub_results': [{'description': 'Moving video frames with real visible picture content are on screen.', 'passed': True, 'operator': 'equals', 'transforms': [], 'json_path': None, 'expected': 'true', 'extracted_value': '{{moving_video_frames_visible}}', 'store_key': 'moving_video_frames_visible', 'variable_refs': {'{{moving_video_frames_visible}}': 'true'}}, {'description': 'A black or blank screen is not on screen.', 'passed': True, 'operator': 'equals', 'transforms': [], 'json_path': None, 'expected': 'false', 'extracted_value': '{{black_or_blank_screen}}', 'store_key': 'black_or_blank_screen', 'variable_refs': {'{{black_or_blank_screen}}': 'false'}}], 'sub_checks': [{'description': 'Moving video frames with real visible picture content are on screen.', 'store_key': 'moving_video_frames_visible', 'expected_value': 'true', 'extracted_value': '{{moving_video_frames_visible}}', 'operator': 'equals', 'transforms': []}, {'description': 'A black or blank screen is not on screen.', 'store_key': 'black_or_blank_screen', 'expected_value': 'false', 'extracted_value': '{{black_or_blank_screen}}', 'operator': 'equals', 'transforms': []}], 'composite_operator': 'and', 'claim': 'Moving video frames with real visible picture content are on screen — not a black or blank screen.'})


if __name__ == "__main__":
    testmu.run(test)
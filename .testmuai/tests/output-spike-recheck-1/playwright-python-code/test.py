import os
import testmu
from testmu import expect, var, set_var
from playwright.async_api import Page

testmu.configure(
    build="66892699-c4c7-42e7-a5dd-3a604a876a31",
    name="Verify Video Playback",
    tc_id="TC-10",
    network=os.getenv("NETWORK", "false").lower() == "true",
    variables={"video_playing_check": "false", "moving_video_frames_visible": "true", "black_or_blank_screen_visible": "false"},
    auto_heal_version="AH2",
    default_action_timeout_ms=60000,
    default_navigation_timeout_ms=60000,
    kane_run_v4=True,
)

@testmu.test
async def test(page: Page):
    async with testmu.step('Navigate to https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/720/Big_Buck_Bunny_720_10s_1MB.mp4', instruction_id='8daaed8e-f22f-41c5-9210-1fd7c28348ea'):
        await page.goto("https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/720/Big_Buck_Bunny_720_10s_1MB.mp4")
    
    async with testmu.step('Checking whether the video is playing'):
        set_var('video_playing_check', await testmu.textual_analyzer(page, wrapped_js="(els) => {\n  const __m = {1: 0};\n  const el = (i) => els[__m[i]];\n  const __v = (el(1).matches(':playing'));\n  return (typeof __v === 'boolean' ? String(__v) : __v);\n}", locators=['video'], query='whether the video element on the page is playing', expected_value='false', needs_unit_conversion=False, operator='equals', transforms=[], condition='the video is not already playing'))
    if await testmu.evaluate_branch(sub_checks=[{'description': 'the video is not already playing', 'store_key': 'video_playing_check', 'expected_value': 'false', 'stored_value': '{{video_playing_check}}', 'extracted_value': '{{video_playing_check}}', 'operator': 'equals', 'transforms': []}], composite_operator="and"):
        async with testmu.step('Clicking play in the video controls', instruction_id='b9caac36-7558-45de-ab65-0aa14a6d01d6'):
            _loc_1 = page.locator("role=button[name='play']")
            
            await _loc_1.click()
    
    async with testmu.step('Waiting for it to play for several seconds', instruction_id='1fe80619-fba6-4980-8650-8e4a2808dfe7'):
        await page.wait_for_timeout(5000)
    
    async with testmu.step('whether moving video frames with real visible picture content are present in the on-screen video player', instruction_id='e1b415ac-022f-4207-981e-31d222e41a11'):
        set_var('moving_video_frames_visible', await testmu.vision_query(page, "whether moving video frames with real visible picture content are present in the on-screen video player", ""))
    
    async with testmu.step('whether a black or blank screen is present on screen', instruction_id='4564ce0a-0b7f-4a83-8645-8196fa8643d3'):
        set_var('black_or_blank_screen_visible', await testmu.vision_query(page, "whether a black or blank screen is present on screen", ""))
    
    async with testmu.step('Assertion check', instruction_id='4139be85-5942-4566-9bf1-f44e44bee41b'):
        await testmu.verify_assertion(page, 'Assertion check', {'operator': ['equals'], 'assertion_operands': [], 'left_operand': None, 'right_operand': None, 'operands': [], 'sub_results': [{'description': 'moving video frames with real visible picture content are on screen', 'passed': True, 'operator': 'equals', 'transforms': [], 'json_path': None, 'expected': 'true', 'extracted_value': '{{moving_video_frames_visible}}', 'store_key': 'moving_video_frames_visible', 'variable_refs': {'{{moving_video_frames_visible}}': 'true'}}, {'description': 'a black or blank screen is not on screen', 'passed': True, 'operator': 'equals', 'transforms': [], 'json_path': None, 'expected': 'false', 'extracted_value': '{{black_or_blank_screen_visible}}', 'store_key': 'black_or_blank_screen_visible', 'variable_refs': {'{{black_or_blank_screen_visible}}': 'false'}}], 'sub_checks': [{'description': 'moving video frames with real visible picture content are on screen', 'store_key': 'moving_video_frames_visible', 'expected_value': 'true', 'extracted_value': '{{moving_video_frames_visible}}', 'operator': 'equals', 'transforms': []}, {'description': 'a black or blank screen is not on screen', 'store_key': 'black_or_blank_screen_visible', 'expected_value': 'false', 'extracted_value': '{{black_or_blank_screen_visible}}', 'operator': 'equals', 'transforms': []}], 'composite_operator': 'and', 'claim': 'moving video frames with real visible picture content are on screen -- not a black or blank screen.'})


if __name__ == "__main__":
    testmu.run(test)
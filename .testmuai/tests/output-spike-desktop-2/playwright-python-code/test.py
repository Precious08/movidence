import os
import testmu
from testmu import expect, var, set_var
from playwright.async_api import Page

testmu.configure(
    build="c68e66e1-13b2-4a2a-9160-9e2bffcbbca5",
    name="Verify Video Playback",
    tc_id="TC-2",
    network=os.getenv("NETWORK", "false").lower() == "true",
    variables={"video_playing_check": "false", "moving_video_picture_content": "true", "black_screen_absent": "false", "blank_screen_absent": "false"},
    auto_heal_version="AH2",
    default_action_timeout_ms=60000,
    default_navigation_timeout_ms=60000,
    kane_run_v4=True,
)

@testmu.test
async def test(page: Page):
    async with testmu.step('Navigate to https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/720/Big_Buck_Bunny_720_10s_1MB.mp4', instruction_id='6198d623-375a-4aaf-a5d4-bda9575d8de7'):
        await page.goto("https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/720/Big_Buck_Bunny_720_10s_1MB.mp4")
    
    async with testmu.step('Waiting for the video to open at the start URL', instruction_id='74844935-ebcc-4320-a216-f145831bfd3a'):
        await page.wait_for_timeout(1000)
    
    async with testmu.step('Checking whether the video is playing'):
        set_var('video_playing_check', await testmu.textual_analyzer(page, wrapped_js="(els) => {\n  const __m = {1: 0};\n  const el = (i) => els[__m[i]];\n  const __v = (!el(1).paused && !el(1).ended);\n  return (typeof __v === 'boolean' ? String(__v) : __v);\n}", locators=['video'], query='whether the video element is playing', expected_value='false', needs_unit_conversion=False, operator='equals', transforms=[], condition='The video is not already playing.'))
    if await testmu.evaluate_branch(sub_checks=[{'description': 'The video is not already playing.', 'store_key': 'video_playing_check', 'expected_value': 'false', 'stored_value': '{{video_playing_check}}', 'extracted_value': '{{video_playing_check}}', 'operator': 'equals', 'transforms': []}], composite_operator="and"):
        async with testmu.step('Clicking play button', instruction_id='63499ee5-7ebb-44ac-ad16-8618115d5dc9'):
            _loc_1 = page.locator("role=button[name='play']")
            
            await _loc_1.click()
    
    async with testmu.step('Letting the video play for several seconds', instruction_id='1f136d9e-0bce-4fd7-b7fb-895f11935d87'):
        await page.wait_for_timeout(4000)
    
    async with testmu.step('Clicking play button on video controls', instruction_id='11242a60-b2db-42c0-a72d-99f5069d4ff0'):
        _loc_2 = page.locator("role=button[name='play']")
        
        await _loc_2.click()
    
    async with testmu.step('whether moving video frames with real visible picture content are present in the video player', instruction_id='80f447d3-a8c0-4886-a695-03b1621646f0'):
        set_var('moving_video_picture_content', await testmu.vision_query(page, "whether moving video frames with real visible picture content are present in the video player", ""))
    
    async with testmu.step('whether a black screen is present in the visible video player area', instruction_id='2d187ad4-2a29-412b-9888-05a26f20f23b'):
        set_var('black_screen_absent', await testmu.vision_query(page, "whether a black screen is present in the visible video player area", ""))
    
    async with testmu.step('whether a blank screen is present in the visible video player area', instruction_id='dae185a2-8b2f-423d-9b38-9ab36ce87d31'):
        set_var('blank_screen_absent', await testmu.vision_query(page, "whether a blank screen is present in the visible video player area", ""))
    
    async with testmu.step('Assertion check', instruction_id='3d03c6fe-f319-45b1-a183-48784ea327fd'):
        await testmu.verify_assertion(page, 'Assertion check', {'operator': ['equals'], 'assertion_operands': [], 'left_operand': None, 'right_operand': None, 'operands': [], 'sub_results': [{'description': 'Moving video frames with real visible picture content are on screen.', 'passed': True, 'operator': 'equals', 'transforms': [], 'json_path': None, 'expected': 'true', 'extracted_value': '{{moving_video_picture_content}}', 'store_key': 'moving_video_picture_content', 'variable_refs': {'{{moving_video_picture_content}}': 'true'}}, {'description': 'A black screen is not on screen.', 'passed': True, 'operator': 'equals', 'transforms': [], 'json_path': None, 'expected': 'false', 'extracted_value': '{{black_screen_absent}}', 'store_key': 'black_screen_absent', 'variable_refs': {'{{black_screen_absent}}': 'false'}}, {'description': 'A blank screen is not on screen.', 'passed': True, 'operator': 'equals', 'transforms': [], 'json_path': None, 'expected': 'false', 'extracted_value': '{{blank_screen_absent}}', 'store_key': 'blank_screen_absent', 'variable_refs': {'{{blank_screen_absent}}': 'false'}}], 'sub_checks': [{'description': 'Moving video frames with real visible picture content are on screen.', 'store_key': 'moving_video_picture_content', 'expected_value': 'true', 'extracted_value': '{{moving_video_picture_content}}', 'operator': 'equals', 'transforms': []}, {'description': 'A black screen is not on screen.', 'store_key': 'black_screen_absent', 'expected_value': 'false', 'extracted_value': '{{black_screen_absent}}', 'operator': 'equals', 'transforms': []}, {'description': 'A blank screen is not on screen.', 'store_key': 'blank_screen_absent', 'expected_value': 'false', 'extracted_value': '{{blank_screen_absent}}', 'operator': 'equals', 'transforms': []}], 'composite_operator': 'and', 'claim': 'moving video frames with real visible picture content are on screen -- not a black or blank screen.'})


if __name__ == "__main__":
    testmu.run(test)
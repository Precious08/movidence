---
mode: testing
max_steps: 50
timeout: 600
target: chrome
---

# Session: spike-bisect-1

## Step 1
Delivery check gate-TEST for the file http://localhost:8000/samples/good.mp4. Open the video at the start URL. If it is not already playing, press play. Let it play for several seconds. Verify that moving video frames with real visible picture content are on screen -- not a black or blank screen.

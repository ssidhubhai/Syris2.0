import subprocess, os, time, json, urllib.request

for _ in range(15):
    try:
        urllib.request.urlopen("http://localhost:3000")
        print("Server ready!")
        break
    except Exception:
        time.sleep(1)

artifact_dir = r"C:\Users\Admin\.gemini\antigravity\brain\fe64014f-34ff-41a3-83d2-565cf60421c0"
chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# Standard viewports for responsive workspace QA
viewports = [
    ("desktop_workspace_1440.png", "1440,1200"),
    ("laptop_workspace_1024.png", "1024,768"),
    ("tablet_workspace_820.png", "820,1180"),
    ("mobile_workspace_390.png", "390,844"),
]

for filename, size in viewports:
    out_path = os.path.join(artifact_dir, filename)
    cmd = [
        chrome,
        "--headless=new",
        "--disable-gpu",
        f"--window-size={size}",
        f"--screenshot={out_path}",
        "http://localhost:3000"
    ]
    subprocess.run(cmd, capture_output=True)
    if os.path.exists(out_path):
        print(f"Captured {filename}: {os.path.getsize(out_path)} bytes")


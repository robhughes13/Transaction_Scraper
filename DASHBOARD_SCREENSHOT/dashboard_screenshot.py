import os
import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from datetime import datetime
import pyautogui
pyautogui.FAILSAFE = False  # Disables the emergency stop feature
# Set up Edge WebDriver
options = Options()
# options.add_argument("--headless")  # Run in headless mode (no GUI)
options.add_argument(r"user-data-dir=C:\Users\rhughes\AppData\Local\Microsoft\Edge\User Data")  # Replace with your Edge profile path
options.add_argument(r"profile-directory=Default")  # Use default profile
options.add_argument("--auth-server-whitelist=*pbireports")  # Allows automatic login
options.add_argument("--auth-negotiate-delegate-whitelist=*pbireports")  # Uses Windows credentials
options.add_argument("--start-maximized")  # Maximizes the window
service = Service(r"\\wf.local\dmfiles\ETL\internal\Executables\Edge_Webdriver\msedgedriver.exe")  # Update with your Edge driver path
driver = webdriver.Edge(service=service, options=options)


# URL of the dashboard
dashboard_url = "http://pbireports/Reports/powerbi/Leadership%20Team/Leadership%20Daily%20Totals%20(UPDATED%20JUNE%202023)"
opening_url= "http://www.google.com"

try:
    
    # Open the webpage
    driver.get(opening_url)
    0
    # Wait for the page to load (adjust as needed)
    time.sleep(10)  

    # Open the webpage
    driver.get(dashboard_url)
    
    # Wait for the page to load (adjust as needed)
    time.sleep(5)  

    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Define save directory (ensure this path exists)
    save_dir = r"\\wf.local\dmfiles\ETL\internal\Executables\Tools\Dashboard Screenshots"
    os.makedirs(save_dir, exist_ok=True)

    # Screenshot file path
    screenshot_path = os.path.join(save_dir, f"dashboard_{timestamp}.png")

    # Capture and save the screenshot
    driver.save_screenshot(screenshot_path)
    print(f"Screenshot saved: {screenshot_path}")

finally:
    # Close the browser
    driver.quit()

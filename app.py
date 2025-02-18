import tkinter as tk
from tkinter import messagebox, ttk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import random
import time
import logging

# Set up logging
logging.basicConfig(filename="browser_automation.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# List of user-agent strings for rotation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
]

def open_browser_tabs(urls, num_tabs, scroll_speed, scroll_duration, headless, random_clicks, num_clicks, proxy):
    try:
        options = Options()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--start-maximized")
        options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")
        if proxy:
            options.add_argument(f"--proxy-server={proxy}")

        driver = webdriver.Chrome(options=options)

        for i in range(num_tabs):
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[-1])
            url = urls[i % len(urls)]
            driver.get(url)
            logging.info(f"Opened tab {i + 1} with URL: {url}")

            if random_clicks:
                clickable_elements = driver.find_elements(By.CSS_SELECTOR, "a, button, input[type='submit'], [onclick]")
                if clickable_elements:
                    for _ in range(num_clicks):
                        element = random.choice(clickable_elements)
                        try:
                            element.click()
                            logging.info(f"Clicked on element: {element.text}")
                            time.sleep(1)
                        except Exception as e:
                            logging.warning(f"Could not click on element: {e}")

            start_time = time.time()
            while time.time() - start_time < scroll_duration:
                driver.execute_script("window.scrollBy(0, 100);")
                time.sleep(scroll_speed)
                logging.info(f"Scrolled in tab {i + 1}")

            progress_var.set((i + 1) / num_tabs * 100)
            root.update_idletasks()

        messagebox.showinfo("Success", f"{num_tabs} tabs opened successfully!")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        time.sleep(5)
        driver.quit()

def on_submit():
    try:
        urls = entry_urls.get("1.0", tk.END).strip().splitlines()
        num_tabs = int(entry_tabs.get())
        scroll_speed = float(entry_scroll_speed.get())
        scroll_duration = float(entry_scroll_duration.get())
        headless = headless_var.get()
        random_clicks = random_clicks_var.get()
        num_clicks = int(entry_num_clicks.get())
        proxy = entry_proxy.get().strip()

        if not urls:
            messagebox.showwarning("Input Error", "Please enter at least one valid URL.")
            return
        if num_tabs <= 0:
            messagebox.showwarning("Input Error", "Number of tabs must be greater than 0.")
            return

        open_browser_tabs(urls, num_tabs, scroll_speed, scroll_duration, headless, random_clicks, num_clicks, proxy)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values for inputs.")

root = tk.Tk()
root.title("Advanced Browser Automation")

tk.Label(root, text="Enter URLs (one per line):").grid(row=0, column=0, padx=10, pady=10, sticky="w")
entry_urls = tk.Text(root, width=50, height=5)
entry_urls.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Number of Tabs:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
entry_tabs = tk.Entry(root)
entry_tabs.grid(row=1, column=1, padx=10, pady=10)
entry_tabs.insert(0, "10")

tk.Label(root, text="Scroll Speed (seconds):").grid(row=2, column=0, padx=10, pady=10, sticky="w")
entry_scroll_speed = tk.Entry(root)
entry_scroll_speed.grid(row=2, column=1, padx=10, pady=10)
entry_scroll_speed.insert(0, "1")

tk.Label(root, text="Scroll Duration (seconds):").grid(row=3, column=0, padx=10, pady=10, sticky="w")
entry_scroll_duration = tk.Entry(root)
entry_scroll_duration.grid(row=3, column=1, padx=10, pady=10)
entry_scroll_duration.insert(0, "10")

tk.Label(root, text="Number of Random Clicks:").grid(row=4, column=0, padx=10, pady=10, sticky="w")
entry_num_clicks = tk.Entry(root)
entry_num_clicks.grid(row=4, column=1, padx=10, pady=10)
entry_num_clicks.insert(0, "3")

tk.Label(root, text="Proxy (optional):").grid(row=5, column=0, padx=10, pady=10, sticky="w")
entry_proxy = tk.Entry(root)
entry_proxy.grid(row=5, column=1, padx=10, pady=10)

headless_var = tk.BooleanVar()
tk.Checkbutton(root, text="Run in Headless Mode", variable=headless_var).grid(row=6, column=1, padx=10, pady=10, sticky="w")

random_clicks_var = tk.BooleanVar()
tk.Checkbutton(root, text="Enable Random Clicks", variable=random_clicks_var).grid(row=7, column=1, padx=10, pady=10, sticky="w")

submit_button = tk.Button(root, text="Start Automation", command=on_submit)
submit_button.grid(row=8, column=1, padx=10, pady=20)

progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
progress_bar.grid(row=9, column=1, padx=10, pady=10)

root.mainloop()

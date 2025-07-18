# Slovak Land Scraper

## ✨ Features

* ### Triple-Threat Scraping
    We hit up Bazoš, Reality.sk, and Topreality.sk. Because why limit yourself to one portal when you can stalk three?
* ### Daily Deals
    Only interested in what popped up *today*? We got you. This scraper focuses on the freshest listings, so you're always ahead of the curve (or at least, the other land-hungry folks). I am using task scheduler on my server at 11:59 PC to scrape everything new from that day.
* ### Inbox Invasion (the good kind!)
    Get a beautifully formatted HTML email with all the juicy details of new listings. Think of it as your daily dose of digital real estate eye candy.
* ### URL Whisperer
    Want land in "Somewhereville" with a budget of "just under a million"? Just filter it on the website, copy the URL, and paste it into `main.py`. Easy peasy, lemon squeezy.

## 🛠️ Technologies Under the Hood

* ### Python
    The magic wand that makes it all happen.
* ### Requests
    For when you need to politely (or not-so-politely) ask websites for their data. But this program is still taking a lot of effort to not kill the website, just to peek inside, take what is needed - waiting 2 seconds before new request occur.
* ### BeautifulSoup4 (bs4)
    Our digital surgeon, dissecting HTML to find exactly what we need.
* ### python-dotenv
    Keeps your email password safer than your grandma's secret cookie recipe.
* ### smtplib & email.message
    For sending emails without needing a carrier pigeon (you know, they are messy).
* ### datetime & time
    Because timing is everything, especially when you're trying not to get blocked by angry websites.

## 🚀 Setup & Installation (Get Your Hands Dirty!)

1.  ### Clone This Masterpiece
    ```bash
    git clone [https://github.com/YourUsername/YourRepoName.git](https://github.com/YourUsername/YourRepoName.git) # Replace with your actual repo URL
    cd YourRepoName
    ```

2.  ### Conjure a Virtual Environment (highly recommended, don't be a savage)
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, it's `venv\Scripts\activate`
    ```

3.  ### Install the Digital Tools
    ```bash
    pip install requests beautifulsoup4 python-dotenv
    ```

4.  ### Hide Your Secrets (Email Credentials)
    Create a folder named `credentials` in the root of your project (same level as `main.py`).
    Inside `credentials`, create a file named `mail.env`.
    Add your email details like so:
    ```
    EMAIL="your_email@gmail.com"
    PASS="your_app_password" # Seriously, use an App Password for Gmail if you have 2FA. Don't risk your main password!
    ```
    *Why an App Password?* Because your Google account loves security more than you love coffee. If you use 2-Factor Authentication, a regular password won't cut it for programmatic access. Go to your Google Account security settings and generate one!

## 🏃‍♂️ How to Run This

1.  ### Tailor Your Search
    Open `main.py`. See those `bazos_url`, `reality_url`, and `topreality_url` variables? Those are your playgrounds. Go to the respective websites, apply all your filters (location, price, if the previous owner was a wizard, etc.), and then just copy the resulting URL. Paste it in!
    *(Pro Tip: The `topreality_nexpage_part_one/two/three` and `bazos_next_page_part_one/two/three` variables are for navigating paginated results. They're mostly fine as is for initial setup, but good to know they exist!)*

2.  ### Unleash the Scraper!
    In your terminal (with the virtual environment activated, remember?), run:
    ```bash
    python main.py
    ```
    The script will whir into action. If it finds new ads from today, it'll send you an email. It also creates a `Last_24_hours_search.html` file locally, just in case your email server decides to take a nap.

## 📂 Project Blueprint

* ### `main.py`
    The conductor of this web scraping orchestra. It calls the shots.
* ### `property_scrapers/`
    Where the real magic happens, split by website.
    * `bazos_scrape.py`: Your Bazoš specialist.
    * `reality_scrape.py`: Your Reality.sk specialist.
    * `topreality_scrape.py`: Your Topreality.sk specialist.
* ### `email_sender/email_sender.py`
    The mailman, meticulously crafting and delivering your land reports.
* ### `credentials/mail.env`
    (You create this!) Your secret stash for email login info. Shhh!
* ### `database_management.py`
    A lonely file, currently empty, dreaming of a future where it can store all your precious land data. Maybe later, little guy.

## 📈 Future Dreams (If You're Feeling Ambitious)

* ### Database Love
    Let's give `database_management.py` a purpose! Store historical data, prevent duplicate notifications, and maybe even build a fancy dashboard.
* ### Bulletproof Error Handling
    Websites are fickle. Let's make this scraper more resilient to their mood swings.
* ### Externalize EVERYTHING
    Configuration files for every tiny setting! Because hardcoding is for amateurs.
* ### Fancy Logging
    Know exactly what the scraper is doing, when, and why.
* ### Dockerize It!
    Package this beauty in a Docker container for effortless deployment anywhere.
* ### Set It and Forget It
    Integrate with `cron` (Linux/macOS) or Task Scheduler (Windows) for fully automated daily runs.
    For windows I recommend to use batch file to run python script, for me it is working better.
    ```batch
    @echo off
    cd "C:\path\to\your\project"
    call venv\Scripts\activate.bat
    python main.py
    deactivate

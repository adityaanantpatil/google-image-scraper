# 🖼️ Google Image Scraper

An automated Selenium-based tool for downloading images from Google Images search results.

## ⚠️ Legal Disclaimer

**IMPORTANT: READ BEFORE USE**

This tool performs automated scraping of Google Images, which may violate:
- 🚫 Google's Terms of Service
- ⚖️ Copyright laws and intellectual property rights
- 🤖 Website access policies and robots.txt guidelines

**Use at your own risk.** The authors are not responsible for any legal consequences arising from the use of this tool. Consider the following:

- **©️ Copyright**: Downloaded images may be copyrighted. Using them without permission may be illegal.
- **📜 Terms of Service**: Automated scraping violates Google's ToS.
- **🚦 Rate Limiting**: Excessive requests may result in IP bans.
- **⚡ Legal Action**: Google and content owners may pursue legal action against violators.

**✅ Recommended alternatives:**
- Use official APIs (e.g., Google Custom Search API, Unsplash API, Pexels API)
- Download images manually with proper attribution
- Use datasets with appropriate licenses

🎓 This tool is provided for educational purposes only.

---

## 📁 Project Structure

```
project-root/
│   automated_scraper.py
│   README.md
│
└───chromedriver-win64/
        chromedriver.exe
        LICENSE.chromedriver
        THIRD_PARTY_NOTICES.chromedriver
```

## ✨ Features

- 📜 Automated scrolling to load more images
- 💾 Downloads up to 1000 images (configurable)
- 🔢 Maintains download order with sequential naming
- ⏭️ Skips duplicate downloads
- 🎯 Handles multiple CSS selectors for reliability
- 📊 Progress tracking during download

## 📋 Requirements

### 🐍 Python Dependencies
```bash
pip install selenium requests pillow
```

### 💻 System Requirements
- Python 3.7+
- Chrome browser installed
- ChromeDriver (included in `chromedriver-win64/`)

## 🚀 Installation

1. Clone or download this repository
2. Install required Python packages:
   ```bash
   pip install selenium requests pillow
   ```
3. Ensure ChromeDriver path matches your setup in the script

## ⚙️ Configuration

Edit the following variables in `automated_scraper.py`:

```python
# Path to ChromeDriver
DRIVER_PATH = r'./chromedriver-win64/chromedriver.exe'

# Download destination folder
folder = r'./downloads'

# In the main execution block:
gs = GoogleScraper(wd, 1000)  # Maximum number of images
gs.scrape_images('your search query here', folder)  # Search query
```

## 🎮 Usage

1. Update the configuration paths and search query
2. Run the script:
   ```bash
   python automated_scraper.py
   ```
3. Images will be downloaded to `<folder>/<query_name>/`

### 📂 Example Output Structure
```
./downloads/your_search_query_here/
    image_0001.jpg
    image_0002.jpg
    image_0003.jpg
    ...
```

## 🔧 How It Works

1. **🔍 Query Construction**: Builds Google Images search URL
2. **📜 Page Scrolling**: Automatically scrolls to load more images
3. **🎯 Element Detection**: Finds image elements using multiple CSS selectors
4. **🔗 URL Extraction**: Extracts image URLs from thumbnails and preview panels
5. **⬇️ Download**: Downloads images with proper headers and saves as JPEGs
6. **📝 Sequential Naming**: Names files `image_0001.jpg`, `image_0002.jpg`, etc.

## 🎛️ Key Parameters

- `max_num_of_images`: Maximum images to download (default: 1000)
- `quality`: JPEG quality setting (default: 85)
- `timeout`: Request timeout in seconds (default: 15)

## 🔧 Troubleshooting

### ❗ Common Issues

**🌐 Browser doesn't open:**
- Verify ChromeDriver path is correct
- Ensure Chrome browser is installed
- Check ChromeDriver version matches Chrome version

**📭 No images downloaded:**
- Google may have changed their HTML structure
- Try reducing `max_num_of_images`
- Check your internet connection
- Your IP may be temporarily blocked

**💥 Script crashes:**
- Increase `time.sleep()` delays
- Reduce scroll speed
- Check for Chrome updates

## 📝 Notes

- 🖼️ Images are saved as JPEG format with 85% quality
- ⏭️ Duplicate files are automatically skipped
- 📊 Progress is printed to console during execution
- 🔒 Browser window closes automatically when complete

## 🤔 Ethical Considerations

Before using this tool, ask yourself:
- ✅ Do I have the right to use these images?
- 📜 Is there a legal way to obtain what I need?
- 🤝 Am I respecting the website's terms and bandwidth?
- 💔 Could this harm content creators?

**Always respect copyright and use images legally.**

## 📄 License

This project is provided as-is for educational purposes only. Users assume all responsibility for their use of this tool.

---

**⚡ Remember: Just because you can automate something doesn't mean you should. Use responsibly.**
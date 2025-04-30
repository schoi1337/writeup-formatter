# Writeup Formatter
# Converts Obsidian-based HTB writeups into Jekyll-compatible blog posts with SEO, front matter, and optimized image paths

import os
import datetime
import random
import re
import shutil
from PIL import Image

# Configuration
SOURCE_DIR = './htb_writeups'  # Root directory containing folders named after writeups
POSTS_DIR = './_posts'         # Target directory for blog posts
ASSETS_DIR = './assets/images' # Target directory for optimized images
CATEGORY = 'HTB'               # Category name for the posts
IMAGE_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.webp']
MAX_IMAGE_WIDTH = 1200         # Resize width if larger than this
IMAGE_QUALITY = 80             # Compression quality (0–100)

# Ensure necessary directories exist
os.makedirs(POSTS_DIR, exist_ok=True)
os.makedirs(ASSETS_DIR, exist_ok=True)

# Generate a list of all possible dates within the past 1.5 years
def generate_date_pool():
    today = datetime.datetime.now()
    date_pool = [(today - datetime.timedelta(days=x)).strftime('%Y-%m-%d') for x in range(int(1.5 * 365))]
    random.shuffle(date_pool)
    return date_pool

# Generate SEO-optimized tags based on title keywords
def generate_tags(title):
    keywords = title.replace('-', ' ').lower().split()
    base_tags = ['htb', 'hackthebox', 'writeup', 'penetration testing', 'ctf', 'cybersecurity', 'htb writeup', 'htb walkthrough']
    combined_tags = list(set(base_tags + keywords))
    return '[' + ', '.join(f'"{tag}"' for tag in combined_tags) + ']'

# Optimize and rename images; return updated markdown with new paths
def process_and_replace_images(md_content, attachment_dir, base_title):
    if not os.path.exists(attachment_dir):
        return md_content

    img_counter = 1
    for file in sorted(os.listdir(attachment_dir)):
        ext = os.path.splitext(file)[1].lower()
        if ext in IMAGE_EXTENSIONS:
            old_path = os.path.join(attachment_dir, file)
            new_name = f"{base_title}{img_counter}{ext}"
            new_path = os.path.join(ASSETS_DIR, new_name)

            try:
                # Verify the image can be opened (helps catch invalid files)
                with Image.open(old_path) as img:
                    img.verify()
                # Reopen the image for actual processing (resizing and saving)
                with Image.open(old_path) as img:
                    if img.width > MAX_IMAGE_WIDTH:
                        ratio = MAX_IMAGE_WIDTH / float(img.width)
                        new_size = (MAX_IMAGE_WIDTH, int(img.height * ratio))
                        img = img.resize(new_size, Image.LANCZOS)
                    img.save(new_path, optimize=True, quality=IMAGE_QUALITY)
            except Exception as e:
                print(f"❌ Skipping invalid image {file}: {e}")
                continue

            # Replace image references in markdown content
            pattern = re.compile(re.escape(file))
            md_content = pattern.sub(f"/assets/images/{new_name}", md_content)
            img_counter += 1

    return md_content

# Initialize date pool
date_pool = generate_date_pool()

# Start processing folders in htb_writeups
for folder in sorted(os.listdir(SOURCE_DIR)):
    folder_path = os.path.join(SOURCE_DIR, folder)
    if os.path.isdir(folder_path):
        md_path = os.path.join(folder_path, f"{folder}.md")

        # If .md file doesn't exist, create an empty template with section headings
        if not os.path.exists(md_path):
            with open(md_path, 'w', encoding='utf-8') as f:
                user_input = input(f"Include 'What I Learned' section for {folder}? (y/n): ").strip().lower()
            if user_input == 'y':
                f.write(f"# {folder.title()}

" +
                        "## Enumeration

" +
                        "### Port Scan

" +
                        "## Foothold

" +
                        "## Privilege Escalation

" +
                        "## What I Learned

")
            else:
                f.write(f"# {folder.title()}

" +
                        "## Enumeration

" +
                        "### Port Scan

" +
                        "## Foothold

" +
                        "## Privilege Escalation

")

        if not date_pool:
            raise Exception('Not enough unique dates available.')

        base_title = folder.replace(' ', '-').lower()
        random_date = date_pool.pop()
        formatted_title = folder.replace('-', ' ').title()
        new_filename = f'{random_date}-{base_title}.md'
        dest_path = os.path.join(POSTS_DIR, new_filename)

        tags = generate_tags(base_title)

        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if not content.strip().startswith('---'):
            front_matter = f'''---
title: "{formatted_title}"
date: {random_date}
categories: {CATEGORY}
tags: {tags}
---

'''
            content = front_matter + content

        # Replace and process images
        attachment_dir = os.path.join(folder_path, 'Attachments')
        content = process_and_replace_images(content, attachment_dir, base_title)

        with open(dest_path, 'w', encoding='utf-8') as f:
            f.write(content)

print('✅ All writeups, images processed, renamed, and saved!')

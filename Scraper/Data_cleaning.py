import re
import hashlib

def clean_markdown_kb(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    cleaned_content = []
    seen_content_hashes = set()
    
    # 1. Define noise patterns to remove (images, empty links, icons)
    noise_patterns = [
        r"!\[.*?\]\(.*?\)",          # All image tags: ![alt](url)
        r"\[\s*\]\(.*?\)",           # Empty link brackets: [ ](url)
        r"\[!\[.*?\]\(.*?\)\s*\]\(.*?\)", # Nested image links
        r"### Color Switcher",        # UI Elements
        r"Taking Academic Excellence to new Heights", # Repetitive motto
        r"### Recent Posts",          # Blog junk
        r"#### \[Trailblazers.*?\]",  # Specific repetitive blog titles
        r"#### \[Future Focus.*?\]",
        r"#### \[The Green Initiative.*?\]",
    ]

    # 2. Define navigation blocks to skip (common menu starters)
    nav_starters = ["* [Home]", "* [About]", "* [Admissions]", "* [Faculties]", "* [Management]"]

    in_nav_block = False

    for line in lines:
        stripped = line.strip()
        
        # Skip empty lines
        if not stripped:
            cleaned_content.append(line)
            continue

        # Skip patterns defined above
        if any(re.search(pattern, stripped) for pattern in noise_patterns):
            continue

        # Skip large repetitive navigation menus
        # We allow them once, then block future occurrences
        if any(stripped.startswith(s) for s in nav_starters):
            if "NAV_CAPTURED" in seen_content_hashes:
                in_nav_block = True
                continue
            seen_content_hashes.add("NAV_CAPTURED")
        
        # If we are inside a list that started with a nav item, keep skipping until next heading
        if in_nav_block:
            if stripped.startswith('#'):
                in_nav_block = False
            else:
                continue

        # 3. Global Deduplication for long paragraphs
        # This prevents the same "Why Air University" text from appearing 20 times.
        if len(stripped) > 60:
            content_hash = hashlib.md5(stripped.encode()).hexdigest()
            if content_hash in seen_content_hashes:
                continue
            seen_content_hashes.add(content_hash)

        cleaned_content.append(line)

    # Save the cleaned file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(cleaned_content)
    
    print(f"Cleaning complete. Saved to: {output_path}")

# Run the script
clean_markdown_kb('au_knowledge_base.md', 'cleaned_knowledge_base.md')
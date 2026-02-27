import os

def merge_scraped_data(input_folder="data/air_university_data", output_file="au_knowledge_base.md"):
    all_files = [f for f in os.listdir(input_folder) if f.endswith('.md')]
    # Sort files numerically (page_1, page_2...)
    all_files.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))

    print(f"Merging {len(all_files)} files...")

    with open(output_file, "w", encoding="utf-8") as outfile:
        for filename in all_files:
            file_path = os.path.join(input_folder, filename)
            with open(file_path, "r", encoding="utf-8") as infile:
                content = infile.read()
                # Clean up repeated headers or noise if necessary
                outfile.write(content)
                outfile.write("\n\n---\n\n") # Separator between pages

    print(f"Success! All data merged into: {output_file}")

if __name__ == "__main__":
    merge_scraped_data()
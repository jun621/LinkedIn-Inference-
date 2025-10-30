import os
import zipfile
from docx import Document
import shutil
import csv

class ResumeExtractor:
    def __init__(self, zip_path, output_dir="extracted_resumes"):
        self.zip_path = zip_path
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    # extract text from each paragrpah within each resume
    def extract_text_from_docx(self, docx_path):
        """Extract text from DOCX file"""
        text = ""
        try:
            doc = Document(docx_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            print(f"Error reading DOCX {docx_path}: {e}")
        return text
    
    def process_zip(self):
        """Extract all text from resumes in zip file and save to CSV"""
        temp_dir = "temp_extracted"
        os.makedirs(temp_dir, exist_ok=True)
        
        # Extract zip file
        print(f"Extracting {self.zip_path}...")
        with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        
        # Process each file and store data
        resume_data = []
        file_count = 0
        
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                # Skip Mac system files
                if file.startswith('._') or file == '.DS_Store':
                    continue
                    
                file_path = os.path.join(root, file)
                file_ext = os.path.splitext(file)[1].lower()
                
                text = ""
               
                if file_ext == '.docx':
                    print(f"Processing DOCX: {file}")
                    text = self.extract_text_from_docx(file_path)
                else:
                    continue
                
                if text:
                    file_count += 1
                    resume_data.append({
                        'resume_id': file_count,
                        'filename': file,
                        'file_type': file_ext[1:],
                        'text': text.strip()
                    })
        
        # Save as CSV only
        csv_file = os.path.join(self.output_dir, "all_resumes.csv")
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['resume_id', 'filename', 'file_type', 'text'])
            writer.writeheader()
            writer.writerows(resume_data)
        
        # Cleanup temp directory
        shutil.rmtree(temp_dir)
        
        print(f"\n{'='*80}")
        print(f"Extraction complete!")
        print(f"Processed {file_count} resume(s)")
        print(f"CSV file saved to: {csv_file}")
        print(f"{'='*80}")
        
        return resume_data


if __name__ == "__main__":
    zip_file_path = "/home/jkoizum1/Qualtrics_resumes-2.zip"
    
    extractor = ResumeExtractor(zip_file_path, output_dir="extracted_resumes")
    data = extractor.process_zip()
    
    # Display summary
    print(f"\nTotal resumes processed: {len(data)}")
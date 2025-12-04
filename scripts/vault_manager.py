#!/usr/bin/env python3
import os
import csv
import hashlib
import json
import shutil
from datetime import datetime
from pathlib import Path

class VaultManager:
    """Manages video vault: ingests, deduplicates, and tracks Minecraft parkour videos"""
    
    def __init__(self, base_path="D:\\mc_parkour_factory"):
        self.base_path = Path(base_path)
        self.vault_csv = self.base_path / "logs" / "vault.csv"
        self.incoming_dir = self.base_path / "incoming"
        self.vault_dir = self.base_path / "vault"
        self.today = datetime.now()
        self.today_folder = self.vault_dir / self.today.strftime("%Y-%m-%d")
        
        # Create directories
        os.makedirs(self.today_folder / "raw", exist_ok=True)
        os.makedirs(self.base_path / "logs", exist_ok=True)
        
        self.vault_data = self._load_vault_csv()
    
    def _get_file_hash(self, file_path):
        """Compute MD5 hash for deduplication"""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def _load_vault_csv(self):
        """Load existing vault CSV or create new"""
        if self.vault_csv.exists():
            data = {}
            with open(self.vault_csv, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data[row['file_hash']] = row
            return data
        return {}
    
    def _save_vault_csv(self):
        """Save vault data to CSV"""
        with open(self.vault_csv, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['file_hash', 'file_path', 'date_added', 'file_size_mb']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for hash_val, row in self.vault_data.items():
                writer.writerow(row)
    
    def process_incoming_videos(self):
        """Move videos from incoming to vault"""
        incoming_files = list(self.incoming_dir.glob("*.mp4"))
        
        if not incoming_files:
            print("No videos in incoming folder")
            return []
        
        processed = []
        for file_path in incoming_files:
            file_hash = self._get_file_hash(file_path)
            
            if file_hash in self.vault_data:
                print(f"SKIP: Duplicate - {file_path.name}")
                continue
            
            dest_path = self.today_folder / "raw" / file_path.name
            shutil.move(str(file_path), str(dest_path))
            file_size_mb = os.path.getsize(dest_path) / (1024 * 1024)
            
            self.vault_data[file_hash] = {
                'file_hash': file_hash,
                'file_path': str(dest_path),
                'date_added': self.today.strftime("%Y-%m-%d %H:%M:%S"),
                'file_size_mb': f"{file_size_mb:.2f}"
            }
            
            processed.append(str(dest_path))
            print(f"OK: {file_path.name}")
        
        self._save_vault_csv()
        return processed
    
    def get_available_videos(self, num_needed=50):
        """Get videos available for posting"""
        available = []
        for file_hash, entry in self.vault_data.items():
            if entry['file_path'] and Path(entry['file_path']).exists():
                available.append((file_hash, entry))
        
        print(f"\n[VAULT STATUS]")
        print(f"Total: {len(self.vault_data)} | Available: {len(available)} | Needed: {num_needed}")
        return available[:num_needed]

if __name__ == "__main__":
    vm = VaultManager()
    processed = vm.process_incoming_videos()
    available = vm.get_available_videos(50)
    print(f"\nProcessed: {len(processed)} videos")
    print(f"Available for rotation: {len(available)} videos")

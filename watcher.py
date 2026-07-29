import os
import subprocess
import time
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_file:
            # Watch all these file types
            watch_files = [
                'events.json',
                'quotes.json',
                'registrations.json',
                'settings.json',
                'admin_users.json'
            ]
            
            # Check if it's a file we care about
            file_name = event.src_path.split('/')[-1]
            
            if file_name in watch_files:
                print(f"\n📁 {datetime.now().strftime('%H:%M:%S')} - Change detected!")
                print(f"   📄 File: {file_name}")
                self.push_changes()
            
            # Check if it's an image
            if 'static/images/events/' in event.src_path or 'static/images/gallery/' in event.src_path:
                if file_name.endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                    print(f"\n📁 {datetime.now().strftime('%H:%M:%S')} - Image uploaded!")
                    print(f"   🖼️  File: {file_name}")
                    self.push_changes()
    
    def on_created(self, event):
        if event.is_file:
            file_name = event.src_path.split('/')[-1]
            
            # New event or image created
            if 'events.json' in event.src_path or file_name.endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                print(f"\n📁 {datetime.now().strftime('%H:%M:%S')} - New file created!")
                print(f"   📄 File: {file_name}")
                self.push_changes()
    
    def push_changes(self):
        print("   ⏳ Pushing to Render...")
        
        # Add all changes
        subprocess.run(['git', 'add', '.'], check=False, capture_output=True)
        
        # Check if there are changes to commit
        result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
        
        if result.stdout.strip():
            # Commit with timestamp
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            subprocess.run(['git', 'commit', '-m', f'Auto-update: {timestamp}'], check=False)
            
            # Push to Render
            push_result = subprocess.run(['git', 'push', 'origin', 'main'], check=False)
            
            if push_result.returncode == 0:
                print("   ✅ Changes pushed to Render!")
                print(f"   🕐 Time: {timestamp}")
            else:
                print("   ❌ Push failed! Check your internet connection.")
        else:
            print("   ℹ️  No changes to commit")
        
        print("-" * 60)

# Main watcher
def run_watcher():
    print("=" * 60)
    print("   🚀 WORD TEMPLE - AUTO-PUSHER")
    print("=" * 60)
    print("\n📁 Watching for changes:")
    print("   📄 data/events.json - New/Updated events")
    print("   📄 data/quotes.json - New/Updated quotes")
    print("   📄 data/registrations.json - New registrations")
    print("   📄 data/settings.json - Settings changes")
    print("   🖼️  static/images/events/ - New event images")
    print("   🖼️  static/images/gallery/ - New gallery images")
    print("\n⚡ Any change will auto-push to Render!")
    print("🔄 Press Ctrl+C to stop\n")
    
    observer = Observer()
    observer.schedule(ChangeHandler(), path='data/', recursive=False)
    observer.schedule(ChangeHandler(), path='static/images/events/', recursive=False)
    observer.schedule(ChangeHandler(), path='static/images/gallery/', recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n👋 Auto-pusher stopped.")
        print("   To restart: python watcher.py")
    observer.join()

if __name__ == "__main__":
    run_watcher()

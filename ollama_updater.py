#!/usr/bin/env python3
"""
Ollama Updater Pro - Self-Installing GUI
Auto-installs tkinter if missing!
"""

import subprocess
import os
import sys
import threading
import tempfile
import time

# Auto-install tkinter if missing
def install_tkinter():
    """Automatically install tkinter if not present"""
    try:
        import tkinter
        return True
    except ImportError:
        print("\n" + "="*60)
        print("📦 Tkinter not found - Installing automatically...")
        print("="*60)
        
        # Detect package manager and install
        try:
            # Try apt (Debian/Ubuntu)
            subprocess.run(['sudo', 'apt', 'update'], check=True, capture_output=True)
            subprocess.run(['sudo', 'apt', 'install', '-y', 'python3-tk'], check=True, capture_output=True)
            print("✅ Tkinter installed successfully!")
            print("🔄 Restarting script...\n")
            return True
        except:
            print("❌ Failed to install tkinter automatically")
            print("\nPlease install manually with:")
            print("  sudo apt install python3-tk")
            print("\nThen run this script again.")
            return False

# Install tkinter if needed
if not install_tkinter():
    sys.exit(1)

# Now import tkinter
import tkinter as tk
from tkinter import ttk, scrolledtext, simpledialog, messagebox

class OllamaUpdaterLite:
    def __init__(self, root):
        self.root = root
        root.title("Ollama Updater 🦙")
        root.geometry("800x600")
        root.configure(bg='#1a1a2e')
        self.sudo_password = None
        
        self.setup_ui()
        self.refresh_status()
    
    def setup_ui(self):
        # Header
        title = tk.Label(self.root, text="🦙 Ollama Updater Pro", 
                        font=('Arial', 24, 'bold'), 
                        bg='#1a1a2e', fg='#e94560')
        title.pack(pady=20)
        
        # Status frame
        status_frame = tk.Frame(self.root, bg='#16213e', relief=tk.RAISED, bd=2)
        status_frame.pack(padx=20, pady=10, fill=tk.X)
        
        self.version_label = tk.Label(status_frame, text="Current Version: Checking...", 
                                     bg='#16213e', fg='#00ff9d', font=('Arial', 11))
        self.version_label.pack(pady=5)
        
        self.host_label = tk.Label(status_frame, text="Network Config: Checking...", 
                                  bg='#16213e', fg='#ffd700', font=('Arial', 11))
        self.host_label.pack(pady=5)
        
        # Buttons frame
        btn_frame = tk.Frame(self.root, bg='#1a1a2e')
        btn_frame.pack(pady=20)
        
        self.update_btn = tk.Button(btn_frame, text="🚀 UPDATE & CONFIGURE", 
                                   command=self.ask_password_and_update,
                                   bg='#0f3460', fg='white', 
                                   font=('Arial', 12, 'bold'),
                                   padx=20, pady=10,
                                   activebackground='#e94560',
                                   activeforeground='white',
                                   cursor='hand2')
        self.update_btn.pack(side=tk.LEFT, padx=10)
        
        self.config_btn = tk.Button(btn_frame, text="⚙️ CONFIGURE ONLY", 
                                   command=self.ask_password_and_configure,
                                   bg='#0f3460', fg='white',
                                   font=('Arial', 12, 'bold'),
                                   padx=20, pady=10,
                                   activebackground='#e94560',
                                   activeforeground='white',
                                   cursor='hand2')
        self.config_btn.pack(side=tk.LEFT, padx=10)
        
        # Progress bar
        self.progress = ttk.Progressbar(self.root, mode='indeterminate', length=400)
        self.progress.pack(pady=10)
        self.progress.pack_forget()
        
        # Console output
        console_label = tk.Label(self.root, text="📋 Live Console Output:", 
                                bg='#1a1a2e', fg='white', 
                                font=('Arial', 10, 'bold'))
        console_label.pack(anchor=tk.W, padx=20, pady=(10,0))
        
        self.console = scrolledtext.ScrolledText(self.root, 
                                                 bg='#0f0f1a', 
                                                 fg='#00ff9d',
                                                 font=('Monaco', 10),
                                                 height=20,
                                                 relief=tk.FLAT)
        self.console.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
    
    def log(self, message, is_error=False):
        """Add message to console"""
        self.console.insert(tk.END, f'{message}\n')
        line_count = int(self.console.index('end-1c').split('.')[0])
        if is_error:
            self.console.tag_add('error', f"{line_count}.0", f"{line_count}.end")
            self.console.tag_config('error', foreground='#ff6b6b')
        else:
            self.console.tag_add('normal', f"{line_count}.0", f"{line_count}.end")
            self.console.tag_config('normal', foreground='#00ff9d')
        self.console.see(tk.END)
        self.root.update()
    
    def ask_password(self):
        """Ask for sudo password in GUI dialog"""
        password = simpledialog.askstring("Sudo Password Required", 
                                         "🔐 Enter your sudo password to configure Ollama:\n\n(This is required to edit system files)",
                                         parent=self.root,
                                         show='*')
        if password:
            # Test if password is correct
            test_cmd = f"echo '{password}' | sudo -S echo 'Password OK' 2>/dev/null"
            result = subprocess.run(test_cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                self.sudo_password = password
                return True
            else:
                messagebox.showerror("Authentication Failed", 
                                    "❌ Incorrect password! Please try again.")
                return self.ask_password()
        return False
    
    def refresh_status(self):
        """Check current Ollama status"""
        def check():
            # Check version
            try:
                result = subprocess.run(['ollama', '--version'], 
                                      capture_output=True, text=True, timeout=2)
                if result.returncode == 0:
                    self.version_label.config(text=f"✓ Current Version: {result.stdout.strip()}", 
                                             fg='#00ff9d')
                else:
                    self.version_label.config(text="⚠️ Ollama not installed", fg='#ffd700')
            except FileNotFoundError:
                self.version_label.config(text="⚠️ Ollama not installed", fg='#ffd700')
            except:
                self.version_label.config(text="❌ Ollama not found", fg='#ff6b6b')
            
            # Check network config
            try:
                with open('/etc/systemd/system/ollama.service', 'r') as f:
                    content = f.read()
                    if 'OLLAMA_HOST=0.0.0.0' in content:
                        self.host_label.config(text="✓ Network: Configured for 0.0.0.0", fg='#00ff9d')
                    else:
                        self.host_label.config(text="⚠️ Network: Not configured (localhost only)", fg='#ffd700')
            except FileNotFoundError:
                self.host_label.config(text="⚠️ Ollama service not installed yet", fg='#ffd700')
            except:
                self.host_label.config(text="⚠️ Cannot check config", fg='#ffd700')
        
        threading.Thread(target=check, daemon=True).start()
    
    def configure_service(self):
        """Configure Ollama service - works even if freshly installed"""
        self.log("\n🔧 Configuring Ollama service...")
        
        # Check if service file exists, if not, Ollama will create it during install
        check_file_cmd = f"echo '{self.sudo_password}' | sudo -S test -f /etc/systemd/system/ollama.service && echo 'exists' || echo 'missing'"
        result = subprocess.run(check_file_cmd, shell=True, capture_output=True, text=True)
        
        if 'missing' in result.stdout:
            self.log("⚠️ Service file not found yet. It will be created when Ollama installs.", True)
            self.log("   Please run UPDATE & CONFIGURE first to install Ollama.", True)
            return False
        
        # Read the service file
        read_cmd = f"echo '{self.sudo_password}' | sudo -S cat /etc/systemd/system/ollama.service"
        result = subprocess.run(read_cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            self.log("❌ Failed to read service file", True)
            return False
        
        content = result.stdout
        
        # Check if already configured
        if 'Environment="OLLAMA_HOST=0.0.0.0"' in content:
            self.log("✓ Already configured for 0.0.0.0!", True)
            return True
        
        # Add the environment variable
        lines = content.split('\n')
        new_lines = []
        inserted = False
        
        for line in lines:
            new_lines.append(line)
            if line.strip() == '[Service]' and not inserted:
                new_lines.append('Environment="OLLAMA_HOST=0.0.0.0"')
                inserted = True
        
        if not inserted:
            self.log("❌ Could not find [Service] section", True)
            return False
        
        # Write back using temp file
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
            tmp.write('\n'.join(new_lines))
            temp_file = tmp.name
        
        # Copy temp file to destination
        copy_cmd = f"echo '{self.sudo_password}' | sudo -S cp {temp_file} /etc/systemd/system/ollama.service"
        result = subprocess.run(copy_cmd, shell=True, capture_output=True, text=True)
        
        # Clean up
        os.unlink(temp_file)
        
        if result.returncode != 0:
            self.log("❌ Failed to write service file", True)
            return False
        
        self.log("✓ Added OLLAMA_HOST to service file")
        
        # Restart service (only if it's running)
        subprocess.run(f"echo '{self.sudo_password}' | sudo -S systemctl daemon-reload", shell=True)
        subprocess.run(f"echo '{self.sudo_password}' | sudo -S systemctl restart ollama", shell=True)
        
        self.log("✅ Service configured successfully!")
        return True
    
    def update_ollama(self):
        """Update/Install Ollama - works on fresh installs too"""
        self.log("\n🔄 Starting Ollama installation/update...")
        
        # Download the install script
        self.log("  Downloading install script...")
        download_result = subprocess.run("curl -fsSL https://ollama.com/install.sh -o /tmp/ollama_install.sh", 
                                        shell=True, capture_output=True)
        
        if download_result.returncode != 0:
            self.log("❌ Failed to download install script", True)
            return False
        
        # Run the script with sudo
        self.log("  Running installer (this may take a minute)...")
        cmd = f"echo '{self.sudo_password}' | sudo -S bash /tmp/ollama_install.sh"
        
        process = subprocess.Popen(cmd, shell=True,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT,
                                  text=True, bufsize=1)
        
        for line in process.stdout:
            line = line.strip()
            if line and 'Password:' not in line and '[sudo]' not in line:
                self.log(f"  {line}")
        
        process.wait()
        
        # Clean up temp file (only if it exists)
        if os.path.exists('/tmp/ollama_install.sh'):
            subprocess.run(f"echo '{self.sudo_password}' | sudo -S rm /tmp/ollama_install.sh", shell=True)
        
        if process.returncode == 0:
            self.log("✓ Ollama installed/updated successfully!")
            return True
        else:
            self.log(f"❌ Installation failed with exit code {process.returncode}", True)
            return False
    
    def ask_password_and_update(self):
        if self.ask_password():
            self.run_full_update()
        else:
            messagebox.showwarning("Cancelled", "Operation cancelled")
    
    def ask_password_and_configure(self):
        if self.ask_password():
            self.configure_only()
        else:
            messagebox.showwarning("Cancelled", "Operation cancelled")
    
    def run_full_update(self):
        self.update_btn.config(state=tk.DISABLED)
        self.config_btn.config(state=tk.DISABLED)
        self.progress.pack()
        self.progress.start(10)
        self.console.delete(1.0, tk.END)
        
        def update_thread():
            try:
                # Step 1: Install/Update Ollama
                update_ok = self.update_ollama()
                
                # Step 2: Configure (if update succeeded OR if Ollama was already installed)
                config_ok = False
                if update_ok:
                    # Wait a moment for service file to be created
                    self.log("  Waiting for service file to be created...")
                    time.sleep(2)
                    config_ok = self.configure_service()
                else:
                    # Try to configure anyway in case Ollama was already installed
                    self.log("  Attempting to configure existing Ollama installation...")
                    config_ok = self.configure_service()
                
                self.progress.stop()
                self.progress.pack_forget()
                
                # Honest results
                if update_ok and config_ok:
                    self.log("\n🎉 SUCCESS! Ollama installed/updated AND configured!")
                    self.log("🌐 Server accessible at 0.0.0.0:11434")
                    messagebox.showinfo("Success", "Ollama installed/updated and configured successfully!")
                elif update_ok and not config_ok:
                    self.log("\n⚠️ Ollama installed but configuration FAILED!", True)
                    messagebox.showwarning("Partial Success", "Ollama installed but network configuration failed. You may need to configure manually.")
                elif not update_ok and config_ok:
                    self.log("\n⚠️ Configuration applied to existing Ollama installation!")
                    messagebox.showinfo("Success", "Ollama configuration updated successfully!")
                else:
                    self.log("\n❌ INSTALLATION FAILED! Please check errors above.", True)
                    messagebox.showerror("Installation Failed", "Ollama installation failed. Check the console for details.")
                
                self.refresh_status()
                self.sudo_password = None
                
            except Exception as e:
                self.log(f"❌ Error: {str(e)}", True)
                self.progress.stop()
                self.progress.pack_forget()
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
            finally:
                self.update_btn.config(state=tk.NORMAL)
                self.config_btn.config(state=tk.NORMAL)
        
        threading.Thread(target=update_thread, daemon=True).start()
    
    def configure_only(self):
        self.update_btn.config(state=tk.DISABLED)
        self.config_btn.config(state=tk.DISABLED)
        self.console.delete(1.0, tk.END)
        
        def config_thread():
            self.log("⚙️ Running configuration only...")
            success = self.configure_service()
            self.refresh_status()
            
            if success:
                self.log("\n✅ Configuration completed successfully!")
                messagebox.showinfo("Success", "Ollama network configuration completed!")
            else:
                self.log("\n❌ Configuration failed!", True)
                self.log("   Make sure Ollama is installed first (run UPDATE & CONFIGURE)", True)
                messagebox.showerror("Configuration Failed", "Failed to configure Ollama. Make sure Ollama is installed first.")
            
            self.sudo_password = None
            self.update_btn.config(state=tk.NORMAL)
            self.config_btn.config(state=tk.NORMAL)
        
        threading.Thread(target=config_thread, daemon=True).start()

if __name__ == '__main__':
    # Small delay to show any install messages
    time.sleep(0.5)
    
    root = tk.Tk()
    root.title("Ollama Updater Pro 🦙")
    root.geometry("800x600")
    root.configure(bg='#1a1a2e')
    app = OllamaUpdaterLite(root)
    root.mainloop()

"""
Main entry point for the Gest application.
Initializes all components and launches the GUI interface.
"""

import sys
import os
from pathlib import Path

# Add src to path for imports
current_dir = Path(__file__).parent
src_dir = current_dir
sys.path.insert(0, str(src_dir))

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from typing import Optional

# Import Gest modules
from config.settings import get_config_manager
from core.camera_manager import get_camera_manager
from core.detection_engine import get_detection_engine
from core.feature_processor import get_feature_processor
from core.gesture_classifier import get_gesture_classifier
from core.action_executor import get_action_executor
from gui.gesture_trainer import GestureTrainerGUI
from utils.logger import setup_logger, get_logger
from utils.error_handler import handle_exceptions

class GestApplication:
    """
    Main application class for Gest gesture recognition system.
    """
    
    def __init__(self):
        """Initialize the Gest application."""
        # Setup logging first
        self.logger = setup_logger()
        self.logger.info("Starting Gest Application...")
        
        # Load configuration
        try:
            self.config_manager = get_config_manager()
            self.settings = self.config_manager.load_settings()
            self.logger.info("Configuration loaded successfully")
        except Exception as e:
            self.logger.error(f"Failed to load configuration: {e}")
            sys.exit(1)
        
        # Initialize core components
        self.camera_manager = get_camera_manager()
        self.detection_engine = get_detection_engine()
        self.feature_processor = get_feature_processor()
        self.gesture_classifier = get_gesture_classifier()
        self.action_executor = get_action_executor()
        
        # GUI components
        self.root = None
        self.main_gui = None
        self.trainer_window = None
        
        self.logger.info("Gest application initialized successfully")
    
    @handle_exceptions
    def initialize_camera(self) -> bool:
        """
        Initialize camera system.
        
        Returns:
            True if camera initialized successfully, False otherwise
        """
        try:
            self.logger.info("Initializing camera system...")
            success = self.camera_manager.initialize_camera()
            
            if success:
                camera_info = self.camera_manager.get_camera_info()
                self.logger.info(f"Camera initialized: {camera_info}")
            else:
                self.logger.error("Failed to initialize camera")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Camera initialization error: {e}")
            return False
    
    def create_main_window(self) -> None:
        """Create and configure the main application window."""
        self.root = tk.Tk()
        
        # Configure window
        gui_config = self.settings.get("gui", {})
        window_title = gui_config.get("window_title", "Gest - Gesture Recognition")
        window_size = gui_config.get("window_size", [1200, 800])
        
        self.root.title(window_title)
        self.root.geometry(f"{window_size[0]}x{window_size[1]}")
        self.root.configure(bg='#f0f0f0')
        
        # Configure styles
        self.configure_styles()
        
        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.logger.info(f"Main window created: {window_title}")
    
    def configure_styles(self) -> None:
        """Configure ttk styles for the application."""
        style = ttk.Style()
        
        # Configure accent button style
        style.configure(
            'Accent.TButton',
            background='#007ACC',
            foreground='white',
            font=('Arial', 10, 'bold')
        )
    
    def show_startup_dialog(self) -> str:
        """
        Show startup dialog to choose application mode.
        
        Returns:
            Selected mode: 'main', 'trainer', or 'exit'
        """
        dialog = tk.Toplevel()
        dialog.title("Gest - Choose Mode")
        dialog.geometry("400x300")
        dialog.configure(bg='#f0f0f0')
        dialog.transient(self.root)
        dialog.grab_set()
        
        result = tk.StringVar(value="exit")
        
        # Title
        title_label = ttk.Label(dialog, text="Welcome to Gest", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=20)
        
        # Mode selection buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=20)
        
        trainer_button = ttk.Button(
            button_frame,
            text="🎓 Training Mode\n(Record & Train Gestures)",
            width=25,
            command=lambda: [result.set("trainer"), dialog.destroy()]
        )
        trainer_button.pack(pady=10)
        
        exit_button = ttk.Button(
            button_frame,
            text="❌ Exit",
            width=25,
            command=lambda: [result.set("exit"), dialog.destroy()]
        )
        exit_button.pack(pady=10)
        
        # Wait for user choice
        dialog.wait_window()
        return result.get()
    
    def run_trainer_mode(self) -> None:
        """Run the gesture trainer application."""
        try:
            self.trainer_gui = GestureTrainerGUI(self.root)
            
            # Hide main window content and show trainer
            for widget in self.root.winfo_children():
                widget.destroy()
            
            self.logger.info("Gesture trainer mode started")
            
        except Exception as e:
            self.logger.error(f"Error running trainer mode: {e}")
            messagebox.showerror("Error", f"Failed to start trainer mode: {e}")
    
    @handle_exceptions
    def run(self) -> None:
        """Run the Gest application."""
        self.logger.info("Starting Gest application...")
        
        # Create main window
        self.create_main_window()
        
        # Show startup dialog
        mode = self.show_startup_dialog()
        
        if mode == "exit":
            self.on_closing()
            return
        elif mode == "trainer":
            self.run_trainer_mode()
        
        # Start main event loop
        self.logger.info("Starting GUI event loop...")
        self.root.mainloop()
    
    def on_closing(self) -> None:
        """Handle application closing."""
        self.logger.info("Closing Gest application...")
        
        # Stop any ongoing operations
        if hasattr(self, 'camera_manager'):
            self.camera_manager.release()
        
        # Release other resources
        if hasattr(self, 'detection_engine'):
            self.detection_engine.release()
        
        # Close GUI
        if self.root:
            self.root.quit()
            self.root.destroy()
        
        self.logger.info("Gest application closed")

def main():
    """Main function."""
    try:
        app = GestApplication()
        app.run()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
    except Exception as e:
        print(f"Application error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("Gest application terminated")

if __name__ == "__main__":
    main()

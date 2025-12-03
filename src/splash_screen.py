"""
NiTriTe V.13 - Splash Screen / Loading Screen
Beautiful loading screen with progress bar for desktop application
Version améliorée avec gestion propre du threading
"""

import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import threading
import time
import sys


class SplashScreen:
    """Splash screen with progress bar and loading messages - Improved version"""

    def __init__(self):
        self._destroyed = False
        self._callback_executed = False
        
        self.root = tk.Tk()
        self.root.withdraw()  # Hide initially

        # Create splash window
        self.splash = tk.Toplevel(self.root)
        self.splash.title("NiTriTe V.13")

        # Window configuration
        width = 500
        height = 400
        screen_width = self.splash.winfo_screenwidth()
        screen_height = self.splash.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.splash.geometry(f"{width}x{height}+{x}+{y}")
        self.splash.overrideredirect(True)  # Remove window decorations
        self.splash.configure(bg='#1a1a1a')
        
        # Toujours au premier plan
        self.splash.lift()
        self.splash.attributes('-topmost', True)

        # Progress tracking (MUST be initialized BEFORE create_ui)
        self.progress_var = tk.DoubleVar()
        self.progress_var.set(0)

        # Create UI
        self.create_ui()

        self.loading_steps = [
            (10, "Initialisation...", "Démarrage de NiTriTe V.13..."),
            (25, "Chargement des ressources...", "Préparation de l'interface..."),
            (40, "Chargement de la base de données...", "Lecture de 715 applications..."),
            (55, "Chargement des catégories...", "Organisation de 25 catégories..."),
            (70, "Chargement des outils système...", "Préparation de 553+ outils..."),
            (85, "Chargement des profils...", "Configuration de 10 profils..."),
            (95, "Finalisation...", "Préparation de l'interface..."),
            (100, "Terminé !", "Lancement de NiTriTe V.13...")
        ]

        self.current_step = 0

    def create_ui(self):
        """Create the splash screen UI"""

        # Main container
        main_frame = ctk.CTkFrame(self.splash, fg_color='#1a1a1a')
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Logo container
        logo_frame = ctk.CTkFrame(main_frame, fg_color='#1a1a1a')
        logo_frame.pack(pady=(20, 30))

        # Logo circle with N
        logo_canvas = tk.Canvas(logo_frame, width=120, height=120, bg='#1a1a1a', highlightthickness=0)
        logo_canvas.pack()

        # Draw circle
        logo_canvas.create_oval(10, 10, 110, 110, outline='#FF6B35', width=3)

        # Draw N
        logo_canvas.create_text(60, 60, text='N', font=('Segoe UI', 48, 'bold'),
                                fill='#FF6B35')

        # Title
        title_label = ctk.CTkLabel(main_frame, text='NiTriTe V.13 Beta',
                               font=('Segoe UI', 28, 'bold'),
                               text_color='#ffffff')
        title_label.pack(pady=(0, 5))

        # Subtitle
        subtitle_label = ctk.CTkLabel(main_frame, text='Gestionnaire d\'Applications et Outils Système',
                                  font=('Segoe UI', 12),
                                  text_color='#b0b0b0')
        subtitle_label.pack(pady=(0, 40))

        # Progress bar frame
        progress_frame = ctk.CTkFrame(main_frame, fg_color='#1a1a1a')
        progress_frame.pack(fill=tk.X, pady=15)

        # Progress bar
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Orange.Horizontal.TProgressbar",
                        troughcolor='#3a3a3a',
                        background='#FF6B35',
                        bordercolor='#3a3a3a',
                        lightcolor='#FF6B35',
                        darkcolor='#FF6B35',
                        thickness=8)

        self.progress_bar = ttk.Progressbar(
            progress_frame,
            style="Orange.Horizontal.TProgressbar",
            mode='determinate',
            maximum=100,
            variable=self.progress_var
        )
        self.progress_bar.pack(fill=tk.X)

        # Loading text
        self.loading_text = ctk.CTkLabel(main_frame, text='Initialisation...',
                                     font=('Segoe UI', 11),
                                     text_color='#e0e0e0')
        self.loading_text.pack(pady=(10, 5))

        # Percentage label
        self.percent_label = ctk.CTkLabel(main_frame, text='0%',
                                      font=('Segoe UI', 20, 'bold'),
                                      text_color='#FF6B35')
        self.percent_label.pack(pady=(5, 20))

        # Status text
        self.status_text = ctk.CTkLabel(main_frame, text='Chargement des ressources...',
                                    font=('Segoe UI', 10, 'italic'),
                                    text_color='#909090')
        self.status_text.pack()

    def update_progress(self, value, text=None, status=None):
        """Update progress bar and text - Thread-safe version"""
        if self._destroyed:
            return
            
        def _update():
            try:
                if self._destroyed:
                    return
                self.progress_var.set(value)
                self.percent_label.configure(text=f'{int(value)}%')

                if text:
                    self.loading_text.configure(text=text)

                if status:
                    self.status_text.configure(text=status)

                self.splash.update_idletasks()
            except tk.TclError:
                # Widget destroyed
                self._destroyed = True
        
        # Si on est dans le thread principal, exécuter directement
        try:
            self.root.after(0, _update)
        except:
            pass

    def run_loading_sequence(self, callback=None):
        """Run the loading sequence - Improved version"""
        self._callback = callback

        def loading_thread():
            for progress, text, status in self.loading_steps:
                if self._destroyed:
                    break
                self.update_progress(progress, text, status)
                # Simulate loading time
                delay = 0.3 if progress == 100 else 0.15 + (0.05 * (progress / 100))
                time.sleep(delay)

            # Wait a bit before closing
            time.sleep(0.3)
            
            # Schedule close and callback on main thread
            if not self._destroyed:
                try:
                    self.root.after(0, self._finish_loading)
                except:
                    pass

        # Start loading in separate thread
        thread = threading.Thread(target=loading_thread, daemon=True)
        thread.start()
    
    def _finish_loading(self):
        """Finish loading sequence and call callback"""
        if self._destroyed or self._callback_executed:
            return
        
        self._callback_executed = True
        
        # Close splash screen
        self.close()
        
        # Destroy root to stop mainloop
        try:
            self.root.quit()
            self.root.destroy()
        except:
            pass
        
        # Call callback if provided
        if self._callback:
            self._callback()

    def show(self):
        """Show the splash screen"""
        if not self._destroyed:
            self.splash.deiconify()
            self.splash.lift()
            self.splash.focus_force()

    def close(self):
        """Close the splash screen"""
        self._destroyed = True
        try:
            self.splash.destroy()
        except:
            pass

    def mainloop(self):
        """Run the main loop"""
        try:
            self.root.mainloop()
        except:
            pass


class LoadingScreen:
    """Simple loading screen manager for integration with main app"""

    @staticmethod
    def show_and_load(load_function):
        """
        Show splash screen and execute load function

        Args:
            load_function: Function to call after loading sequence
        """
        splash = SplashScreen()
        splash.show()

        # Run loading sequence with callback
        splash.run_loading_sequence(callback=load_function)

        # Keep splash visible
        splash.root.mainloop()

        return splash


def test_splash():
    """Test the splash screen"""

    def on_complete():
        print("Loading complete!")

    splash = SplashScreen()
    splash.show()
    splash.run_loading_sequence(callback=on_complete)
    splash.mainloop()


if __name__ == '__main__':
    test_splash()

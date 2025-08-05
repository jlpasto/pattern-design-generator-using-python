import tkinter as tk
from tkinter import ttk, messagebox

class PatternAssemblyGUI:
    def __init__(self, master):
        self.master = master
        master.title("Pattern Assembly Program")
        master.geometry("600x800") # Set initial window size

        self.results = None # Initialize results to None, will be set on submit

        # Configure grid for better resizing
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)

        # Create a main frame for padding and organization
        self.main_frame = ttk.Frame(master, padding="20 20 20 20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        # Configure main_frame grid for two columns: labels and inputs
        self.main_frame.columnconfigure(0, weight=0) # Column for labels (fixed width, or content-based)
        self.main_frame.columnconfigure(1, weight=1) # Column for entries (expands)

        self.current_grid_row = 0 # To manage sequential placement of widgets

        self.create_widgets()
        self.reset_form() # Start with initial state: only the first question visible

    def create_widgets(self):
        # --- Widgets for Step 1: "Do you want to assemble a pattern?" ---
        self.q1_label = ttk.Label(self.main_frame, text="Do you want to assemble a pattern?")
        self.assemble_choice_var = tk.StringVar(value="yes")
        self.assemble_yes_radio = ttk.Radiobutton(self.main_frame, text="Yes", variable=self.assemble_choice_var, value="yes", command=self.advance_flow)
        self.assemble_no_radio = ttk.Radiobutton(self.main_frame, text="No", variable=self.assemble_choice_var, value="no", command=self.advance_flow)

        self.step1_widgets = [
            self.q1_label, self.assemble_yes_radio, self.assemble_no_radio
        ]

        # --- Pattern name entry (always present, but its visibility is managed by flow) ---
        self.pattern_name_label = ttk.Label(self.main_frame, text="Pattern/Motif Name:")
        self.assemble_pattern_entry = ttk.Entry(self.main_frame, width=40)

        # --- Widgets for 'No Assembly' Flow (dimensions for Produit/Frise, is_border) ---
        self.produit_dims_label = ttk.Label(self.main_frame, text="Dimensions for Produit (if no assembly):")
        self.width_produit_label = ttk.Label(self.main_frame, text="Width (default 1990):")
        self.width_produit_entry = ttk.Entry(self.main_frame, width=20)
        self.width_produit_entry.insert(0, "1990")

        self.height_produit_label = ttk.Label(self.main_frame, text="Height (default 1771):")
        self.height_produit_entry = ttk.Entry(self.main_frame, width=20)
        self.height_produit_entry.insert(0, "1771")

        self.frise_dims_label = ttk.Label(self.main_frame, text="Dimensions for Frise (if no assembly):")
        self.width_frise_label = ttk.Label(self.main_frame, text="Width (default 501):")
        self.width_frise_entry = ttk.Entry(self.main_frame, width=20)
        self.width_frise_entry.insert(0, "501")

        self.height_frise_label = ttk.Label(self.main_frame, text="Height (default 780):")
        self.height_frise_entry = ttk.Entry(self.main_frame, width=20)
        self.height_frise_entry.insert(0, "780")

        self.is_border_label = ttk.Label(self.main_frame, text="Is this a pattern for border?")
        self.is_border_var = tk.StringVar(value="no")
        self.is_border_yes_radio = ttk.Radiobutton(self.main_frame, text="Yes", variable=self.is_border_var, value="yes")
        self.is_border_no_radio = ttk.Radiobutton(self.main_frame, text="No", variable=self.is_border_var, value="no")

        self.no_assembly_flow_widgets = [
            self.produit_dims_label, # This is a header, should span 2 columns
            self.width_produit_label, self.width_produit_entry,
            self.height_produit_label, self.height_produit_entry,
            self.frise_dims_label, # This is a header, should span 2 columns
            self.width_frise_label, self.width_frise_entry,
            self.height_frise_label, self.height_frise_entry,
            self.is_border_label, self.is_border_yes_radio, self.is_border_no_radio
        ]

        # --- Widgets for 'Yes Assembly' Flow - Type and Subtype Selection ---
        self.assembly_type_label = ttk.Label(self.main_frame, text="Which type of assembly do you want to perform?")
        self.assembly_type_choice_var = tk.StringVar(value="product assembly")
        self.product_assembly_radio = ttk.Radiobutton(self.main_frame, text="Product Assembly", variable=self.assembly_type_choice_var, value="product assembly", command=self.advance_flow)
        self.border_assembly_radio = ttk.Radiobutton(self.main_frame, text="Border Assembly", variable=self.assembly_type_choice_var, value="border assembly", command=self.advance_flow)
        self.both_assembly_radio = ttk.Radiobutton(self.main_frame, text="Both", variable=self.assembly_type_choice_var, value="both", command=self.advance_flow)

        self.assembly_subtype_label = ttk.Label(self.main_frame, text="Choose the type of assembly:")
        self.assembly_subtype_choice_var = tk.IntVar(value=1)
        self.assembly_subtype_radios = []
        for i in range(1, 7):
            radio = ttk.Radiobutton(self.main_frame, text=f"Type {i}", variable=self.assembly_subtype_choice_var, value=i)
            self.assembly_subtype_radios.append(radio)

        self.yes_assembly_type_widgets = [
            self.assembly_type_label, # Header
            self.product_assembly_radio, self.border_assembly_radio, self.both_assembly_radio,
            self.assembly_subtype_label # Header
        ] + self.assembly_subtype_radios

        # --- Widgets for Product Grid/Output (used in 'both' or 'product assembly') ---
        self.num_rows_product_label = ttk.Label(self.main_frame, text="Product Grid Rows (default 2):")
        self.num_rows_product_entry = ttk.Entry(self.main_frame, width=20)
        self.num_rows_product_entry.insert(0, "2")
        self.num_cols_product_label = ttk.Label(self.main_frame, text="Product Grid Columns (default 2):")
        self.num_cols_product_entry = ttk.Entry(self.main_frame, width=20)
        self.num_cols_product_entry.insert(0, "2")
        self.width_product_label_yes = ttk.Label(self.main_frame, text="Product Output Width (default 1990):")
        self.width_product_entry_yes = ttk.Entry(self.main_frame, width=20)
        self.width_product_entry_yes.insert(0, "1990")
        self.height_product_label_yes = ttk.Label(self.main_frame, text="Product Output Height (default 1771):")
        self.height_product_entry_yes = ttk.Entry(self.main_frame, width=20)
        self.height_product_entry_yes.insert(0, "1771")

        self.product_grid_output_widgets = [
            self.num_rows_product_label, self.num_rows_product_entry,
            self.num_cols_product_label, self.num_cols_product_entry,
            self.width_product_label_yes, self.width_product_entry_yes,
            self.height_product_label_yes, self.height_product_entry_yes
        ]

        # --- Widgets for Border Grid/Output (used in 'both' or 'border assembly') ---
        self.num_rows_border_label = ttk.Label(self.main_frame, text="Border Grid Rows (default 9):")
        self.num_rows_border_entry = ttk.Entry(self.main_frame, width=20)
        self.num_rows_border_entry.insert(0, "9")
        self.num_cols_border_label = ttk.Label(self.main_frame, text="Border Grid Columns (default 4):")
        self.num_cols_border_entry = ttk.Entry(self.main_frame, width=20)
        self.num_cols_border_entry.insert(0, "4")
        self.width_border_label_yes = ttk.Label(self.main_frame, text="Border Output Width (default 501):")
        self.width_border_entry_yes = ttk.Entry(self.main_frame, width=20)
        self.width_border_entry_yes.insert(0, "501")
        self.height_border_label_yes = ttk.Label(self.main_frame, text="Border Output Height (default 780):")
        self.height_border_entry_yes = ttk.Entry(self.main_frame, width=20)
        self.height_border_entry_yes.insert(0, "780")

        self.border_grid_output_widgets = [
            self.num_rows_border_label, self.num_rows_border_entry,
            self.num_cols_border_label, self.num_cols_border_entry,
            self.width_border_label_yes, self.width_border_entry_yes,
            self.height_border_label_yes, self.height_border_entry_yes
        ]

        # --- Widgets for Single Grid (used in 'product assembly' or 'border assembly' when not 'both') ---
        self.num_rows_label = ttk.Label(self.main_frame, text="Grid Rows (default based on assembly type):")
        self.num_rows_entry = ttk.Entry(self.main_frame, width=20)
        self.num_cols_label = ttk.Label(self.main_frame, text="Grid Columns (default based on assembly type):")
        self.num_cols_entry = ttk.Entry(self.main_frame, width=20)

        self.single_grid_widgets = [
            self.num_rows_label, self.num_rows_entry,
            self.num_cols_label, self.num_cols_entry
        ]

        # --- Buttons and Results Display ---
        self.submit_button = ttk.Button(self.main_frame, text="Submit", command=self.submit_form)
        self.reset_button = ttk.Button(self.main_frame, text="Reset", command=self.reset_form)
        #self.results_label = ttk.Label(self.main_frame, text="Results will appear here.")

        # Group all conditional widgets for easy hiding/showing
        self.all_flow_widgets = (
            # Pattern name label and entry are handled separately in advance_flow for consistent placement
            *self.no_assembly_flow_widgets,
            *self.yes_assembly_type_widgets,
            *self.product_grid_output_widgets,
            *self.border_grid_output_widgets,
            *self.single_grid_widgets
        )

    def hide_all_widgets(self):
        """Hides all widgets that are part of the dynamic flow."""
        for widget in self.step1_widgets:
            widget.grid_forget()
        # Pattern name label and entry are also dynamically placed, so hide them here
        self.pattern_name_label.grid_forget()
        self.assemble_pattern_entry.grid_forget()

        for widget in self.all_flow_widgets:
            widget.grid_forget()
        self.submit_button.grid_forget()
        self.reset_button.grid_forget()
        #self.results_label.grid_forget()

    def place_widgets(self, widget_list):
        """Places a list of widgets sequentially in the grid, handling label-entry alignment."""
        i = 0
        while i < len(widget_list):
            widget = widget_list[i]
            if isinstance(widget, ttk.Label) and i + 1 < len(widget_list) and isinstance(widget_list[i+1], ttk.Entry):
                # This is a label followed by an entry, place them on the same row
                label = widget
                entry = widget_list[i+1]
                label.grid(row=self.current_grid_row, column=0, sticky=tk.W, pady=5)
                entry.grid(row=self.current_grid_row, column=1, sticky=tk.W + tk.E, padx=20)
                self.current_grid_row += 1
                i += 2 # Skip the next widget as it's already placed
            elif isinstance(widget, ttk.Radiobutton):
                # Radio buttons span both columns for better centering
                widget.grid(row=self.current_grid_row, column=0, sticky=tk.W, padx=20, columnspan=2)
                self.current_grid_row += 1
                i += 1
            else: # Other labels (like section titles)
                # Standalone labels span two columns
                widget.grid(row=self.current_grid_row, column=0, sticky=tk.W, pady=5, columnspan=2)
                self.current_grid_row += 1
                i += 1

    def advance_flow(self):
        """Manages the sequential display of input sections based on user choices."""
        self.hide_all_widgets() # Clear previous step's widgets
        self.current_grid_row = 0 # Reset row counter for new placement

        assemble_choice = self.assemble_choice_var.get()
        assembly_type_choice = self.assembly_type_choice_var.get()

        # Always show the first question (Step 1)
        self.place_widgets(self.step1_widgets)
        
        # Pattern name is always shown after the first question, aligned with entries
        self.pattern_name_label.grid(row=self.current_grid_row, column=0, sticky=tk.W, pady=5)
        self.assemble_pattern_entry.grid(row=self.current_grid_row, column=1, sticky=tk.W + tk.E, padx=20)
        self.current_grid_row += 1


        if assemble_choice == 'no':
            # If "No" to assembling, show the 'no assembly' specific inputs
            self.place_widgets(self.no_assembly_flow_widgets)
        else: # assemble_choice == 'yes'
            # If "Yes" to assembling, show assembly type and subtype
            self.place_widgets(self.yes_assembly_type_widgets)

            # Then, based on assembly type, show relevant grid/output dimensions
            if assembly_type_choice == 'both':
                self.place_widgets(self.product_grid_output_widgets)
                self.place_widgets(self.border_grid_output_widgets)
            elif assembly_type_choice == 'product assembly':
                # Set default values for single grid based on product assembly
                self.num_rows_entry.delete(0, tk.END)
                self.num_rows_entry.insert(0, "2")
                self.num_cols_entry.delete(0, tk.END)
                self.num_cols_entry.insert(0, "2")
                self.place_widgets(self.single_grid_widgets)
                self.place_widgets(self.product_grid_output_widgets[-4:]) # Last 4 are output dims
            elif assembly_type_choice == 'border assembly':
                # Set default values for single grid based on border assembly
                self.num_rows_entry.delete(0, tk.END)
                self.num_rows_entry.insert(0, "9")
                self.num_cols_entry.delete(0, tk.END)
                self.num_cols_entry.insert(0, "4")
                self.place_widgets(self.single_grid_widgets)
                self.place_widgets(self.border_grid_output_widgets[-4:]) # Last 4 are output dims

        # Place buttons and results label at the end of the current flow
        self.submit_button.grid(row=self.current_grid_row, column=0, pady=20, columnspan=2)
        self.current_grid_row += 1
        self.reset_button.grid(row=self.current_grid_row, column=0, pady=5, columnspan=2)
        self.current_grid_row += 1
        #self.results_label.grid(row=self.current_grid_row, column=0, sticky=tk.W, pady=10, columnspan=2)
        self.current_grid_row += 1

        self.master.update_idletasks() # Update layout immediately after changes

    def validate_integer_input(self, value, default_value, field_name):
        """Validates if an input value is an integer and meets minimum requirements."""
        if not value.strip():
            return default_value
        try:
            int_val = int(value)
            if int_val < 1 and ("rows" in field_name.lower() or "columns" in field_name.lower()):
                raise ValueError(f"{field_name} must be at least 1.")
            return int_val
        except ValueError as e:
            messagebox.showerror("Invalid Input", f"Please enter a valid integer for {field_name}. {e}")
            raise # Re-raise to stop processing the form

    def submit_form(self):
        """Collects and validates all form inputs, then displays the results."""
        # self.results = {} # No need to clear here, it's set below

        assemble_choice = self.assemble_choice_var.get()
        
        assemble_pattern = self.assemble_pattern_entry.get().strip()
        if not assemble_pattern:
            messagebox.showerror("Input Error", "Please enter a pattern name.")
            return
        
        # Store results temporarily in a local variable
        current_results = {}
        current_results["assemble_choice"] = assemble_choice
        current_results["assemble_pattern"] = assemble_pattern

        if assemble_choice == 'no':
            try:
                width_produit = self.validate_integer_input(self.width_produit_entry.get(), 1990, "Produit Width")
                height_produit = self.validate_integer_input(self.height_produit_entry.get(), 1771, "Produit Height")
                width_frise = self.validate_integer_input(self.width_frise_entry.get(), 501, "Frise Width")
                height_frise = self.validate_integer_input(self.height_frise_entry.get(), 780, "Frise Height")
            except Exception: # Catch the re-raised ValueError from validate_integer_input
                return

            is_border_answer = self.is_border_var.get()

            current_results.update({
                "assemble_choice": "no",
                "assemble_pattern": assemble_pattern,
                "width_produit": width_produit,
                "height_produit": height_produit,
                "width_frise": width_frise,
                "height_frise": height_frise,
                "is_border_answer": is_border_answer
            })

            output_message = "\n--- The layers are being generated... \n Locate output folder for result. ---\n"
            
            # Set the instance variable self.results
            self.results = current_results

        else: # assemble_choice == 'yes'
            assembly_type_choice = self.assembly_type_choice_var.get()
            assembly_subtype_choice = self.assembly_subtype_choice_var.get()

            current_results["assembly_type_choice"] = assembly_type_choice
            current_results["assembly_subtype_choice"] = assembly_subtype_choice

            try:
                if assembly_type_choice == 'both':
                    num_rows_product = self.validate_integer_input(self.num_rows_product_entry.get(), 2, "Product Rows")
                    num_cols_product = self.validate_integer_input(self.num_cols_product_entry.get(), 2, "Product Columns")
                    width_product = self.validate_integer_input(self.width_product_entry_yes.get(), 1990, "Product Output Width")
                    height_product = self.validate_integer_input(self.height_product_entry_yes.get(), 1771, "Product Output Height")
                    num_rows_border = self.validate_integer_input(self.num_rows_border_entry.get(), 9, "Border Rows")
                    num_cols_border = self.validate_integer_input(self.num_cols_border_entry.get(), 4, "Border Columns")
                    width_border = self.validate_integer_input(self.width_border_entry_yes.get(), 501, "Border Output Width")
                    height_border = self.validate_integer_input(self.height_border_entry_yes.get(), 780, "Border Output Height")

                    current_results.update({
                        "num_rows_product": num_rows_product,
                        "num_cols_product": num_cols_product,
                        "width_product": width_product,
                        "height_product": height_product,
                        "num_rows_border": num_rows_border,
                        "num_cols_border": num_cols_border,
                        "width_border": width_border,
                        "height_border": height_border
                    })

                    # Match the original script's return type (tuple for 'yes' path)
                    self.results = (
                        assemble_pattern, assemble_choice, assembly_type_choice, assembly_subtype_choice,
                        num_rows_product, num_cols_product, width_product, height_product,
                        num_rows_border, num_cols_border, width_border, height_border
                    )
                    output_message = "\n--- The layers are being generated... \n Locate output folder for result. ---\n"

                else: # product assembly or border assembly
                    default_rows = 2 if assembly_type_choice == 'product assembly' else 9
                    default_cols = 2 if assembly_type_choice == 'product assembly' else 4

                    num_rows = self.validate_integer_input(self.num_rows_entry.get(), default_rows, "Grid Rows")
                    num_cols = self.validate_integer_input(self.num_cols_entry.get(), default_cols, "Grid Columns")

                    current_results.update({
                        "num_rows": num_rows,
                        "num_cols": num_cols
                    })

                    if assembly_type_choice == 'product assembly':
                        width_product = self.validate_integer_input(self.width_product_entry_yes.get(), 1990, "Product Output Width")
                        height_product = self.validate_integer_input(self.height_product_entry_yes.get(), 1771, "Product Output Height")
                        current_results.update({
                            "width_product": width_product,
                            "height_product": height_product
                        })
                        # Match the original script's return type (tuple for 'yes' path)
                        self.results = (
                            assemble_pattern, assemble_choice, assembly_type_choice, assembly_subtype_choice,
                            num_rows, num_cols, width_product, height_product
                        )
                        output_message = "\n--- The layers are being generated... \n Locate output folder for result. ---\n"
                        

                    else: # border assembly
                        width_border = self.validate_integer_input(self.width_border_entry_yes.get(), 501, "Border Output Width")
                        height_border = self.validate_integer_input(self.height_border_entry_yes.get(), 780, "Border Output Height")
                        current_results.update({
                            "width_border": width_border,
                            "height_border": height_border
                        })
                        # Match the original script's return type (tuple for 'yes' path)
                        self.results = (
                            assemble_pattern, assemble_choice, assembly_type_choice, assembly_subtype_choice,
                            num_rows, num_cols, width_border, height_border
                        )
                        output_message = "\n--- The layers are being generated... \n Locate output folder for result. ---\n"

            except Exception: # Catch the re-raised ValueError
                return

        messagebox.showinfo("Form Submitted", output_message)
        #self.results_label.config(text=output_message)
        print(self.results) # For console output as per original request
        
        # Close the window after submission
        self.master.quit() # Stop the Tkinter event loop
        self.master.destroy() # Destroy the window


    def reset_form(self):
        """Resets all input fields and returns the GUI to its initial state."""
        # Clear all entry fields
        self.assemble_pattern_entry.delete(0, tk.END)
        self.width_produit_entry.delete(0, tk.END)
        self.height_produit_entry.delete(0, tk.END)
        self.width_frise_entry.delete(0, tk.END)
        self.height_frise_entry.delete(0, tk.END)
        self.num_rows_product_entry.delete(0, tk.END)
        self.num_cols_product_entry.delete(0, tk.END)
        self.width_product_entry_yes.delete(0, tk.END)
        self.height_product_entry_yes.delete(0, tk.END)
        self.num_rows_border_entry.delete(0, tk.END)
        self.num_cols_border_entry.delete(0, tk.END)
        self.width_border_entry_yes.delete(0, tk.END)
        self.height_border_entry_yes.delete(0, tk.END)
        self.num_rows_entry.delete(0, tk.END)
        self.num_cols_entry.delete(0, tk.END)

        # Reset variables to their default values
        self.assemble_choice_var.set("yes")
        self.is_border_var.set("no")
        self.assembly_type_choice_var.set("product assembly")
        self.assembly_subtype_choice_var.set(1)

        # Re-insert default values for entries
        self.width_produit_entry.insert(0, "1990")
        self.height_produit_entry.insert(0, "1771")
        self.width_frise_entry.insert(0, "501")
        self.height_frise_entry.insert(0, "780")
        self.num_rows_product_entry.insert(0, "2")
        self.num_cols_product_entry.insert(0, "2")
        self.width_product_entry_yes.insert(0, "1990")
        self.height_product_entry_yes.insert(0, "1771")
        self.num_rows_border_entry.insert(0, "9")
        self.num_cols_border_entry.insert(0, "4")
        self.width_border_entry_yes.insert(0, "501")
        self.height_border_entry_yes.insert(0, "780")
        self.num_rows_entry.insert(0, "2") # Default for product assembly
        self.num_cols_entry.insert(0, "2") # Default for product assembly


        #self.results_label.config(text="Results will appear here.")
        self.advance_flow() # Restart the flow from the beginning

# --- Wrapper function to run the GUI and get results ---
def get_pattern_assembly_params():
    root = tk.Tk()
    app = PatternAssemblyGUI(root)
    root.mainloop() # This will block until root.destroy() is called

    # After mainloop exits, app.results will contain the submitted data
    return app.results

# Main execution (for testing this script directly)
if __name__ == "__main__":
    # This block will only run if you execute this script directly
    # If you import it into another script, this block is skipped.
    print("Running GUI to get parameters...")
    params = get_pattern_assembly_params()
    print("\n--- Parameters received from GUI ---")
    print(params)
    print("GUI application closed.")

import sys

def assemble_pattern_program_numbered():
    """
    This function demonstrates how to prompt a user for input
    using numbered options and then use it in a program.
    """

    # 1: Do you want to assemble a pattern?
    while True:
        print("\nDo you want to assemble a pattern?")
        print("  1. Yes")
        print("  2. No")
        assemble_choice_num = input("Enter your choice (1 or 2): ")

        if assemble_choice_num == '1':
            assemble_choice = 'yes'
            break
        elif assemble_choice_num == '2':
            assemble_choice = 'no'
            break
        else:
            print("Invalid input. Please enter '1' for Yes or '2' for No.")

    if assemble_choice == 'no':
        print("Okay, no pattern assembly will be performed.")
        # Ask for pattern name
        while True:
            assemble_pattern = input("Enter the name of the pattern/motif: ")
            if assemble_pattern.strip() == '':
                print("Invalid input. Please enter a pattern name.")
            else:
                break
        # # Ask for output size
        while True:
            try:
                print("Enter dimensions for Produit.")
                width_produit = int(input("Enter output width (default 1990): ") or "1990")
                height_produit = int(input("Enter output height (default 1771): ") or "1771")
                break
            except ValueError:
                print("Please enter valid integers for width and height.")

        # # Ask for output size
        while True:
            try:
                print("Enter dimensions for Frise.")
                width_frise = int(input("Enter output width (default 501): ") or "501")
                height_frise = int(input("Enter output height (default 780): ") or "780")
                break
            except ValueError:
                print("Please enter valid integers for width and height.")


        # # Ask if border type
        while True:
            print("\nIs this a pattern for border?")
            print("  1. Yes")
            print("  2. No")

            try:
                is_border = input("Enter your choice (1 or 2): ")

                if is_border == '1':
                    is_border_answer = 'yes'
                    break
                elif is_border == '2':
                    is_border_answer = 'no'
                    break
                else:
                    print("Invalid input. Please enter '1' for Yes or '2' for No.")
            except ValueError:
                print("Please enter valid integers for width and height.")

        # Return a dict with the info, including assemble_pattern and assemble_ppatern
        return {
            "assemble_choice": "no",
            "assemble_pattern": assemble_pattern,
            "width_produit" : width_produit,
            "height_produit" : height_produit,
            "width_frise" : width_frise,
            "height_frise" : height_frise,
            "is_border_answer": is_border_answer
        }
         
       
    # What is the name of pattern? (ex. maria)
    while True:
        print("\nWhat is the name of pattern/motif?")
        assemble_pattern = input("Enter pattern name: ")

        if assemble_pattern == '':
            print("Invalid input. Please enter a pattern")
        else:
            break
        
        # add check if pattern exist in directory

    # 2. Which type of assembly do you want to perform?
    while True:
        print("\nWhich type of assembly do you want to perform?")
        print("  1. Product Assembly")
        print("  2. Border Assembly")
        print("  3. Both")
        assembly_type_choice_num = input("Enter your choice (1, 2, or 3): ")

        if assembly_type_choice_num == '1':
            assembly_type_choice = 'product assembly'
            break
        elif assembly_type_choice_num == '2':
            assembly_type_choice = 'border assembly'
            break
        elif assembly_type_choice_num == '3':
            assembly_type_choice = 'both'
            break
        else:
            print("Invalid input. Please enter 1, 2, or 3.")

    
    # 3. Choose the type of assembly:
    while True:
        print("\nChoose the type of assembly:")
        print("  1. Type 1")
        print("  2. Type 2")
        print("  3. Type 3")
        print("  4. Type 4")
        print("  5. Type 5")
        print("  6. Type 6")
        assembly_subtype_choice_num = input("Enter your choice (1-6): ")

        if assembly_subtype_choice_num == '1':
            assembly_subtype_choice = 1
            break
        elif assembly_subtype_choice_num == '2':
            assembly_subtype_choice = 2
            break
        elif assembly_subtype_choice_num == '3':
            assembly_subtype_choice = 3
            break
        elif assembly_subtype_choice_num == '4':
            assembly_subtype_choice = 4
            break
        elif assembly_subtype_choice_num == '5':
            assembly_subtype_choice = 5
            break
        elif assembly_subtype_choice_num == '6':
            assembly_subtype_choice = 6
            break
        else:
            print("Invalid input. Please enter a number between 1 and 6.")

    if assembly_type_choice == 'both':
        # Product grid size
        while True:
            try:
                print("\nEnter the number of rows for the PRODUCT grid (default 2):")
                num_rows_product_input = input("Product Rows: ")
                num_rows_product = int(num_rows_product_input) if num_rows_product_input.strip() else 2
                if num_rows_product < 1:
                    print("Number of rows must be at least 1.")
                    continue
                break
            except ValueError:
                print("Please enter a valid integer.")
        while True:
            try:
                print("Enter the number of columns for the PRODUCT grid (default 2):")
                num_cols_product_input = input("Product Columns: ")
                num_cols_product = int(num_cols_product_input) if num_cols_product_input.strip() else 2
                if num_cols_product < 1:
                    print("Number of columns must be at least 1.")
                    continue
                break
            except ValueError:
                print("Please enter a valid integer.")
        # Product output dimensions
        print("\nEnter the output WIDTH in pixels for PRODUCT layer (default: 1990):")
        width_product_input = input("Product Width: ")
        width_product = int(width_product_input) if width_product_input.strip() else 1990
        print("Enter the output HEIGHT in pixels for PRODUCT layer (default: 1771):")
        height_product_input = input("Product Height: ")
        height_product = int(height_product_input) if height_product_input.strip() else 1771
        # Border grid size
        while True:
            try:
                print("\nEnter the number of rows for the BORDER grid (default 9):")
                num_rows_border_input = input("Border Rows: ")
                num_rows_border = int(num_rows_border_input) if num_rows_border_input.strip() else 9
                if num_rows_border < 1:
                    print("Number of rows must be at least 1.")
                    continue
                break
            except ValueError:
                print("Please enter a valid integer.")
        while True:
            try:
                print("Enter the number of columns for the BORDER grid (default 4):")
                num_cols_border_input = input("Border Columns: ")
                num_cols_border = int(num_cols_border_input) if num_cols_border_input.strip() else 4
                if num_cols_border < 1:
                    print("Number of columns must be at least 1.")
                    continue
                break
            except ValueError:
                print("Please enter a valid integer.")
        # Border output dimensions
        print("\nEnter the output WIDTH in pixels for BORDER layer (default: 501):")
        width_border_input = input("Border Width: ")
        width_border = int(width_border_input) if width_border_input.strip() else 501
        print("Enter the output HEIGHT in pixels for BORDER layer (default: 780):")
        height_border_input = input("Border Height: ")
        height_border = int(height_border_input) if height_border_input.strip() else 780
    else:
        while True:
            try:
                print("\nEnter the number of rows for the grid:")
                print("  - Default 2 for product assembly")
                print("  - Default 9 for border assembly")
                num_rows_input = input("Rows: ")
                num_rows = int(num_rows_input) if num_rows_input.strip() else 2
                if num_rows < 1:
                    print("Number of rows must be at least 1.")
                    continue
                break
            except ValueError:
                print("Please enter a valid integer.")
        while True:
            try:
                print("Enter the number of columns for the grid:")
                print("  - Default 2 for product assembly") 
                print("  - Default 4 for border assembly")
                num_cols_input = input("Columns: ")
                num_cols = int(num_cols_input) if num_cols_input.strip() else 2
                if num_cols < 1:
                    print("Number of columns must be at least 1.")
                    continue
                break
            except ValueError:
                print("Please enter a valid integer.")
        # Output dimensions
        if assembly_type_choice == 'product assembly':
            print("\nEnter the output WIDTH in pixels for PRODUCT layer (default: 1990):")
            width_product_input = input("Product Width: ")
            width_product = int(width_product_input) if width_product_input.strip() else 1990
            print("Enter the output HEIGHT in pixels for PRODUCT layer (default: 1771):")
            height_product_input = input("Product Height: ")
            height_product = int(height_product_input) if height_product_input.strip() else 1771
        else:
            print("\nEnter the output WIDTH in pixels for BORDER layer (default: 501):")
            width_border_input = input("Border Width: ")
            width_border = int(width_border_input) if width_border_input.strip() else 501
            print("Enter the output HEIGHT in pixels for BORDER layer (default: 780):")
            height_border_input = input("Border Height: ")
            height_border = int(height_border_input) if height_border_input.strip() else 780

    print("\n--- Your Assembly Choices ---")
    print(f"Assemble a pattern: {assemble_choice}")
    print(f"Pattern name: {assemble_pattern}")
    print(f"Type of assembly: {assembly_type_choice}")
    print(f"Specific assembly type: {assembly_subtype_choice}")
    if assembly_type_choice == 'both':
        print(f"Product grid size: {num_rows_product} rows x {num_cols_product} columns")
        print(f"Product output size: {width_product} x {height_product} px")
        print(f"Border grid size: {num_rows_border} rows x {num_cols_border} columns")
        print(f"Border output size: {width_border} x {height_border} px")
        return assemble_pattern, assemble_choice, assembly_type_choice, assembly_subtype_choice, num_rows_product, num_cols_product, width_product, height_product, num_rows_border, num_cols_border, width_border, height_border
    else:
        print(f"Grid size: {num_rows} rows x {num_cols} columns")
        if assembly_type_choice == 'product assembly':
            print(f"Product output size: {width_product} x {height_product} px")
            return assemble_pattern, assemble_choice, assembly_type_choice, assembly_subtype_choice, num_rows, num_cols, width_product, height_product
        else:
            print(f"Border output size: {width_border} x {height_border} px")
            return assemble_pattern, assemble_choice, assembly_type_choice, assembly_subtype_choice, num_rows, num_cols, width_border, height_border
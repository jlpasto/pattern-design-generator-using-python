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
        sys.exit(0) # Exit the function if the user doesn't want to assemble
         
       
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
        assembly_subtype_choice_num = input("Enter your choice (1-5): ")

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
        else:
            print("Invalid input. Please enter a number between 1 and 5.")

    if assembly_type_choice == 5:
        print("Type 5 not yet supported")
        sys.exit(0) # Exit the function if the user chose type 5
    

    print("\n--- Your Assembly Choices ---")
    print(f"Assemble a pattern: {assemble_choice}")
    print(f"Pattern name: {assemble_pattern}")
    print(f"Type of assembly: {assembly_type_choice}")
    print(f"Specific assembly type: {assembly_subtype_choice}")

    return assemble_pattern, assemble_choice, assembly_type_choice, assembly_subtype_choice
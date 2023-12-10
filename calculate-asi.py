import math

def calculate_asi(as_vector):
    def calculate_component_squared(component):
        if isinstance(component, tuple):
            return sum(calculate_component_squared(inner_component) for inner_component in component)
        else:
            return component**2
    
    asi_squared = sum(calculate_component_squared(component) for component in as_vector)
    asi = math.sqrt(asi_squared)
    return asi

def main():
    # Get user input for the Attack Surface vector
    as_vector_str = input("Enter the Attack Surface vector in the format (a, b, (c1, c2, ...), (d1, d2, ...), (e1, e2, ...), f, g, h): ")
    
    # Convert the user input string into a tuple
    try:
        as_vector = eval(as_vector_str)
    except:
        print("Invalid input format. Please enter the vector in the correct format.")
        return
    
    # Calculate the Attack Surface Index (ASI)
    asi = calculate_asi(as_vector)
    
    # Print the result
    print(f"The Attack Surface Index (ASI) for the given vector {as_vector} is approximately {asi:.2f}.")

if __name__ == "__main__":
    main()
